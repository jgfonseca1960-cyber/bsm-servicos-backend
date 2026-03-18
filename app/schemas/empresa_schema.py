from pydantic import BaseModel


class EmpresaCreate(BaseModel):

    nome: str
    cnpj: str
    cpf: str

    responsavel: str

    endereco: str
    bairro: str
    cidade: str
    estado: str

    tipo_servico: str

    latitude: float
    longitude: float

    avaliacao: float


class EmpresaOut(BaseModel):

    id: int
    nome: str
    cidade: str

    class Config:
        from_attributes = True