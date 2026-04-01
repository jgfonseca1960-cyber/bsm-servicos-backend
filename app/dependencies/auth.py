from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import verificar_token

security = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Token não informado")

    token = credentials.credentials

    # 🔥 REMOVE "Bearer " AUTOMATICAMENTE SE VIER JUNTO
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")

    payload = verificar_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")

    return payload


def get_current_admin(user=Depends(get_current_user)):
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Acesso negado")

    return user