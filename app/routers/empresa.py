from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
import shutil
import os

from app.database import get_db, engine

from app.models.empresa_model import Empresa
from app.models.categoria_model import Categoria
from app.models.foto_model import Foto
from app.models.avaliacao_model import Avaliacao

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
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if not current_user:
        raise HTTPException(401, "Usuário não autenticado")

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


# =========================
# LISTAR EMPRESAS (COM FOTO + MEDIA)
# =========================

@router.get("/listar")
def listar_empresas(
    request: Request,
    db: Session = Depends(get_db),

    pagina: int = 1,
    limite: int = 10,
    categoria_id: int | None = None,
    cidade: str | None = None,
):

    query = db.query(Empresa)

    if categoria_id:
        query = query.filter(Empresa.categoria_id == categoria_id)

    if cidade:
        query = query.filter(Empresa.cidade.ilike(f"%{cidade}%"))

    offset = (pagina - 1) * limite

    empresas = query.offset(offset).limit(limite).all()

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


# =========================
# UPLOAD FOTO
# =========================

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

    return {"msg": "foto enviada"}


# =========================
# LISTAR FOTOS
# =========================

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

    return [
        {
            "id": f.id,
            "principal": f.principal,
            "url": base_url + f.caminho
        }
        for f in fotos
    ]

## FOTO PRINCIPAL

@router.post("/foto_principal/{foto_id}")
def foto_principal(
    foto_id: int,
    db: Session = Depends(get_db)
):

    foto = db.query(Foto).filter(
        Foto.id == foto_id
    ).first()

    if not foto:
        return {"erro": "foto não encontrada"}

    # remove principal das outras
    db.query(Foto).filter(
        Foto.empresa_id == foto.empresa_id
    ).update({"principal": False})

    foto.principal = True

    db.commit()

    return {"msg": "foto principal definida"}