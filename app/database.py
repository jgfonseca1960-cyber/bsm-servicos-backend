from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def init_db():
    print("Recriando banco...")

    # IMPORTAR MODELOS
    from app.models.usuario_model import Usuario
    from app.models.empresa_model import Empresa
    from app.models.empresa_foto_model import EmpresaFoto
    from app.models.servico_model import Servico
    from app.models.tipo_servico_model import TipoServico

    # 💥 RESET TOTAL DO BANCO (resolve erro de dependência)
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.commit()

    # 🔥 recria todas as tabelas
    Base.metadata.create_all(bind=engine)

    print("Banco recriado do ZERO!")