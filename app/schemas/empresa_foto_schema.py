from pydantic import BaseModel


class FotoResponse(BaseModel):
    id: int
    url: str

    class Config:
        from_attributes = True