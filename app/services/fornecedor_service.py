from sqlalchemy.orm import Session
from app.models.fornecedor import Fornecedor

def criar_fornecedor(db: Session, dados):
    fornecedor = Fornecedor(**dados.dict())
    db.add(fornecedor)
    db.commit()
    db.refresh(fornecedor)
    return fornecedor

def listar_fornecedores(db: Session):
    return db.query(Fornecedor).all()

def deletar_fornecedor(db: Session, id: int):
    fornecedor = db.query(Fornecedor).filter(
        Fornecedor.id == id
    ).first()

    db.delete(fornecedor)
    db.commit()