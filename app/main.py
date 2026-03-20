from fastapi import FastAPI
from sqlalchemy import text
import os

from app.database import Base, engine

from app.models.usuario_model import Usuario
from app.models.empresa_model import Empresa

from app.routers import auth
from app.routers import usuario
from app.routers import empresa

app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(empresa.router)


# ✅ DEBUG BANCO

@app.get("/debug/database")
def debug_database():

    return {
        "DATABASE_URL": os.getenv("DATABASE_URL")
    }


@app.get("/debug/usuarios")
def debug_usuarios():

    with engine.connect() as conn:

        result = conn.execute(text("SELECT * FROM usuarios"))

        return [dict(row._mapping) for row in result]