from fastapi import FastAPI

from app.database import Base, engine

from app.routers import auth, empresa, usuario


app = FastAPI()


@app.on_event("startup")
def start_db():

    try:
        Base.metadata.create_all(bind=engine)
        print("DB OK")

    except Exception as e:
        print("ERRO DB", e)


app.include_router(auth.router, prefix="/auth")
app.include_router(empresa.router, prefix="/empresas")
app.include_router(usuario.router)