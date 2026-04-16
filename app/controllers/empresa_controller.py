from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.empresa_model import Empresa

router = APIRouter(
    prefix="/empresa",
    tags=["Empresas"]
)

# =========================
# 📌 LISTAR EMPRESAS (ROTA NOVA)
# =========================
@router.get("/empresas", response_model=List[dict])
def listar_empresas(db: Session = Depends(get_db)):
    empresas = db.query(Empresa).all()

    return [
        {
            "id": e.id,
            "nome": e.nome,
            "telefone": e.telefone,
            "email": e.email,
            "endereco": e.endereco,
            "latitude": e.latitude,
            "longitude": e.longitude,
        }
        for e in empresas
    ]


# =========================
# 🔥 ROTA ANTIGA (COMPATIBILIDADE)
# =========================
@router.get("/listar")
def listar_empresas_compat(db: Session = Depends(get_db)):
    return listar_empresas(db)


# =========================
# 🔍 DETALHAR EMPRESA
# =========================
@router.get("/detalhe/{empresa_id}")
def detalhe_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return {
        "id": empresa.id,
        "nome": empresa.nome,
        "telefone": empresa.telefone,
        "email": empresa.email,
        "endereco": empresa.endereco,
        "latitude": empresa.latitude,
        "longitude": empresa.longitude,
    }


# =========================
# ➕ CRIAR EMPRESA
# =========================
@router.post("/")
def criar_empresa(data: dict, db: Session = Depends(get_db)):
    empresa = Empresa(**data)

    db.add(empresa)
    db.commit()
    db.refresh(empresa)

    return {"msg": "Empresa criada com sucesso", "id": empresa.id}


# =========================
# ✏️ ATUALIZAR EMPRESA
# =========================
@router.put("/{empresa_id}")
def atualizar_empresa(empresa_id: int, data: dict, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    for key, value in data.items():
        setattr(empresa, key, value)

    db.commit()
    db.refresh(empresa)

    return {"msg": "Empresa atualizada com sucesso"}


# =========================
# ❌ DELETAR EMPRESA
# =========================
@router.delete("/{empresa_id}")
def deletar_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    db.delete(empresa)
    db.commit()

    return {"msg": "Empresa deletada com sucesso"}