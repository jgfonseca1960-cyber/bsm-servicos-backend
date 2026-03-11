from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.usuario_model import Usuario

from app.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioLogin,
    UsuarioOut,
)

from app.security import (
    hash_senha,
    verificar_senha,
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ REGISTER

@router.post(
    "/register",
    response_model=UsuarioOut
)
def register(
    dados: UsuarioCreate,
    db: Session = Depends(get_db),
):

    usuario = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()

    if usuario:
        raise HTTPException(
            status_code=400,
            detail="Email já existe"
        )

    novo = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha=hash_senha(dados.senha),
        tipo=dados.tipo,
        empresa_id=dados.empresa_id,
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


# ✅ LOGIN

@router.post("/login")
def login(
    dados: UsuarioLogin,
    db: Session = Depends(get_db),
):

    usuario = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=400,
            detail="Usuário não existe"
        )

    if not verificar_senha(
        dados.senha,
        usuario.senha,
    ):
        raise HTTPException(
            status_code=400,
            detail="Senha inválida"
        )

    return {
        "msg": "login ok",
        "usuario": usuario.nome,
        "tipo": usuario.tipo,
    }