from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.usuario_model import Usuario
from app.core.security import verificar_senha, criar_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# 🔥 MODELO PARA RECEBER JSON (ESSENCIAL)
class LoginRequest(BaseModel):
    email: str
    senha: str


@router.post("/login")
def login(
    dados: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    # 🔥 IMPORTANTE: usar senha_hash (não senha)
    if not verificar_senha(
        dados.senha,
        user.senha_hash
    ):
        raise HTTPException(status_code=401, detail="Senha inválida")

    token = criar_token(
        {
            "sub": str(user.id),
            "is_admin": getattr(user, "is_admin", False)
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }