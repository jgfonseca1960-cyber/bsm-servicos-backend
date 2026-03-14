from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioLogin
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from app.core.security import gerar_hash, verificar_senha, criar_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

router = APIRouter()

SECRET_KEY = "segredo123"
ALGORITHM = "HS256"
EXPIRA_MIN = 60 * 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def criar_token(data: dict):
    dados = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=EXPIRA_MIN
    )

    dados.update({"exp": expire})

    token = jwt.encode(
        dados,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


@router.post("/register")
def register(
    dados: UsuarioCreate,
    db: Session = Depends(get_db)
):

    novo = Usuario(
    nome=dados.nome,
    email=dados.email,
    senha=gerar_hash(dados.senha)
)
    
    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo

@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(Usuario).filter(
        Usuario.email == form.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Usuário não encontrado"
        )

    if not verificar_senha(
        form.password,
        user.senha
    ):
        raise HTTPException(
            status_code=400,
            detail="Senha inválida"
        )

    token = criar_token({
        "sub": str(user.id)
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }