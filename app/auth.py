from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "segredo123"
ALGORITHM = "HS256"
EXPIRA_MIN = 60 * 24


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