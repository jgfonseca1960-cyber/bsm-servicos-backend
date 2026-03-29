from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario_model import Usuario
from app.core.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# 🔹 USUÁRIO LOGADO
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(Usuario).filter(Usuario.id == int(user_id)).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user


# 🔥 ADMIN (AQUI É A REGRA DE NEGÓCIO)
def get_current_admin(user: Usuario = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Acesso restrito a administradores"
        )

    return user