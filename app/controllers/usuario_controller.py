from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.services.usuario_service import (
    criar_usuario,
    listar_usuarios,
    get_usuario_por_id,
    atualizar_usuario,
    deletar_usuario
)

from app.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate
)

# 🔥 SEM PREFIX AQUI
router = APIRouter(
    tags=["Usuários"]
)


# 🔹 CRIAR USUÁRIO
@router.post("/", response_model=UsuarioResponse)
def criar_novo_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return criar_usuario(db, usuario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


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


# 🔹 ATUALIZAR
@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario_existente(
    usuario_id: int,
    usuario: UsuarioUpdate,
    db: Session = Depends(get_db)
):
    try:
        updated = atualizar_usuario(db, usuario_id, usuario)

        if not updated:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        return updated

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar: {str(e)}")


# 🔹 DELETAR
@router.delete("/{usuario_id}", response_model=UsuarioResponse)
def deletar_usuario_existente(usuario_id: int, db: Session = Depends(get_db)):
    try:
        deleted = deletar_usuario(db, usuario_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        return deleted

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar: {str(e)}")