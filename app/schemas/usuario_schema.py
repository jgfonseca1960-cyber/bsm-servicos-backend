from pydantic import BaseModel, EmailStr


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    is_admin: bool = False


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    is_admin: bool

    class Config:
        from_attributes = True