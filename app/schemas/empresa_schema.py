from pydantic import BaseModel


class EmpresaCreate(BaseModel):

    nome: str
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

    class Config:
        from_attributes = True