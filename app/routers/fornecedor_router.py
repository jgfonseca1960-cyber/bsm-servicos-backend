from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.fornecedor import Fornecedor
from app.schemas.fornecedor_schema import FornecedorCreate, FornecedorResponse
from typing import List

router = APIRouter(prefix="/fornecedores", tags=["Fornecedores"])

# Dependência de banco
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

# READ (listar todos)
@router.get("/", response_model=List[FornecedorResponse])
def listar_fornecedores(db: Session = Depends(get_db)):
    return db.query(Fornecedor).all()

# READ (buscar por id)
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

    fornecedor.nome_empresa = dados.nome_empresa
    fornecedor.telefone = dados.telefone
    fornecedor.cidade = dados.cidade

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
    return {"mensagem": "Fornecedor removido com sucesso"}