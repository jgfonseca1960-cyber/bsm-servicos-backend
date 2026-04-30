from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.models.usuario_model import Usuario
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    usuario = (
        db.query(Usuario)
        .filter(Usuario.email == form_data.username)
        .first()
    )

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    # ⚠️ ajuste conforme seu hash depois
    if usuario.senha_hash != form_data.password:
        raise HTTPException(status_code=401, detail="Senha inválida")

    # 🔥 CONVERSÃO AQUI
    tipo_usuario = "admin" if usuario.is_admin else "usuario"

    access_token = create_access_token(
        data={
            "sub": str(usuario.id),
            "is_admin": usuario.is_admin,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "tipo_usuario": tipo_usuario,  # 🔥 ESSA LINHA RESOLVE TUDO
    }