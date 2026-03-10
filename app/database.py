import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from app.database import engine
from app.models import empresa_model

empresa_model.Base.metadata.drop_all(bind=engine)
empresa_model.Base.metadata.create_all(bind=engine)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()