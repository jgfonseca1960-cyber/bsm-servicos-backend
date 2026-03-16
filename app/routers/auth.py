from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate

from app.core.security import (
    gerar_hash,
    verificar_senha,
    criar_token,
)

router = APIRouter()


# =========================
# REGISTER
# =========================

@router.post("/register")
def register(
    dados: UsuarioCreate,
    db: Session = Depends(get_db)
):

    user = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()

    if user:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )
    novo = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha=gerar_hash(dados.senha),
        tipo=dados.tipo
)
    
    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


# =========================
# LOGIN OAuth2
# =========================

@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(Usuario).filter(
        Usuario.email == form.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Usuário não encontrado"
        )

    if not verificar_senha(
        form.password,
        user.senha
    ):
        raise HTTPException(
            status_code=400,
            detail="Senha inválida"
        )

    token = criar_token({
        "sub": str(user.id)
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }