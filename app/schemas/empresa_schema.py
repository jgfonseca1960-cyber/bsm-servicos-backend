from pydantic import BaseModel

class EmpresaCreate(BaseModel):

    nome: str
    responsavel: str | None = None
    telefone: str | None = None
    endereco: str | None = None

    cidade: str
    estado: str | None = None
    bairro: str | None = None

    tipo_servico: str | None = None
    categoria: str | None = None

    descricao: str | None = None

    latitude: float | None = None
    longitude: float | None = None


class EmpresaResponse(EmpresaCreate):

    id: int

    media_avaliacoes: float | None = None
    total_avaliacoes: int | None = None

    class Config:
        from_attributes = True