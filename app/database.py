import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://neondb_owner:npg_j5ogriF7NlLZ@ep-shy-fog-ac45dkha-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
# os.getenv("DATABASE_URL")
print("DATABASE_URL =", DATABASE_URL)
engine = create_engine(
    DATABASE_URL,
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
    Base.metadata.create_all(bind=engine)