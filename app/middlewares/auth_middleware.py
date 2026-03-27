from fastapi import Request, HTTPException
from jose import jwt, JWTError
from app.config import SECRET_KEY, ALGORITHM

async def auth_middleware(request: Request, call_next):
    if "Authorization" not in request.headers:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    token = request.headers["Authorization"].split(" ")[1]
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    response = await call_next(request)
    return response