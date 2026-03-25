from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.empresa_model import Empresa
from app.models.categoria_model import Categoria
from app.models.foto_model import Foto
from app.models.avaliacao_model import Avaliacao

from app.schemas.empresa_schema import EmpresaCreate
from app.core.deps import get_current_user

import cloudinary.uploader
from app.core.cloudinary_config import *

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
# LISTAR EMPRESAS
# =========================

@router.get("/listar")
def listar_empresas(
    db: Session = Depends(get_db),
):

    empresas = db.query(Empresa).all()

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
            "foto": foto.caminho if foto else None
        })

    return resultado


# =========================
# UPLOAD FOTO CLOUDINARY
# =========================

@router.post("/upload_foto/{empresa_id}")
def upload_foto(
    empresa_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    resultado = cloudinary.uploader.upload(file.file)

    url = resultado["secure_url"]

    principal = db.query(Foto).filter(
        Foto.empresa_id == empresa_id,
        Foto.principal == True
    ).first()

    nova = Foto(
        caminho=url,
        empresa_id=empresa_id,
        principal=True if not principal else False
    )

    db.add(nova)
    db.commit()

    return {"url": url}


# =========================
# LISTAR FOTOS
# =========================

@router.get("/fotos/{empresa_id}")
def listar_fotos(
    empresa_id: int,
    db: Session = Depends(get_db)
):

    fotos = db.query(Foto).filter(
        Foto.empresa_id == empresa_id
    ).all()

    return [
        {
            "id": f.id,
            "principal": f.principal,
            "url": f.caminho
        }
        for f in fotos
    ]


# =========================
# FOTO PRINCIPAL
# =========================

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

    db.query(Foto).filter(
        Foto.empresa_id == foto.empresa_id
    ).update({"principal": False})

    foto.principal = True

    db.commit()

    return {"msg": "foto principal definida"}


# =========================
# DETALHE EMPRESA
# =========================

@router.get("/detalhe/{empresa_id}")
def detalhe_empresa(
    empresa_id: int,
    db: Session = Depends(get_db)
):

    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        return {"erro": "empresa não encontrada"}

    categoria = db.query(Categoria).filter(
        Categoria.id == empresa.categoria_id
    ).first()

    fotos = db.query(Foto).filter(
        Foto.empresa_id == empresa.id
    ).all()

    avaliacoes = db.query(Avaliacao).filter(
        Avaliacao.empresa_id == empresa.id
    ).all()

    lista_fotos = []

    for f in fotos:
        lista_fotos.append({
            "id": f.id,
            "principal": f.principal,
            "url": f.caminho
        })

    media = 0

    if avaliacoes:
        media = sum([a.nota for a in avaliacoes]) / len(avaliacoes)

    return {
        "id": empresa.id,
        "nome": empresa.nome,
        "cidade": empresa.cidade,
        "bairro": empresa.bairro,
        "endereco": empresa.endereco,
        "categoria": categoria.nome if categoria else None,
        "avaliacao_media": media,
        "fotos": lista_fotos
    }


# =========================
# POR CATEGORIA
# =========================

@router.get("/por_categoria/{categoria_id}")
def por_categoria(
    categoria_id: int,
    db: Session = Depends(get_db)
):

    empresas = db.query(Empresa).filter(
        Empresa.categoria_id == categoria_id
    ).all()

    resultado = []

    for e in empresas:

        foto = db.query(Foto).filter(
            Foto.empresa_id == e.id,
            Foto.principal == True
        ).first()

        resultado.append({
            "id": e.id,
            "nome": e.nome,
            "cidade": e.cidade,
            "foto": foto.caminho if foto else None
        })

    return resultado


# =========================
# HOME
# =========================

@router.get("/home")
def home(
    db: Session = Depends(get_db)
):

    empresas = db.query(Empresa).limit(20).all()

    resultado = []

    for e in empresas:

        foto = db.query(Foto).filter(
            Foto.empresa_id == e.id,
            Foto.principal == True
        ).first()

        resultado.append({
            "id": e.id,
            "nome": e.nome,
            "cidade": e.cidade,
            "foto": foto.caminho if foto else None
        })

    return resultado