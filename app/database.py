from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# Dependency do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🚀 Função para criar tabelas
def init_db():
    from app.models.usuario_model import Usuario
    from app.models.empresa_model import Empresa
    from app.models.empresa_foto_model import EmpresaFoto
    from app.models.servico_model import Servico

    Base.metadata.create_all(bind=engine)
    
    print("✅ Banco recriado!")