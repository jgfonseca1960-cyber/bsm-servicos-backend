## empresa.py
from fastapi import APIRouter, UploadFile, File
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.empresa_model import Empresa
from app.schemas.empresa_schema import EmpresaCreate
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/empresa",
    tags=["Empresa"]
)


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
            tipo_servico=dados.tipo_servico,
            latitude=dados.latitude,
            longitude=dados.longitude,
            avaliacao=dados.avaliacao,
            usuario_id=current_user.id
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

from sqlalchemy import text
from app.database import engine
from fastapi import APIRouter

router = APIRouter()


@router.get("/empresas_com_avaliacao")
def empresas_com_avaliacao():

    with engine.connect() as conn:

        result = conn.execute(text("""

            SELECT
                e.id,
                e.nome,
                e.categoria,
                AVG(a.nota) as media,
                COUNT(a.id) as total_avaliacoes

            FROM empresas e

            LEFT JOIN avaliacoes a
            ON a.empresa_id = e.id

            GROUP BY e.id

            ORDER BY e.nome

        """))

        return [dict(row._mapping) for row in result]
    
from fastapi import UploadFile, File
import shutil
import os
from sqlalchemy import text
from app.database import engine

@router.post("/upload_logo/{empresa_id}")
def upload_logo(empresa_id: int, file: UploadFile = File(...)):

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

    return {"msg": "Logo enviado", "path": caminho}