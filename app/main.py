from fastapi import FastAPI

from app.database import Base, engine

# IMPORTAR MODELS (OBRIGATÓRIO)
from app.models.usuario_model import Usuario
from app.models.empresa_model import Empresa


Empresa.__table__.drop(bind=engine, checkfirst=True)
Base.metadata.create_all(bind=engine)


# IMPORTAR ROUTERS
from app.routers import auth
from app.routers import usuario
from app.routers import empresa

app = FastAPI()


# criar tabelas
Base.metadata.create_all(bind=engine)


# rotas
app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(empresa.router)