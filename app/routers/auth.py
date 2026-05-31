from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel

from app.database import get_db
from app.models.usuario_model import Usuario
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# =========================
# 📦 SCHEMA REGISTER
# =========================
class RegisterRequest(BaseModel):
    nome: str
    email: str
    senha: str


# =========================
# 🔐 HASH
# =========================
def verificar_senha(
    senha_plana,
    senha_hash,
):
    return pwd_context.verify(
        senha_plana,
        senha_hash,
    )


def gerar_hash_senha(
    senha,
):
    return pwd_context.hash(
        senha,
    )


# =========================
# 🆕 REGISTER
# =========================
@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    try:
        usuario_existente = (
            db.query(Usuario)
            .filter(Usuario.email == data.email)
            .first()
        )

        if usuario_existente:
            raise HTTPException(
                status_code=400,
                detail="Email já cadastrado",
            )

        novo_usuario = Usuario(
            nome=data.nome,
            email=data.email,
            senha_hash=gerar_hash_senha(
                data.senha,
            ),
            is_admin=False,
        )

        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        return {
            "message": "Usuário criado com sucesso",
        }

    except HTTPException:
        raise

    except Exception as e:
        print("🔥 ERRO REGISTER:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# =========================
# 🔑 LOGIN
# =========================
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        usuario = (
            db.query(Usuario)
            .filter(
                Usuario.email == form_data.username
            )
            .first()
        )

        if not usuario:
            raise HTTPException(
                status_code=401,
                detail="Usuário não encontrado",
            )

        # 🔥 VERIFICA HASH
        if not verificar_senha(
            form_data.password,
            usuario.senha_hash,
        ):
            raise HTTPException(
                status_code=401,
                detail="Senha inválida",
            )

        tipo_usuario = (
            "admin"
            if usuario.is_admin
            else "usuario"
        )

        access_token = create_access_token(
            data={
                "sub": str(usuario.id),
                "tipo_usuario": tipo_usuario,
            }
        )

        return {
            return {
                
            "access_token": access_token,
            "token_type": "bearer",
            "tipo_usuario": tipo_usuario,
            "usuario_id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
        }
        }

    except HTTPException:
        raise

    except Exception as e:
        print(
            "🔥 ERRO REAL LOGIN:",
            str(e),
        )

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )