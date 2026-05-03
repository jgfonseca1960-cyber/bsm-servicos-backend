from pydantic import BaseModel
from typing import Optional, List


# =========================
# 🔹 FOTO
# =========================
class FotoResponse(BaseModel):
    id: int
    url: str
    principal: bool

    class Config:
        from_attributes = True


# =========================
# 🔹 BASE COMPLETA
# =========================
class EmpresaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    telefone: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None

    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    ativo: Optional[bool] = True
    avaliacao_media: Optional[float] = None

    cpf: Optional[str] = None
    cnpj: Optional[str] = None


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
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    ativo: Optional[bool] = None
    avaliacao_media: Optional[float] = None

    cpf: Optional[str] = None
    cnpj: Optional[str] = None

    servico_id: Optional[int] = None


# =========================
# 🔹 RESPONSE COMPLETA
# =========================
class EmpresaResponse(EmpresaBase):
    id: int
    servico_id: Optional[int] = None

    foto_principal: Optional[str] = None
    fotos: List[FotoResponse] = []

    distancia_km: Optional[float] = None

    class Config:
        from_attributes = True