from fastapi import FastAPI

from app.database import Base, engine

from app.models import usuario_model
from app.models import empresa_model

from app.routers.auth import router as auth_router
from app.routers.usuario import router as usuario_router
from app.routers.empresa import router as empresa_router
from app.routers.avaliacao import router as avaliacao_router


app = FastAPI(
    title="BSM API"
)


# criar tabelas
Base.metadata.create_all(bind=engine)


# routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

app.include_router(usuario_router, prefix="/usuarios", tags=["Usuarios"])

app.include_router(empresa_router, prefix="/empresas", tags=["Empresas"])

app.include_router(avaliacao_router, prefix="/avaliacoes", tags=["Avaliacoes"])