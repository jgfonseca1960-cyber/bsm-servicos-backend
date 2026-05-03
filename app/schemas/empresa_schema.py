from pydantic import BaseModel
from typing import Optional, List


# =========================
# 🔹 FOTO RESPONSE
# =========================
class FotoResponse(BaseModel):
    id: int
    url: str
    principal: bool

    class Config:
        from_attributes = True


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
    bairro: Optional[str] = None  # 🔥 ADICIONADO
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
    bairro: Optional[str] = None  # 🔥 ADICIONADO
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    ativo: Optional[bool] = None
    servico_id: Optional[int] = None


# =========================
# 🔹 RESPONSE COMPLETO
# =========================
class EmpresaResponse(EmpresaBase):
    id: int
    servico_id: Optional[int] = None

    # 🔥 CAMPOS QUE ESTAVAM SUMINDO
    foto_principal: Optional[str] = None
    fotos: List[FotoResponse] = []

    avaliacao_media: Optional[float] = 0
    distancia_km: Optional[float] = None

    class Config:
        from_attributes = True