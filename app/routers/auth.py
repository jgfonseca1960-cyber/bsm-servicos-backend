from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario_model import Usuario

from app.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioLogin,
    UsuarioResponse
)

from app.auth import criar_token


router = APIRouter()


# =========================
# REGISTER
# =========================

@router.post("/register", response_model=UsuarioResponse)
def register(
    dados: UsuarioCreate,
    db: Session = Depends(get_db)
):

    existe = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )

    novo = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha=dados.senha,
        tipo="admin"
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


# =========================
# LOGIN
# =========================

@router.post("/login")
def login(
    dados: UsuarioLogin,
    db: Session = Depends(get_db)
):

    usuario = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    if usuario.senha != dados.senha:
        raise HTTPException(
            status_code=401,
            detail="Senha inválida"
        )

    token = criar_token(
        {"user_id": usuario.id}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }