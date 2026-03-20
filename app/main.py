from fastapi import FastAPI

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

from sqlalchemy import text
from app.database import engine


@app.get("/debug/usuarios")
def debug_usuarios():

    with engine.connect() as conn:

        result = conn.execute(text("SELECT * FROM usuarios"))

        return [dict(row._mapping) for row in result]