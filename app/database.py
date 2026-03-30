from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os

from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# ✅ FUNÇÃO QUE FALTOU (ESSENCIAL)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    print("Criando banco (SEM apagar dados)...")

    from app.models.usuario_model import Usuario
    from app.models.empresa_model import Empresa
    from app.models.empresa_foto_model import EmpresaFoto
    from app.models.servico_model import Servico
    from app.models.tipo_servico_model import TipoServico

    Base.metadata.create_all(bind=engine)

    print("Banco pronto!")