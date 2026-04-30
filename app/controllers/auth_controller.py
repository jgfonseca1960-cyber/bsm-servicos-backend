from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.database import get_db
from app.models.usuario_model import Usuario
from app.core.security import create_access_token

router = APIRouter(tags=["Auth"])

# 🔐 CONTEXTO DE CRIPTOGRAFIA
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    try:
        # 🔥 Se for hash (bcrypt)
        if senha_hash.startswith("$2b$"):
            return pwd_context.verify(senha_plana, senha_hash)

        # 🔥 Fallback (senha simples - legado)
        return senha_plana == senha_hash

    except Exception as e:
        print("🔥 ERRO VERIFICAR SENHA:", e)
        return False


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        # 🔍 BUSCA USUÁRIO
        usuario = (
            db.query(Usuario)
            .filter(Usuario.email == form_data.username)
            .first()
        )

        # ❌ USUÁRIO NÃO EXISTE
        if not usuario:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        # 🔐 VALIDA SENHA (HASH + LEGADO)
        if not verificar_senha(form_data.password, usuario.senha_hash):
            raise HTTPException(status_code=401, detail="Senha inválida")

        # 👤 DEFINE TIPO
        tipo_usuario = "admin" if usuario.is_admin else "usuario"

        # 🔑 GERA TOKEN
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

    except HTTPException:
        raise

    except Exception as e:
        print("🔥 ERRO LOGIN:", e)
        raise HTTPException(status_code=500, detail="Erro interno no servidor")