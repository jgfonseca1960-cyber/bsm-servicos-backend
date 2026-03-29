from pydantic import BaseModel


class ServicoBase(BaseModel):
    nome: str
    tipo_id: int


class ServicoCreate(ServicoBase):
    pass


class ServicoResponse(ServicoBase):
    id: int

    class Config:
        from_attributes = True