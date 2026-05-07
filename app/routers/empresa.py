```python
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os
import shutil
import uuid

from app.database import get_db

from app.models.empresa_model import Empresa
from app.models.empresa_foto_model import EmpresaFoto
from app.models.avaliacao_model import Avaliacao

from app.schemas.empresa_schema import (
    EmpresaCreate,
    EmpresaUpdate
)

router = APIRouter(
    prefix="/empresa",
    tags=["Empresa"]
)

# =========================
# 📁 CONFIG UPLOAD
# =========================
UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

# =========================
# 📸 UPLOAD FOTO
# =========================
@router.post("/{empresa_id}/fotos")
def upload_foto(
    empresa_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    filename = f"{uuid.uuid4()}_{file.filename}"

    filepath = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    foto = EmpresaFoto(
        empresa_id=empresa_id,
        url=f"/uploads/{filename}",
        principal=False
    )

    db.add(foto)

    db.commit()

    db.refresh(foto)

    return {
        "message": "Foto enviada com sucesso",
        "foto": {
            "id": foto.id,
            "url": foto.url,
            "principal": foto.principal
        }
    }


# =========================
# ⭐ DEFINIR FOTO PRINCIPAL
# =========================
@router.put(
    "/{empresa_id}/foto-principal/{foto_id}"
)
def definir_foto_principal(
    empresa_id: int,
    foto_id: int,
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    fotos = db.query(EmpresaFoto).filter(
        EmpresaFoto.empresa_id == empresa_id
    ).all()

    foto_principal = None

    for foto in fotos:
        foto.principal = False

        if foto.id == foto_id:
            foto.principal = True
            foto_principal = foto

    if not foto_principal:
        raise HTTPException(
            status_code=404,
            detail="Foto não encontrada"
        )

    db.commit()

    return {
        "message": "Foto principal atualizada"
    }


# =========================
# ❌ DELETAR FOTO
# =========================
@router.delete("/foto/{foto_id}")
def deletar_foto(
    foto_id: int,
    db: Session = Depends(get_db)
):
    foto = db.query(EmpresaFoto).filter(
        EmpresaFoto.id == foto_id
    ).first()

    if not foto:
        raise HTTPException(
            status_code=404,
            detail="Foto não encontrada"
        )

    caminho_arquivo = foto.url.replace(
        "/uploads/",
        "uploads/"
    )

    if os.path.exists(caminho_arquivo):
        os.remove(caminho_arquivo)

    db.delete(foto)

    db.commit()

    return {
        "message": "Foto removida"
    }


# =========================
# ➕ CRIAR EMPRESA
# =========================
@router.post("/")
def criar_empresa(
    dados: EmpresaCreate,
    db: Session = Depends(get_db)
):
    nova = Empresa(**dados.dict())

    db.add(nova)

    db.commit()

    db.refresh(nova)

    return nova


# =========================
# 📡 LISTAR EMPRESAS
# =========================
@router.get("/")
def listar_empresas(
    db: Session = Depends(get_db)
):
    empresas = db.query(Empresa).all()

    resultado = []

    for e in empresas:

        avaliacoes = db.query(Avaliacao).filter(
            Avaliacao.empresa_id == e.id
        ).all()

        media = 0

        if avaliacoes:
            media = (
                sum([a.nota for a in avaliacoes])
                / len(avaliacoes)
            )

        lista_fotos = [
            {
                "id": f.id,
                "url": f.url,
                "principal": f.principal
            }
            for f in e.fotos
        ]

        resultado.append({
            "id": e.id,
            "nome": e.nome,
            "descricao": e.descricao,

            "telefone": e.telefone,
            "whatsapp": e.whatsapp,
            "email": e.email,

            "endereco": e.endereco,
            "bairro": e.bairro,
            "cidade": e.cidade,
            "estado": e.estado,
            "cep": e.cep,

            "latitude": e.latitude,
            "longitude": e.longitude,

            "ativo": e.ativo,

            "avaliacao_media": media,

            "cpf": e.cpf,
            "cnpj": e.cnpj,

            "servico_id": e.servico_id,

            "foto_principal": e.foto_principal,

            "fotos": lista_fotos
        })

    return resultado


# =========================
# 🔍 DETALHE EMPRESA
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
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    avaliacoes = db.query(Avaliacao).filter(
        Avaliacao.empresa_id == empresa.id
    ).all()

    media = 0

    if avaliacoes:
        media = (
            sum([a.nota for a in avaliacoes])
            / len(avaliacoes)
        )

    lista_fotos = [
        {
            "id": f.id,
            "url": f.url,
            "principal": f.principal
        }
        for f in empresa.fotos
    ]

    return {
        "id": empresa.id,
        "nome": empresa.nome,
        "descricao": empresa.descricao,

        "telefone": empresa.telefone,
        "whatsapp": empresa.whatsapp,
        "email": empresa.email,

        "endereco": empresa.endereco,
        "bairro": empresa.bairro,
        "cidade": empresa.cidade,
        "estado": empresa.estado,
        "cep": empresa.cep,

        "latitude": empresa.latitude,
        "longitude": empresa.longitude,

        "ativo": empresa.ativo,

        "avaliacao_media": media,

        "cpf": empresa.cpf,
        "cnpj": empresa.cnpj,

        "servico_id": empresa.servico_id,

        "foto_principal": empresa.foto_principal,

        "fotos": lista_fotos,

        "avaliacoes": [
            {
                "id": a.id,
                "usuario": a.usuario_nome,
                "nota": a.nota,
                "comentario": a.comentario
            }
            for a in avaliacoes
        ]
    }


# =========================
# ✏️ ATUALIZAR EMPRESA
# =========================
@router.put("/{empresa_id}")
def atualizar_empresa(
    empresa_id: int,
    dados: EmpresaUpdate,
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    update_data = dados.dict(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            empresa,
            key,
            value
        )

    db.commit()

    db.refresh(empresa)

    return empresa


# =========================
# ❌ DELETAR EMPRESA
# =========================
@router.delete("/{empresa_id}")
def deletar_empresa(
    empresa_id: int,
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    db.delete(empresa)

    db.commit()

    return {
        "message": "Empresa removida com sucesso"
    }
```
