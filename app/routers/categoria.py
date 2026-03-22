from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine

router = APIRouter()


@router.get("/categorias")
def listar():

    with engine.connect() as conn:

        result = conn.execute(text(
            "SELECT * FROM categorias ORDER BY nome"
        ))

        return [dict(r._mapping) for r in result]


@router.post("/categorias")
def criar(nome: str):

    with engine.connect() as conn:

        conn.execute(
            text(
                "INSERT INTO categorias (nome) VALUES (:nome)"
            ),
            {"nome": nome}
        )

        conn.commit()

    return {"msg": "ok"}