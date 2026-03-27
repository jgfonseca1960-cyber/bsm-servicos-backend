from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import DATABASE_URL

# Base dos modelos
Base = declarative_base()

# Engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"}
)

# Sessão
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True
)

# Dependência do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inicialização do banco
def init_db():
    print("🔥 Criando todas as tabelas...")

    import app.models  # importa models

    Base.metadata.create_all(bind=engine)

    print("✅ Todas as tabelas foram criadas!")