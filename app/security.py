from passlib.context import CryptContext

user_id = payload.get("sub")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_senha(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(
    senha: str,
    senha_hash: str
):
    return pwd_context.verify(
        senha,
        senha_hash
    )