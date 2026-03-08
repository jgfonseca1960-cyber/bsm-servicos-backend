from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate
from app.core.security import get_password_hash, verificar_senha, criar_token

router = APIRouter(prefix="/auth", tags=["Auth"])


# conexão banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# REGISTER
@router.post("/register")
def register(user: UsuarioCreate, db: Session = Depends(get_db)):

    usuario_existente = db.query(Usuario).filter(Usuario.email == user.email).first()

    if usuario_existente:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    senha_hash = get_password_hash(user.password)

    novo_usuario = Usuario(
        email=user.email,
        password=senha_hash
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return {
        "msg": "Usuário criado com sucesso",
        "id": novo_usuario.id
    }


# LOGIN
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")

    if not verificar_senha(form_data.password, usuario.password):
        raise HTTPException(status_code=400, detail="Senha inválida")

    token = criar_token({"sub": usuario.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }