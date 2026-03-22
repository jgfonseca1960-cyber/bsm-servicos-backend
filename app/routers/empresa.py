from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import shutil
import os

from app.database import get_db, engine
from app.models.empresa_model import Empresa
from app.schemas.empresa_schema import EmpresaCreate
from app.core.deps import get_current_user


router = APIRouter(
    prefix="/empresa",
    tags=["Empresa"]
)


# =========================
# CRIAR EMPRESA
# =========================

@router.post("/")
def criar(
    dados: EmpresaCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Usuário não autenticado"
        )

    try:

        nova = Empresa(
            nome=dados.nome,
            cnpj=dados.cnpj,
            cpf=dados.cpf,
            responsavel=dados.responsavel,
            endereco=dados.endereco,
            bairro=dados.bairro,
            cidade=dados.cidade,
            estado=dados.estado,
            categoria_id=dados.categoria_id,
            latitude=dados.latitude,
            longitude=dados.longitude,
            logo=dados.logo
        )

        db.add(nova)
        db.commit()
        db.refresh(nova)

        return nova

    except Exception as e:

        print("ERRO EMPRESA:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# MEDIA DE AVALIACOES
# =========================

@router.get("/empresas_com_avaliacao")
def empresas_com_avaliacao():

    with engine.connect() as conn:

        result = conn.execute(text("""

            SELECT
                e.id,
                e.nome,
                AVG(a.nota) as media,
                COUNT(a.id) as total_avaliacoes

            FROM empresas e

            LEFT JOIN avaliacoes a
            ON a.empresa_id = e.id

            GROUP BY e.id

            ORDER BY e.nome

        """))

        return [dict(row._mapping) for row in result]


# =========================
# UPLOAD LOGO
# =========================

@router.post("/upload_logo/{empresa_id}")
def upload_logo(
    empresa_id: int,
    file: UploadFile = File(...)
):

    pasta = "uploads"

    if not os.path.exists(pasta):
        os.makedirs(pasta)

    caminho = f"{pasta}/{empresa_id}_{file.filename}"

    with open(caminho, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with engine.connect() as conn:

        conn.execute(
            text("""
                UPDATE empresas
                SET logo = :logo
                WHERE id = :id
            """),
            {"logo": caminho, "id": empresa_id}
        )

        conn.commit()

    return {
        "msg": "Logo enviado",
        "path": caminho
    }

@router.get("/lista_completa")
def lista_completa():

    with engine.connect() as conn:

        result = conn.execute(text("""

            SELECT

                e.id,
                e.nome,
                e.cidade,
                e.bairro,
                e.logo,

                c.nome as categoria,

                COALESCE(AVG(a.nota),0) as media,
                COUNT(a.id) as total_avaliacoes

            FROM empresas e

            LEFT JOIN categorias c
            ON c.id = e.categoria_id

            LEFT JOIN avaliacoes a
            ON a.empresa_id = e.id

            GROUP BY
                e.id,
                c.nome

            ORDER BY e.nome

        """))

        return [dict(r._mapping) for r in result]
    
    ## endpoint pesquisa por nome

from fastapi import Query
from sqlalchemy import text
from app.database import engine


@router.get("/busca")
def busca(
    categoria_id: int | None = None,
    nome: str | None = None,
    cidade: str | None = None,
):

    sql = """

        SELECT

            e.id,
            e.nome,
            e.cidade,
            e.bairro,
            e.logo,

            c.nome as categoria,

            COALESCE(AVG(a.nota),0) as media,
            COUNT(a.id) as total_avaliacoes

        FROM empresas e

        LEFT JOIN categorias c
            ON c.id = e.categoria_id

        LEFT JOIN avaliacoes a
            ON a.empresa_id = e.id

        WHERE 1=1

    """

    params = {}

    if categoria_id:
        sql += " AND e.categoria_id = :categoria_id"
        params["categoria_id"] = categoria_id

    if nome:
        sql += " AND LOWER(e.nome) LIKE LOWER(:nome)"
        params["nome"] = f"%{nome}%"

    if cidade:
        sql += " AND LOWER(e.cidade) LIKE LOWER(:cidade)"
        params["cidade"] = f"%{cidade}%"

    sql += """

        GROUP BY
            e.id,
            c.nome

        ORDER BY e.nome

    """

    with engine.connect() as conn:

        result = conn.execute(text(sql), params)

        return [dict(r._mapping) for r in result]