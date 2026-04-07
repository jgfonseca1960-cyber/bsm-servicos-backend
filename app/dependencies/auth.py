from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario_model import Usuario
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ✅ USUÁRIO LOGADO
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(Usuario).filter(Usuario.id == int(user_id)).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user


# ✅ ADMIN (ESSA FUNÇÃO É O QUE ESTÁ FALTANDO!)
def get_current_admin(
    user: Usuario = Depends(get_current_user)
):
    # evita erro se campo não existir
    if not hasattr(user, "is_admin") or not user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado")

    return user