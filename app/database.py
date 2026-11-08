
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import DATABASE_URL


# Define explicitamente o driver psycopg2.
# Isso evita que o SQLAlchemy 2.1 tente importar psycopg (versão 3).
def normalizar_database_url(url: str) -> str:
    if url.startswith("postgresql://"):
        return url.replace(
            "postgresql://",
            "postgresql+psycopg2://",
            1,
        )

    if url.startswith("postgres://"):
        return url.replace(
            "postgres://",
            "postgresql+psycopg2://",
            1,
        )

    return url


DATABASE_URL_FINAL = normalizar_database_url(DATABASE_URL)


engine = create_engine(
    DATABASE_URL_FINAL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    # Registra todos os modelos antes de criar/verificar as tabelas.
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
