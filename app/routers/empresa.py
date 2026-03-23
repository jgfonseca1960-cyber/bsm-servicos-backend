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
            logo=dados.logo,
            usuario_id=current_user["id"]
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


        ## Criação de vinculo de fotos

from app.models.foto_model import Foto

@router.post("/upload_foto/{empresa_id}")
def upload_foto(
    empresa_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    pasta = "uploads"

    if not os.path.exists(pasta):
        os.makedirs(pasta)

    caminho = f"{pasta}/{empresa_id}_{file.filename}"

    with open(caminho, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # verifica se já existe foto principal
    principal = db.query(Foto).filter(
        Foto.empresa_id == empresa_id,
        Foto.principal == True
    ).first()

    nova = Foto(
        caminho=caminho,
        empresa_id=empresa_id,
        principal=True if not principal else False
    )

    db.add(nova)
    db.commit()

    return {
        "msg": "Foto enviada",
        "principal": nova.principal
    }


### Incluir Fotos

from app.models.foto_model import Foto
from fastapi import Request

@router.get("/fotos/{empresa_id}")
def listar_fotos(
    empresa_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    fotos = db.query(Foto).filter(
        Foto.empresa_id == empresa_id
    ).all()

    base_url = str(request.base_url)

    resultado = []

    for f in fotos:

        resultado.append({
            "id": f.id,
            "empresa_id": f.empresa_id,
            "principal": f.principal,
            "url": base_url + f.caminho
        })

    return resultado

@router.post("/foto_principal/{foto_id}")

def foto_principal(foto_id: int, db: Session = Depends(get_db)):

    foto = db.query(Foto).filter(
        Foto.id == foto_id
    ).first()

    if not foto:
        return {"erro": "foto não encontrada"}

    # remover principal das outras
    db.query(Foto).filter(
        Foto.empresa_id == foto.empresa_id
    ).update({"principal": False})

    foto.principal = True

    db.commit()

    return {"msg": "foto principal definida"}

@router.delete("/foto/{foto_id}")
def deletar_foto(foto_id: int, db: Session = Depends(get_db)):

    foto = db.query(Foto).filter(
        Foto.id == foto_id
    ).first()

    if not foto:
        return {"erro": "não encontrada"}

    db.delete(foto)
    db.commit()

    return {"msg": "foto deletada"}

from fastapi import Request
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import get_db
from app.models.empresa_model import Empresa
from app.models.categoria_model import Categoria
from app.models.foto_model import Foto
from app.models.avaliacao_model import Avaliacao


@router.get("/listar")
def listar_empresas(
    request: Request,
    db: Session = Depends(get_db)
):

    empresas = db.query(Empresa).all()

    base_url = str(request.base_url)

    resultado = []

    for e in empresas:

        categoria = db.query(Categoria).filter(
            Categoria.id == e.categoria_id
        ).first()

        foto = db.query(Foto).filter(
            Foto.empresa_id == e.id,
            Foto.principal == True
        ).first()

        avaliacoes = db.query(Avaliacao).filter(
            Avaliacao.empresa_id == e.id
        ).all()

        media = 0

        if avaliacoes:
            media = sum([a.nota for a in avaliacoes]) / len(avaliacoes)

        resultado.append({

            "id": e.id,
            "nome": e.nome,
            "cidade": e.cidade,
            "categoria": categoria.nome if categoria else None,
            "avaliacao": media,
            "foto": base_url + foto.caminho if foto else None

        })

    return resultado