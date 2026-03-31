from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models.usuario_model import Usuario

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not pwd_context.verify(senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Senha inválida")

    return {
        "msg": "Login realizado com sucesso",
        "usuario_id": usuario.id,
        "is_admin": usuario.is_admin
    }