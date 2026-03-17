from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext


SECRET_KEY = "segredo123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =========================
# HASH SENHA
# =========================

def gerar_hash(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(
    senha: str,
    hash_senha: str
):
    return pwd_context.verify(
        senha,
        hash_senha
    )


# =========================
# TOKEN
# =========================

def criar_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# ✅ ESTA FUNÇÃO ESTAVA FALTANDO
def verificar_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        return int(user_id)

    except JWTError:

        return None