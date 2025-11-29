from datetime import date, datetime
from abc import ABC, abstractmethod
from enum import Enum
import uuid
from sqlmodel import Session, select
from dbmodels import TransactionModel, Type, Category
from database import engine
from sqlalchemy import func

class Monto:
    def __init__(self,monto):
        if monto<=0:
            raise ValueError("el monto no puede ser menor o igual a 0")
        self.value = monto

    def __str__(self):
        return f"{self.value}"
    
class Tipo:
    def __init__(self,tipo:Type):
        if tipo not in Type:
            raise ValueError(f"El tipo de transacción '{tipo}' no es válido. Usa Categoria Enum.")
        self.value = tipo.value
class Id:
    def __init__(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("El valor debe ser un UUID válido.")
        self.value = value
    @classmethod
    def generate(cls):
        return cls(uuid.uuid4())
    @classmethod
    def generate_from_string(cls, value: str):
        try:
            id_generate = uuid.UUID(value)
            return cls(id_generate)
        except:
            raise ValueError("El valor debe ser un UUID válido.")

class Descripcion:
    def __init__(self,descripcion):
        if len(descripcion)>50:
            raise TextoBreveException("la descripcion no puede tener mas de 50 caracteres")
        self.value = descripcion
        
    def __str__(self):
        return self.value

class TextoBreveException(Exception):
    def __init__(self,descripcion):
        self.descripcion = descripcion
        super().__init__("la descripcion no puede tener mas de 50 caracteres")
        
class BalanceNegativoException(Exception):
    def __init__(self):
        super().__init__("El gasto no puede ser mayor al balance actual")

class Transaction:
    def __init__(self,id : Id,descripcion: Descripcion,monto : Monto, tipo:Tipo,categoria:Category, fecha: datetime):
            self.id = id.value
            self.fecha = fecha   
            self.descripcion = descripcion
            self.monto = monto
            self.tipo = tipo.value
            self.categoria = categoria
            
    @classmethod
    def generate(cls, descripcion:Descripcion, monto:Monto, tipo:Tipo, categoria:Category):
        id = Id.generate()
        fecha = datetime.now()
        return cls(id, descripcion, monto, tipo, categoria, fecha)
    
    def modificar(self, nueva_descripcion:Descripcion|None, nuevo_monto:Monto|None, nuevo_tipo:Tipo|None, nueva_categoria:Category|None):
        if nueva_descripcion is not None:
            self.descripcion = nueva_descripcion
        if nuevo_monto is not None:
            self.monto = nuevo_monto
        if nuevo_tipo is not None:
            self.tipo = nuevo_tipo
        if nueva_categoria is not None:
            self.categoria = nueva_categoria

    def __add__(self,other:"Transaction")->float:
        if isinstance(other,Transaction):
            if (other.tipo==Type.INGRESO.value) and (self.tipo == Type.INGRESO.value):
                return other.monto + self.monto
            if (other.tipo==Type.GASTO.value) and (self.tipo == Type.GASTO.value):
                return -other.monto - self.monto
            if (other.tipo==Type.GASTO.value) and (self.tipo == Type.INGRESO.value):
                return -other.monto + self.monto
            if (other.tipo==Type.INGRESO.value) and (self.tipo == Type.GASTO.value):
                return other.monto - self.monto
            
        elif isinstance(other,(int,float)):
            if self.tipo == Type.INGRESO.value:
                return other + self.monto.value
            else:
                return other - self.monto.value
        else:
            raise ValueError("El valor a sumar debe ser de tipo entero/flotante/transaccion")
        
    def __radd__(self,other: int|float):
        if isinstance(other,Transaction):
            if (other.tipo==Type.INGRESO.value) and (self.tipo == Type.INGRESO.value):
                return other.monto + self.monto
            if (other.tipo==Type.GASTO.value) and (self.tipo == Type.GASTO.value):
                return -other.monto - self.monto
            if (other.tipo==Type.GASTO.value) and (self.tipo == Type.INGRESO.value):
                return -other.monto + self.monto
            if (other.tipo==Type.INGRESO.value) and (self.tipo == Type.GASTO.value):
                return other.monto - self.monto
            
        elif isinstance(other,(int,float)):
            if self.tipo == Type.INGRESO.value:
                return other + self.monto.value
            else:
                return other - self.monto.value
        else:
            raise ValueError("El valor a sumar debe ser de tipo entero/flotante/transaccion")
        
                
    def __eq__(self, other:"Transaction"):
        if other.id == self.id:
            return True    
        return False
     
    def __str__(self):
        return f"{self.id}\n{self.fecha} \n{self.descripcion} \n{self.monto} \n{self.tipo} \n{self.categoria.value}"
    

class Accion(str,Enum):
    AGREGAR = "Agregar"
    ELIMINAR = "Eliminar"
    MODIFICAR = "Modificar"
    

class Billetera:
    """
    0.factory method, generate()
    1.agregar transaccion
    2.eliminar transaccion
    3.balance actual
    4.total ingresos
    5.total gastos
    6.historial
    7.modificar transaccion
    8.buscar transaccion
    9.resumen gasto por categoria
    """
    
    def __init__(self,id:Id):
        self.id = id
        self.session = Session(engine)
                
    @classmethod
    def generate(cls):
        return cls(Id.generate())

                
    def agregar_transaccion(self, descripcion: Descripcion, monto: Monto, tipo: Tipo, categoria: Category):
        transaccion_bd = TransactionModel(descripcion=str(descripcion),monto=monto.value,tipo=tipo.value,categoria=categoria.value)

    # Validación: evitar gasto mayor al balance
        if tipo.value == Type.GASTO and self.balance_actual() < monto.value:
            raise BalanceNegativoException()

        self.session.add(transaccion_bd)
        self.session.commit()
        self.session.refresh(transaccion_bd)

        return transaccion_bd
        
    def _validar_transaccion(self,transaccion :Transaction,accion:Accion):
        if accion == Accion.AGREGAR:
            if transaccion.tipo == Type.GASTO.value:
                if self._calcular_balance()<transaccion.monto.value:
                    raise BalanceNegativoException()
        elif accion == Accion.ELIMINAR:
            if transaccion.tipo == Type.INGRESO.value:
                if self._calcular_balance()<transaccion.monto.value:
                    raise BalanceNegativoException()
        elif accion == Accion.MODIFICAR:
            pass
              
    def eliminar_transaccion(self, id_transaccion: str):
        trans = self.session.get(TransactionModel, id_transaccion)

        if not trans:
            raise ValueError("Transacción no encontrada")

        # Validación: si eliminas un ingreso no puede dejar balance negativo
        if trans.tipo == Type.INGRESO and self.balance_actual() < trans.monto:
            raise BalanceNegativoException()

        self.session.delete(trans)
        self.session.commit()

    
    def _calcular_balance(self):
        return self.balance_actual()

            
    def balance_actual(self):
        ingresos = self.session.exec(
            select(TransactionModel).where(TransactionModel.tipo == "Ingreso")
        ).all()

        gastos = self.session.exec(
            select(TransactionModel).where(TransactionModel.tipo == "Gasto")
        ).all()

        total_ingresos = sum(t.monto for t in ingresos)
        total_gastos = sum(t.monto for t in gastos)

        return total_ingresos - total_gastos

    
    def total_ingresos(self):
        ingresos = self.session.exec(
            select(TransactionModel).where(TransactionModel.tipo == "Ingreso")).all()
        return sum(t.monto for t in ingresos)

    
    def total_gastos(self):
        gastos = self.session.exec(
            select(TransactionModel).where(TransactionModel.tipo == "Gasto")).all()
        return sum(t.monto for t in gastos)

    
    def historial(self):
        return self.session.exec(select(TransactionModel)).all()
        
    def filtrar_por_categoria(self, categoria: Category):
        return self.session.exec(select(TransactionModel).where(TransactionModel.categoria == categoria.value)).all()

    def filtrar_por_fecha(self, fecha: datetime):
        return self.session.exec(select(TransactionModel).where(func.date(TransactionModel.fecha) == fecha.date())).all()

    def filtrar_por_rango(self, desde: datetime, hasta: datetime):
        return self.session.exec(select(TransactionModel).where(TransactionModel.fecha >= desde).where(TransactionModel.fecha <= hasta)).all()

    def filtrar_por_monto(self, minimo=None, maximo=None):
        query = select(TransactionModel)

        if minimo is not None:
            query = query.where(TransactionModel.monto >= minimo)

        if maximo is not None:
            query = query.where(TransactionModel.monto <= maximo)

        return self.session.exec(query).all()


    def ordenar_historial(self, por="fecha", ascendente=True):
        if por not in {"fecha", "monto", "categoria"}:
            raise ValueError("Campo de orden inválido")

        order_col = getattr(TransactionModel, por)

        if not ascendente:
            order_col = order_col.desc()

        return self.session.exec(select(TransactionModel).order_by(order_col)).all()


    def __str__(self):
        return f"Billetera(id={self.id.value})"

    
#en que carpeta va el codigo de la interfaz de terminal
if __name__ == "__main__":
    
    mi_billetera = Billetera.generate()
    mi_billetera.agregar_transaccion(Descripcion("Quincena"),Monto(5000),Tipo(Type.INGRESO),Category.OTROS)
    mi_billetera.agregar_transaccion(Descripcion("compra en supermercado"),Monto(1000),Tipo(Type.GASTO),Category.ALIMENTACION)
    mi_billetera.agregar_transaccion(Descripcion("compra en supermercado"),Monto(1000),Tipo(Type.GASTO),Category.ALIMENTACION)
    mi_billetera.agregar_transaccion(Descripcion("compra en supermercado"),Monto(1000),Tipo(Type.GASTO),Category.ALIMENTACION)
    print(mi_billetera.balance_actual())
    print(mi_billetera.total_gastos())
    print(mi_billetera.total_ingresos())
    mi_billetera.historial()