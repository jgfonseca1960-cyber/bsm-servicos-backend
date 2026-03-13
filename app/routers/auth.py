from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from app.core.security import gerar_hash, verificar_senha, criar_token
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import APIRouter

router = APIRouter()

@router.post("/register")
def register():
    
    existe = db.query(Usuario).filter(
        Usuario.email == usuario.email
    ).first()

    if existe:
        raise HTTPException(400, "Email já cadastrado")

    novo = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=gerar_hash(usuario.senha),
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo

@router.post("/login")
def login():


    usuario = db.query(Usuario).filter(
        Usuario.email == form_data.username
    ).first()

    if not usuario:
        raise HTTPException(400, "Usuário não encontrado")

    if not verificar_senha(form_data.password, usuario.senha):
        raise HTTPException(400, "Senha inválida")

    token = criar_token(
        {"sub": str(usuario.id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }