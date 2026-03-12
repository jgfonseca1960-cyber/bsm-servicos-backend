from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import SessionLocal
from app.models.usuario_model import Usuario
from app.core.security import verificar_senha, criar_token

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

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