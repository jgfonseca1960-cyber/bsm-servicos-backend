from fastapi import FastAPI

from app.database import Base, engine

from app.models import usuario_model
from app.models import empresa_model

from app.routers import auth
from app.routers import empresa
from app.routers import usuario
from app.routers import avaliacao

from app.routers import usuarios

app.include_router(usuarios.router)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="BSM API"
)


app.include_router(auth.router, prefix="/auth", tags=["Auth"])

app.include_router(usuario.router, prefix="/usuarios", tags=["Usuarios"])

app.include_router(empresa.router, prefix="/empresas", tags=["Empresas"])

app.include_router(avaliacao.router, prefix="/avaliacoes", tags=["Avaliacoes"])