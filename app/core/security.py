from passlib.context import CryptContext
from jose import jwt
import os

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET = os.getenv("SECRET_KEY", "123")


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

    return jwt.encode(
        data,
        SECRET,
        algorithm="HS256"
    )