from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.fornecedor_model import Fornecedor
from app.schemas.fornecedor_schema import FornecedorCreate, FornecedorResponse
from typing import List
from fastapi import Depends
from app.core.deps import oauth2_scheme

router = APIRouter(prefix="/fornecedores", tags=["Fornecedores"])

# Dependência do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE
@router.post("/", response_model=FornecedorResponse)
def criar_fornecedor(fornecedor: FornecedorCreate, db: Session = Depends(get_db)):
    novo = Fornecedor(**fornecedor.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


# READ ALL
@router.get("/")
def listar_fornecedores(token: str = Depends(oauth2_scheme)):
    return {"msg": "Token recebido", "token": token}

# READ BY ID
@router.get("/{fornecedor_id}", response_model=FornecedorResponse)
def buscar_fornecedor(fornecedor_id: int, db: Session = Depends(get_db)):
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return fornecedor


# UPDATE
@router.put("/{fornecedor_id}", response_model=FornecedorResponse)
def atualizar_fornecedor(fornecedor_id: int, dados: FornecedorCreate, db: Session = Depends(get_db)):
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")

    for key, value in dados.dict().items():
        setattr(fornecedor, key, value)

    db.commit()
    db.refresh(fornecedor)
    return fornecedor


# DELETE
@router.delete("/{fornecedor_id}")
def deletar_fornecedor(fornecedor_id: int, db: Session = Depends(get_db)):
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")

    db.delete(fornecedor)
    db.commit()
    return {"mensagem": "Fornecedor deletado com sucesso"}