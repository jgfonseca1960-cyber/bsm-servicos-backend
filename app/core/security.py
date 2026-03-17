from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "segredo"
ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def gerar_hash(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(
    senha,
    hash
):
    return pwd_context.verify(
        senha,
        hash
    )


def criar_token(data: dict):

    dados = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=60 * 24
    )

    dados.update(
        {"exp": expire}
    )

    return jwt.encode(
        dados,
        SECRET_KEY,
        algorithm=ALGORITHM
    )