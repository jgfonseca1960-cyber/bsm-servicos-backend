from fastapi import FastAPI

from app.database import engine, Base

import app.models.usuario_model
import app.models.empresa_model
import app.models.avaliacao_model

from app import models

from app.routers import auth, empresa, avaliacao


app = FastAPI()


@app.on_event("startup")
def startup():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(empresa.router)
app.include_router(avaliacao.router)

# @app.get("/")
# def root():
#    return {"status": "API funcionando"}