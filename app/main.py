from fastapi import FastAPI

from app.routers import auth
from app.routers import empresa
from app.routers import avaliacao
from app.routers import usuario


app = FastAPI()


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(usuario.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(empresa.router, prefix="/empresas", tags=["Empresas"])
app.include_router(avaliacao.router, prefix="/avaliacoes", tags=["Avaliacoes"])