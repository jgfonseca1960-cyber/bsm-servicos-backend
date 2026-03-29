from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
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
    print("Recriando banco...")

    from app.models.usuario_model import Usuario
    from app.models.empresa_model import Empresa
    from app.models.empresa_foto_model import EmpresaFoto
    from app.models.servico_model import Servico
    from app.models.tipo_servico_model import TipoServico

    # 💥 reset total (dev)
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.commit()

    Base.metadata.create_all(bind=engine)

    print("Banco recriado do ZERO!")