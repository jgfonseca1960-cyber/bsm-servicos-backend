from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UsuarioCreate, UsuarioResponse
from app.services import usuario_service

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return usuario_service.criar_usuario(db, usuario)

@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return usuario_service.listar_usuarios(db)

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def get_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = usuario_service.get_usuario_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    updated = usuario_service.atualizar_usuario(db, usuario_id, usuario)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return updated

@router.delete("/{usuario_id}", response_model=UsuarioResponse)
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    deleted = usuario_service.deletar_usuario(db, usuario_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return deleted