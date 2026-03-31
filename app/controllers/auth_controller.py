from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models.usuario_model import Usuario
from pydantic import BaseModel

# 🔥 JWT
from app.core.security import criar_token

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginRequest(BaseModel):
    email: str
    senha: str


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == data.email).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not pwd_context.verify(data.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Senha inválida")

    # 🔥 AQUI ESTÁ O JWT (ANTES NÃO TINHA)
    token = criar_token({
        "sub": str(usuario.id),
        "is_admin": usuario.is_admin
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }