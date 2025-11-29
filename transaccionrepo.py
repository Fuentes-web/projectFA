from sqlmodel import Session, select
from dbmodels import TransactionDB
from main import Transaction

class TransactionRepository:

    def save(self, session:Session, tx:Transaction):
        tx_db = TransactionDB(
            id=tx.id,
            descripcion=str(tx.descripcion),
            monto=tx.monto.value,
            tipo=tx.tipo,
            categoria=tx.categoria.value,
            fecha=tx.fecha
        )
        session.add(tx_db)
        session.commit()
        session.refresh(tx_db)
        return tx_db

    def get_all(self, session:Session):
        return session.exec(select(TransactionDB)).all()
