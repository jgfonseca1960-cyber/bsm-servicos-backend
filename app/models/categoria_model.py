from sqlalchemy import Column, Integer, String
from app.database import Base


class Categoria(Base):

    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, unique=True, index=True)