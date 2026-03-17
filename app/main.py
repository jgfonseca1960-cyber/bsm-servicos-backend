from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth, empresa, usuario


app = FastAPI()


@app.on_event("startup")
def start_db():

    print("CRIANDO TABELAS")

    Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/auth")
app.include_router(empresa.router, prefix="/empresas")
app.include_router(usuario.router)