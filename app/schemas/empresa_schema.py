from pydantic import BaseModel
from typing import Optional


# 🔹 BASE
class EmpresaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None


# 🔹 CREATE
class EmpresaCreate(EmpresaBase):
    pass


# 🔹 RESPONSE
class EmpresaResponse(EmpresaBase):
    id: int

    class Config:
        from_attributes = True