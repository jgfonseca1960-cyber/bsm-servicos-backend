from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models.usuario_model import Usuario
from app.core.security import criar_token

router = APIRouter(tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == email).first()

    if not user or not pwd_context.verify(senha, user.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }