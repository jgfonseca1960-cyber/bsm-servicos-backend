from fastapi import FastAPI
from sqlalchemy import text

from app.database import Base, engine

from app.models.usuario_model import Usuario
from app.models.empresa_model import Empresa

from app.routers import auth
from app.routers import usuario
from app.routers import empresa

app = FastAPI()


# RESET BANCO (TEMPORÁRIO)
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS avaliacoes CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS empresas CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS usuarios CASCADE"))
    conn.commit()


Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(empresa.router)