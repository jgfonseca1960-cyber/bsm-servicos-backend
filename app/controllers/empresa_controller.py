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
@router.get("/", response_model=List[EmpresaResponse])
def listar_todas_empresas(db: Session = Depends(get_db)):
    return listar_empresas(db)


# =========================
# 🔹 BUSCAR POR ID
# =========================
@router.get("/{empresa_id}", response_model=EmpresaResponse)
def buscar_empresa_por_id(
    empresa_id: int,
    db: Session = Depends(get_db)
):
    return buscar_empresa(db, empresa_id)


# =========================
# 🔥 ATUALIZAR (ADMIN)
# =========================
@router.put("/{empresa_id}", response_model=EmpresaResponse)
def atualizar_empresa_existente(
    empresa_id: int,
    empresa: EmpresaUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return atualizar_empresa(db, empresa_id, empresa)


# =========================
# 🔥 DELETAR (ADMIN)
# =========================
@router.delete("/{empresa_id}")
def deletar_empresa_existente(
    empresa_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return deletar_empresa(db, empresa_id)