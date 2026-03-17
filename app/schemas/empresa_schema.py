from pydantic import BaseModel


class EmpresaCreate(BaseModel):

    nome: str
    cidade: str
    tipo_servico: str
    categoria: str
    telefone: str
    endereco: str
    descricao: str
    latitude: float
    longitude: float


class EmpresaResponse(EmpresaCreate):

    id: int

    class Config:
        from_attributes = True