from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.empresa_model import Empresa

# 🔹 SERVICE
from app.services.empresa_service import (
    criar_empresa,
    listar_empresas,
    buscar_empresa,
    atualizar_empresa,
    deletar_empresa
)

# 🔹 SCHEMAS
from app.schemas.empresa_schema import (
    EmpresaCreate,
    EmpresaResponse,
    EmpresaUpdate
)

# 🔥 AUTH
from app.dependencies.auth import get_current_admin

router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"]
)


# =========================
# 🔥 CRIAR (ADMIN)
# =========================
@router.post("/", response_model=EmpresaResponse)
def criar_nova_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return criar_empresa(db, empresa)


# =========================
# 🔹 LISTAR (PÚBLICO)
# =========================

@router.get("/")
def listar_todas_empresas(db: Session = Depends(get_db)):
    try:
        return db.query(Empresa).all()
    except Exception as e:
        print("ERRO LISTAR:", str(e))
        raise

# =========================
# 🔹 BUSCAR POR ID
# =========================
@router.get("/{empresa_id}", response_model=EmpresaResponse)

from fastapi import HTTPException

def buscar_empresa(db, empresa_id: int):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail=f"Empresa com id {empresa_id} não encontrada"
        )

    return empresa

# =========================
# 🔥 ATUALIZAR (ADMIN)
# =========================
@router.put("/{empresa_id}", response_model=EmpresaResponse)
def atualizar_empresa(db, empresa_id: int, dados):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail=f"Empresa com id {empresa_id} não encontrada"
        )

    for key, value in dados.dict(exclude_unset=True).items():
        setattr(empresa, key, value)

    db.commit()
    db.refresh(empresa)

    return empresa

# =========================
# 🔥 DELETAR (ADMIN)
# =========================
@router.delete("/{empresa_id}")
def deletar_empresa(db, empresa_id: int):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail=f"Empresa com id {empresa_id} não encontrada"
        )

    db.delete(empresa)
    db.commit()

    return {
        "message": f"Empresa {empresa_id} deletada com sucesso"
    }