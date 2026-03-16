from fastapi import FastAPI
from app.database import Base, engine

from app.routers import auth, usuario, empresa, avaliacao

app = FastAPI(title="BSM API")


@app.on_event("startup")
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/auth")
app.include_router(usuario.router)
app.include_router(empresa.router, prefix="/empresas")
app.include_router(avaliacao.router, prefix="/avaliacoes")