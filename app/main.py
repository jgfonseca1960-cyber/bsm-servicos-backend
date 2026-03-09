from fastapi import FastAPI

from app.database import engine, Base

import app.models.usuario_model
import app.models.empresa_model
import app.models.avaliacao_model

from app.routers import auth, empresa, avaliacao


app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(empresa.router)
app.include_router(avaliacao.router)

# @app.get("/")
# def root():
#    return {"status": "API funcionando"}