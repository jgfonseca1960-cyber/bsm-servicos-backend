from fastapi import FastAPI
from app.database import engine, Base

from app.models import usuario_model
from app.models import empresa_model
from app.models import avaliacao_model
from app.models.usuario import Usuario
from app.models.empresa import Empresa

from app.routers import auth, empresa, avaliacao


app = FastAPI()
Base.metadata.create_all(bind=engine)

# Rotas
app.include_router(auth.router)
app.include_router(empresa.router)
app.include_router(avaliacao.router)

@app.get("/")
def root():
    return {"status": "API funcionando"}