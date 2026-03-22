from pydantic import BaseModel


class EmpresaCreate(BaseModel):

    nome: str
    cnpj: str | None = None
    cpf: str | None = None
    responsavel: str | None = None

    endereco: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    estado: str | None = None

    categoria_id: int | None = None

    latitude: float | None = None
    longitude: float | None = None

    logo: str | None = None


class EmpresaOut(BaseModel):

    id: int
    nome: str
    cidade: str | None = None

    class Config:
        from_attributes = True