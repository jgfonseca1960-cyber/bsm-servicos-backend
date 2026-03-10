from pydantic import BaseModel

class EmpresaCreate(BaseModel):

    nome: str
    responsavel: str
    telefone: str
    endereco: str
    cidade: str
    estado:str
    tipo_servico: str
    descricao: str | None = None
    categoria: str
    latitude: float
    longitude: float


class EmpresaResponse(EmpresaCreate):

    id: int
    media_avaliacoes: float | None = None
    total_avaliacoes: int | None = None

    class Config:
        from_attributes = True