from fastapi import FastAPI

from app.database import Base, engine

# ✅ IMPORTAR MODELS (OBRIGATÓRIO)
from app.models.usuario_model import Usuario
from app.models.empresa_model import Empresa

from app.routers import auth
from app.routers import usuario
from app.routers import empresa


# ✅ RESET DO BANCO
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="BSM Serviços API"
)

app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(empresa.router)