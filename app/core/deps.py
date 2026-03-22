from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

# ✅ cria o esquema do token para Swagger

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# ✅ função que pega usuário do token

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    if not token:

        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    # depois vamos validar JWT de verdade
    return {"id": 1}