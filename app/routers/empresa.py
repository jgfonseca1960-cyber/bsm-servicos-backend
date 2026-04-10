from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.empresa_model import Empresa
from app.models.categoria_model import Categoria
from app.models.avaliacao_model import Avaliacao
from app.models.foto_model import Foto  # ✅ CORREÇÃO

from app.schemas.empresa_schema import EmpresaCreate, EmpresaUpdate  # ✅ ADD UPDATE
from app.core.deps import get_current_user

import cloudinary.uploader
from app.core.cloudinary_config import *

router = APIRouter(
    prefix="/empresas",  # ✅ PADRÃO REST
    tags=["Empresas"]
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
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

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
# ATUALIZAR EMPRESA (PUT)
# =========================

@router.put("/{empresa_id}")
def atualizar_empresa(
    empresa_id: int,
    dados: EmpresaUpdate,
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    for key, value in dados.dict(exclude_unset=True).items():
        setattr(empresa, key, value)

    db.commit()
    db.refresh(empresa)

    return empresa


# =========================
# LISTAR EMPRESAS
# =========================

@router.get("/")
def listar_empresas(db: Session = Depends(get_db)):

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
# DETALHE EMPRESA
# =========================

@router.get("/{empresa_id}")
def detalhe_empresa(
    empresa_id: int,
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    categoria = db.query(Categoria).filter(
        Categoria.id == empresa.categoria_id
    ).first()

    fotos = db.query(Foto).filter(
        Foto.empresa_id == empresa.id
    ).all()

    avaliacoes = db.query(Avaliacao).filter(
        Avaliacao.empresa_id == empresa.id
    ).all()

    lista_fotos = [
        {
            "id": f.id,
            "principal": f.principal,
            "url": f.caminho
        }
        for f in fotos
    ]

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