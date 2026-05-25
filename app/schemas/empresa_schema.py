from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List

from app.schemas.avaliacao_schema import AvaliacaoResponse

# =====================================================
# 🔹 FOTO CREATE
# =====================================================

class EmpresaFotoCreate(BaseModel):
    empresa_id: int

    url: str

    principal: Optional[bool] = False

    public_id: Optional[str] = None


# =====================================================
# 🔹 FOTO RESPONSE
# =====================================================

class FotoResponse(BaseModel):
    id: int

    url: str

    principal: bool

    public_id: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# =====================================================
# 🔹 BASE
# =====================================================

class EmpresaBase(BaseModel):

    # =========================================
    # DADOS BÁSICOS
    # =========================================

    nome: str

    descricao: Optional[str] = None

    telefone: Optional[str] = None

    whatsapp: Optional[str] = None

    email: Optional[str] = None

    # =========================================
    # ENDEREÇO
    # =========================================

    endereco: Optional[str] = None

    bairro: Optional[str] = None

    cidade: Optional[str] = None

    estado: Optional[str] = None

    cep: Optional[str] = None

    # =========================================
    # GEOLOCALIZAÇÃO
    # =========================================

    latitude: Optional[float] = None

    longitude: Optional[float] = None

    # =========================================
    # STATUS
    # =========================================

    ativo: Optional[bool] = True

    avaliacao_media: Optional[float] = 0.0

    # =========================================
    # DOCUMENTOS
    # =========================================

    cpf: Optional[str] = None

    cnpj: Optional[str] = None

    # =========================================
    # ⭐ PREMIUM / MONETIZAÇÃO
    # =========================================

    premium: Optional[bool] = False

    destaque: Optional[bool] = False

    plano: Optional[str] = "gratuito"

    prioridade: Optional[int] = 0

    whatsapp_destacado: Optional[bool] = False

    exibir_no_topo: Optional[bool] = False

    selo_premium: Optional[bool] = False


# =====================================================
# 🔹 CREATE
# =====================================================

class EmpresaCreate(EmpresaBase):

    servico_id: int


# =====================================================
# 🔹 UPDATE
# =====================================================

class EmpresaUpdate(BaseModel):

    # =========================================
    # DADOS BÁSICOS
    # =========================================

    nome: Optional[str] = None

    descricao: Optional[str] = None

    telefone: Optional[str] = None

    whatsapp: Optional[str] = None

    email: Optional[str] = None

    # =========================================
    # ENDEREÇO
    # =========================================

    endereco: Optional[str] = None

    bairro: Optional[str] = None

    cidade: Optional[str] = None

    estado: Optional[str] = None

    cep: Optional[str] = None

    # =========================================
    # GEOLOCALIZAÇÃO
    # =========================================

    latitude: Optional[float] = None

    longitude: Optional[float] = None

    # =========================================
    # STATUS
    # =========================================

    ativo: Optional[bool] = None

    avaliacao_media: Optional[float] = None

    # =========================================
    # DOCUMENTOS
    # =========================================

    cpf: Optional[str] = None

    cnpj: Optional[str] = None

    # =========================================
    # SERVIÇO
    # =========================================

    servico_id: Optional[int] = None

    # =========================================
    # ⭐ PREMIUM / MONETIZAÇÃO
    # =========================================

    premium: Optional[bool] = None

    destaque: Optional[bool] = None

    plano: Optional[str] = None

    prioridade: Optional[int] = None

    whatsapp_destacado: Optional[bool] = None

    exibir_no_topo: Optional[bool] = None

    selo_premium: Optional[bool] = None


# =====================================================
# 🔹 RESPONSE
# =====================================================

class EmpresaResponse(EmpresaBase):

    id: int

    servico_id: Optional[int] = None

    # =========================================
    # FOTO PRINCIPAL
    # =========================================

    foto_principal: Optional[str] = None

    fotos: List[FotoResponse] = Field(
        default_factory=list
    )

    # =========================================
    # DISTÂNCIA
    # =========================================

    distancia_km: Optional[float] = None

    # =========================================
    # AVALIAÇÕES
    # =========================================

    avaliacao_media: Optional[float] = 0.0

    avaliacoes: List[AvaliacaoResponse] = Field(
        default_factory=list
    )

    # =========================================
    # ESTATÍSTICAS
    # =========================================

    total_avaliacoes: Optional[int] = 0

    is_premium: Optional[bool] = False

    # =========================================
    # CONFIG
    # =========================================

    model_config = ConfigDict(
        from_attributes=True
    )