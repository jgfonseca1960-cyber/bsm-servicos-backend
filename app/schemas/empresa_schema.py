from pydantic import BaseModel
from typing import Optional


# =========================
# 🔹 BASE
# =========================
class EmpresaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    telefone: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ativo: Optional[bool] = True


# =========================
# 🔹 CREATE
# =========================
class EmpresaCreate(EmpresaBase):
    servico_id: int


# =========================
# 🔹 UPDATE
# =========================
class EmpresaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    telefone: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ativo: Optional[bool] = None
    servico_id: Optional[int] = None


# =========================
# 🔹 RESPONSE (CORRIGIDO)
# =========================
class EmpresaResponse(EmpresaBase):
    id: int
    servico_id: Optional[int] = None

    class Config:
        from_attributes = True