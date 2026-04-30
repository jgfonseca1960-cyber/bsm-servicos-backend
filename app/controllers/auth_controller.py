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
    try:
        # 🔥 BUSCA USUÁRIO
        usuario = (
            db.query(Usuario)
            .filter(Usuario.email == form_data.username)
            .first()
        )

        # ❌ NÃO EXISTE
        if not usuario:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        # 🔐 VALIDA SENHA (SIMPLES POR ENQUANTO)
        if usuario.senha_hash != form_data.password:
            raise HTTPException(status_code=401, detail="Senha inválida")

        # 🔥 DEFINE TIPO
        tipo_usuario = "admin" if usuario.is_admin else "usuario"

        # 🔥 GERA TOKEN
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
        print("🔥 ERRO LOGIN:", e)
        raise HTTPException(status_code=500, detail=str(e))