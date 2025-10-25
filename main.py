from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

# Importar tus clases
from clases import Billetera, Descripcion, Monto, Tipo, Category, Type, Id, Transaction, BalanceNegativoException

app = FastAPI(title="API de Billetera")

# Modelo Pydantic para crear una transacción
class TransactionCreate(BaseModel):
    descripcion: str = Field(..., max_length=50)
    monto: float = Field(..., gt=0)
    tipo: Type
    categoria: Category

# Modelo Pydantic para modificar transacción
class TransactionUpdate(BaseModel):
    descripcion: Optional[str] = Field(None, max_length=50)
    monto: Optional[float] = Field(None, gt=0)
    tipo: Optional[Type] = None
    categoria: Optional[Category] = None

# Modelo para devolver transacción
class TransactionOut(BaseModel):
    id: str
    descripcion: str
    monto: float
    tipo: str
    categoria: str
    fecha: datetime

# Crear una billetera global para pruebas
mi_billetera = Billetera.generate()

# Endpoint para agregar transacción
@app.post("/transacciones", response_model=TransactionOut)
def agregar_transaccion(tx: TransactionCreate):
    try:
        descripcion = Descripcion(tx.descripcion)
        monto = Monto(tx.monto)
        tipo = Tipo(tx.tipo)
        categoria = tx.categoria
        mi_billetera.agregar_transaccion(descripcion, monto, tipo, categoria)
        # Obtener la última transacción agregada
        transaccion = list(mi_billetera.transacciones.values())[-1]
        return TransactionOut(
            id=str(transaccion.id),
            descripcion=str(transaccion.descripcion),
            monto=transaccion.monto.value,
            tipo=transaccion.tipo,
            categoria=transaccion.categoria.value,
            fecha=transaccion.fecha
        )
    except BalanceNegativoException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para eliminar transacción
@app.delete("/transacciones/{tx_id}")
def eliminar_transaccion(tx_id: str):
    try:
        id_obj = Id.generate_from_string(tx_id)
        mi_billetera.eliminar_transaccion(id_obj.value)
        return {"detail": "Transacción eliminada"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BalanceNegativoException as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para modificar transacción
@app.put("/transacciones/{tx_id}", response_model=TransactionOut)
def modificar_transaccion(tx_id: str, tx_update: TransactionUpdate):
    try:
        id_obj = Id.generate_from_string(tx_id)
        if id_obj.value not in mi_billetera.transacciones:
            raise HTTPException(status_code=404, detail="Transacción no encontrada")
        
        transaccion = mi_billetera.transacciones[id_obj.value]

        nueva_descripcion = Descripcion(tx_update.descripcion) if tx_update.descripcion else None
        nuevo_monto = Monto(tx_update.monto) if tx_update.monto else None
        nuevo_tipo = Tipo(tx_update.tipo) if tx_update.tipo else None
        nueva_categoria = tx_update.categoria if tx_update.categoria else None

        transaccion.modificar(nueva_descripcion, nuevo_monto, nuevo_tipo, nueva_categoria)
        return TransactionOut(
            id=str(transaccion.id),
            descripcion=str(transaccion.descripcion),
            monto=transaccion.monto.value,
            tipo=transaccion.tipo,
            categoria=transaccion.categoria.value,
            fecha=transaccion.fecha
        )
    except BalanceNegativoException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para obtener balance actual
@app.get("/balance")
def balance():
    return {
        "balance_actual": mi_billetera.balance_actual(),
        "total_ingresos": mi_billetera.total_ingresos(),
        "total_gastos": mi_billetera.total_gastos()
    }

# Endpoint para listar todas las transacciones
@app.get("/transacciones", response_model=List[TransactionOut])
def historial():
    return [
        TransactionOut(
            id=str(t.id),
            descripcion=str(t.descripcion),
            monto=t.monto.value,
            tipo=t.tipo,
            categoria=t.categoria.value,
            fecha=t.fecha
        )
        for t in mi_billetera.transacciones.values()
    ]





