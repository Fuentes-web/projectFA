from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid

class Type(str, Enum):
    INGRESO = "Ingreso"
    GASTO = "Gasto"

class Category(str, Enum):
    ALIMENTACION = "Alimentación"
    HOGAR = "Hogar"
    TRANSPORTE = "Transporte"
    ENTRETENIMIENTO = "Entretenimiento"
    SALUD = "Salud"
    OTROS = "Otros"
    TRABAJO = "Trabajo"
    EDUCACION = "Educación"

# Modelo que usa la base de datos
class TransactionModel(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    descripcion: Optional[str] = None
    monto: float
    tipo: Type
    categoria: Category
    fecha: datetime = Field(default_factory=datetime.utcnow)

# Modelo para que el usuario cree una transacción
class TransactionCreate(SQLModel):
    descripcion: Optional[str] = None
    monto: float
    tipo: Type
    categoria: Category

# Usuario
class UserModel(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    username: str = Field(unique=True, index=True)
    password_hash: str
