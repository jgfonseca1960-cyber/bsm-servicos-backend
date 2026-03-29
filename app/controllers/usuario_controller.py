from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

# ✅ IMPORT DIRETO (evita erro de __init__)
from app.services.usuario_service import (
    criar_usuario,
    listar_usuarios,
    get_usuario_por_id,
    atualizar_usuario,
    deletar_usuario
)

# ✅ Schemas
from app.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate
)

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


# 🔹 CRIAR USUÁRIO
@router.post("/", response_model=UsuarioResponse)
def criar_novo_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return criar_usuario(db, usuario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 🔹 LISTAR TODOS
@router.get("/", response_model=list[UsuarioResponse])
def listar_todos_usuarios(db: Session = Depends(get_db)):
    return listar_usuarios(db)


# 🔹 BUSCAR POR ID
@router.get("/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = get_usuario_por_id(db, usuario_id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario


# 🔹 ATUALIZAR (CORRIGIDO COM UsuarioUpdate)
@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario_existente(
    usuario_id: int,
    usuario: UsuarioUpdate,
    db: Session = Depends(get_db)
):
    updated = atualizar_usuario(db, usuario_id, usuario)

    if not updated:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return updated


# 🔹 DELETAR
@router.delete("/{usuario_id}", response_model=UsuarioResponse)
def deletar_usuario_existente(usuario_id: int, db: Session = Depends(get_db)):
    deleted = deletar_usuario(db, usuario_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return deleted