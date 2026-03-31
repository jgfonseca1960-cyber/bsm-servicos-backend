from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db

# 🔹 SERVICE
from app.services.empresa_service import (
    criar_empresa,
    listar_empresas,
    get_empresa_por_id,
    atualizar_empresa,
    deletar_empresa
)

# 🔹 SCHEMAS
from app.schemas.empresa_schema import (
    EmpresaCreate,
    EmpresaResponse,
    EmpresaUpdate
)

# 🔥 AUTH (JWT + ADMIN)

from app.dependencies.auth import get_current_admin

router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"]
)


# 🔥 CRIAR EMPRESA (SOMENTE ADMIN)
@router.post("/", response_model=EmpresaResponse)
def criar_nova_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    return criar_empresa(db, empresa)


# 🔹 LISTAR TODAS (PÚBLICO)
@router.get("/", response_model=List[EmpresaResponse])
def listar_todas_empresas(db: Session = Depends(get_db)):
    return listar_empresas(db)


# 🔹 BUSCAR POR ID
@router.get("/{empresa_id}", response_model=EmpresaResponse)
def buscar_empresa(
    empresa_id: int,
    db: Session = Depends(get_db)
):
    empresa = get_empresa_por_id(db, empresa_id)

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return empresa


# 🔥 ATUALIZAR (SOMENTE ADMIN)
@router.put("/{empresa_id}", response_model=EmpresaResponse)
def atualizar_empresa_existente(
    empresa_id: int,
    empresa: EmpresaUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    updated = atualizar_empresa(db, empresa_id, empresa)

    if not updated:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return updated


# 🔥 DELETAR (SOMENTE ADMIN)
@router.delete("/{empresa_id}", response_model=EmpresaResponse)
def deletar_empresa_existente(
    empresa_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    deleted = deletar_empresa(db, empresa_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return deleted