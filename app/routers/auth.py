from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.database import get_db
from app.models.usuario_model import Usuario
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_senha(senha_plana, senha_hash):
    return pwd_context.verify(senha_plana, senha_hash)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        usuario = (
            db.query(Usuario)
            .filter(Usuario.email == form_data.username)
            .first()
        )

        if not usuario:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        # 🔥 VERIFICA HASH CORRETAMENTE
        if not verificar_senha(form_data.password, usuario.senha_hash):
            raise HTTPException(status_code=401, detail="Senha inválida")

        tipo_usuario = "admin" if usuario.is_admin else "usuario"

        access_token = create_access_token(
            data={
                "sub": str(usuario.id),
                "tipo_usuario": tipo_usuario,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "tipo_usuario": tipo_usuario,
        }

    except Exception as e:
    print("🔥 ERRO REAL LOGIN:", str(e))
    raise HTTPException(status_code=500, detail=str(e))