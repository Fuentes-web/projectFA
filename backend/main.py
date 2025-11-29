from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from sqlmodel import Session, select
from decimal import Decimal
from fastapi.middleware.cors import CORSMiddleware
from clases import Billetera, Descripcion, Monto, Tipo, Category, Type, Id, BalanceNegativoException
from dbmodels import TransactionModel
from database import init_db, get_session

app = FastAPI(title="API de Billetera")

@app.on_event("startup")
def on_startup():
    init_db()

# ---------------------------
# Pydantic models (API layer)
# ---------------------------
class TransactionCreate(BaseModel):
    descripcion: str = Field(..., max_length=50)
    monto: float = Field(..., gt=0)
    tipo: Type
    categoria: Category

class TransactionUpdate(BaseModel):
    descripcion: Optional[str] = Field(None, max_length=50)
    monto: Optional[float] = Field(None, gt=0)
    tipo: Optional[Type] = None
    categoria: Optional[Category] = None

class TransactionOut(BaseModel):
    id: str
    descripcion: str
    monto: float
    tipo: str
    categoria: str
    fecha: datetime

# ---------------------------
# Helper
# ---------------------------
def txmodel_to_out(tx: TransactionModel) -> TransactionOut:
    return TransactionOut(
        id=str(tx.id),
        descripcion=tx.descripcion,
        monto=float(tx.monto),
        tipo=tx.tipo,
        categoria=tx.categoria,
        fecha=tx.fecha
    )

# ---------------------------
# Create a Billetera instance
# ---------------------------
# We'll reuse the service but always set its session from the FastAPI dependency.
mi_billetera = Billetera.generate()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puedes limitar esto luego
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Create transaction
# ---------------------------
@app.post("/transacciones", response_model=TransactionOut)
def crear_transaccion(tx: TransactionCreate, session: Session = Depends(get_session)):
    mi_billetera.session = session
    try:
        descripcion = Descripcion(tx.descripcion)
        monto = Monto(tx.monto)
        tipo = Tipo(tx.tipo)
        categoria = tx.categoria

        nueva = mi_billetera.agregar_transaccion(descripcion, monto, tipo, categoria)
        # agregar_transaccion devuelve el objeto guardado (TransactionModel)
        return txmodel_to_out(nueva)

    except BalanceNegativoException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---------------------------
# Get single transaction
# ---------------------------
@app.get("/transacciones/{tx_id}", response_model=TransactionOut)
def obtener_transaccion(tx_id: str, session: Session = Depends(get_session)):
    tx_db = session.get(TransactionModel, tx_id)
    if not tx_db:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return txmodel_to_out(tx_db)

# ---------------------------
# Delete transaction
# ---------------------------
@app.delete("/transacciones/{tx_id}")
def eliminar_transaccion(tx_id: str, session: Session = Depends(get_session)):
    mi_billetera.session = session
    tx_db = session.get(TransactionModel, tx_id)
    if not tx_db:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    try:
        mi_billetera.eliminar_transaccion(tx_id)
        return {"detail": "Transacción eliminada"}
    except BalanceNegativoException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---------------------------
# Update transaction
# ---------------------------
@app.put("/transacciones/{tx_id}", response_model=TransactionOut)
def modificar_transaccion(tx_id: str, tx_update: TransactionUpdate, session: Session = Depends(get_session)):
    mi_billetera.session = session
    tx_db = session.get(TransactionModel, tx_id)
    if not tx_db:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    # Valores actuales
    old_monto = float(tx_db.monto)
    old_tipo = tx_db.tipo  # "Ingreso" o "Gasto"

    # Aplicar cambios en memoria
    if tx_update.descripcion is not None:
        tx_db.descripcion = tx_update.descripcion
    if tx_update.monto is not None:
        tx_db.monto = float(tx_update.monto)
    if tx_update.tipo is not None:
        tx_db.tipo = tx_update.tipo.value
    if tx_update.categoria is not None:
        tx_db.categoria = tx_update.categoria.value

    # Antes de confirmar, comprobar que la modificación no deja balance negativo
    # Calculamos el balance sin la transacción original y luego sumamos el efecto de la nueva.
    # 1) sumar todos los demás ingresos y restar los demás gastos
    other_txs = session.exec(select(TransactionModel).where(TransactionModel.id != tx_id)).all()
    total_others = 0.0
    for t in other_txs:
        total_others += float(t.monto) if t.tipo == "Ingreso" else -float(t.monto)

    # 2) añadir efecto de la transacción modificada
    new_effect = float(tx_db.monto) if tx_db.tipo == "Ingreso" else -float(tx_db.monto)
    projected_balance = total_others + new_effect

    if projected_balance < 0:
        session.rollback()
        raise HTTPException(status_code=400, detail="La modificación dejaría el balance en negativo")

    # Commit de la modificación
    session.add(tx_db)
    session.commit()
    session.refresh(tx_db)

    return txmodel_to_out(tx_db)

# ---------------------------
# Get balance
# ---------------------------
@app.get("/balance")
def obtener_balance(session: Session = Depends(get_session)):
    mi_billetera.session = session
    return {
        "balance_actual": mi_billetera.balance_actual(),
        "total_ingresos": mi_billetera.total_ingresos(),
        "total_gastos": mi_billetera.total_gastos()
    }

# ---------------------------
# List / filter / order transactions
# Supports query params:
#  - categoria (Category enum name or value)
#  - desde (ISO datetime string)
#  - hasta (ISO datetime string)
#  - min_amount, max_amount (floats)
#  - sort_by ("fecha","monto","categoria")
#  - asc (0 or 1)
# ---------------------------
@app.get("/transacciones", response_model=List[TransactionOut])
def listar_transacciones(
    categoria: Optional[Category] = Query(None),
    desde: Optional[str] = Query(None, description="Fecha desde (ISO)"),
    hasta: Optional[str] = Query(None, description="Fecha hasta (ISO)"),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    sort_by: Optional[str] = Query("fecha", regex="^(fecha|monto|categoria)$"),
    asc: Optional[int] = Query(1, ge=0, le=1),
    session: Session = Depends(get_session)
):
    query = select(TransactionModel)

    # Categoria
    if categoria is not None:
        # categoria puede venir como enum; TransactionModel.categoria guarda el valor (p. ej. "Alimentación")
        query = query.where(TransactionModel.categoria == categoria.value)

    # Fecha rango
    if desde is not None:
        try:
            dt_desde = datetime.fromisoformat(desde)
            query = query.where(TransactionModel.fecha >= dt_desde)
        except Exception:
            raise HTTPException(status_code=400, detail="Formato 'desde' inválido. Usa ISO (YYYY-MM-DDThh:mm:ss)")

    if hasta is not None:
        try:
            dt_hasta = datetime.fromisoformat(hasta)
            query = query.where(TransactionModel.fecha <= dt_hasta)
        except Exception:
            raise HTTPException(status_code=400, detail="Formato 'hasta' inválido. Usa ISO (YYYY-MM-DDThh:mm:ss)")

    # Montos
    if min_amount is not None:
        query = query.where(TransactionModel.monto >= min_amount)
    if max_amount is not None:
        query = query.where(TransactionModel.monto <= max_amount)

    # Ordenamiento
    order_col = getattr(TransactionModel, sort_by)
    if asc == 1:
        query = query.order_by(order_col)
    else:
        query = query.order_by(order_col.desc())

    txs = session.exec(query).all()
    return [txmodel_to_out(t) for t in txs]

# ---------------------------
# Health / root
# ---------------------------
@app.get("/")
def root():
    return {"status": "ok", "service": "billetera"}

