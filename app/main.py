from fastapi import FastAPI

from app.database import Base, engine

from app.routers import auth
from app.routers import usuario
from app.routers import empresa


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BSM Serviços API"
)


app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(empresa.router)