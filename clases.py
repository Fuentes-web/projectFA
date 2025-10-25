from datetime import date, datetime
from abc import ABC, abstractmethod
from enum import Enum
import uuid

class Type(str,Enum):
    INGRESO = "Ingreso"
    GASTO = "Gasto"
    
class Category(str,Enum):
    ALIMENTACION = "Alimentación"
    HOGAR = "Hogar"
    TRANSPORTE = "Transporte"
    ENTRETENIMIENTO = "Entretenimiento"
    SALUD = "Salud"
    OTROS = "Otros"
    TRABAJO = "Trabajo"
    EDUCACION = "Educación"
    
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
    
    def __init__(self,id:Id, transacciones:dict[Id,Transaction]):
        self.id = id
        self.transacciones = transacciones
    
    @classmethod
    def generate(cls):
        id = Id.generate()
        return cls(id,dict())
            
    def agregar_transaccion(self,descripcion:Descripcion, monto:Monto, tipo:Tipo, categoria:Category):
        transaccion = Transaction.generate(descripcion, monto, tipo, categoria)
        self._validar_transaccion(transaccion,Accion.AGREGAR)
        self.transacciones[transaccion.id] = transaccion
        
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
              
    def eliminar_transaccion(self,id_transaccion):
        if id_transaccion not in self.transacciones:
            raise ValueError("llave incorrecta o no disponible")
        else:
            self._validar_transaccion(self.transacciones[id_transaccion],Accion.ELIMINAR)
            del self.transacciones[id_transaccion]  
    
    def _calcular_balance(self):
        balance = 0
        for transaccion in self.transacciones.values():
            balance += transaccion
        return balance
            
    def balance_actual(self):
        return self._calcular_balance()
    
    def total_ingresos(self):
        total_ingresos = 0
        for transaccion in self.transacciones.values():
            if transaccion.tipo == Type.INGRESO:
                total_ingresos+=transaccion.monto.value
        return total_ingresos
    
    def total_gastos(self):
        total_gastos = 0
        for transaccion in self.transacciones.values():
            if transaccion.tipo == Type.GASTO:
                total_gastos+=transaccion.monto.value
        return total_gastos
    
    def historial(self):
        for transaccion in self.transacciones.values():
            print(self.transacciones[transaccion.id])
        
    def __str__(self):
        return f"Billetera(transacciones={self.transacciones})"
    
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