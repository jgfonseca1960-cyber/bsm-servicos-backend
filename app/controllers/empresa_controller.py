from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional, List
import math
from uuid import uuid4
import os

from app.database import get_db
from app.models.empresa_model import Empresa
from app.models.empresa_foto_model import EmpresaFoto
from app.models.servico_model import Servico

from app.utils.files import gerar_url_imagem

import cloudinary.uploader

from app.schemas.empresa_schema import (
    EmpresaCreate,
    EmpresaUpdate,
    EmpresaResponse,
)

router = APIRouter(
    prefix="/empresa",
    tags=["Empresas"]
)

# =========================================================
# 📁 GARANTE PASTA UPLOAD
# =========================================================
os.makedirs("uploads/empresas", exist_ok=True)

# =========================================================
# 📍 DISTÂNCIA
# =========================================================
def calcular_distancia(lat1, lon1, lat2, lon2):
    if not lat1 or not lon1 or not lat2 or not lon2:
        return None

    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(R * c, 2)

# =========================================================
# 🔧 TRATAR URL
# =========================================================
def tratar_url(url: str):
    if not url:
        return None

    if url.startswith("http"):
        return url

    return gerar_url_imagem(url)

# =========================================================
# 🔥 SERIALIZER
# =========================================================
def empresa_to_dict(
    e: Empresa,
    user_lat=None,
    user_lon=None
):

    fotos_validas = []

    fotos_ordenadas = sorted(
        e.fotos or [],
        key=lambda x: (
            not x.principal,
            x.id
        )
    )

    for f in fotos_ordenadas:

        url = tratar_url(f.url)

        if not url:
            continue

        fotos_validas.append({
            "id": f.id,
            "url": url,
            "principal": bool(f.principal)
        })

    foto_principal = None

    for foto in fotos_validas:
        if foto["principal"]:
            foto_principal = foto["url"]
            break

    if not foto_principal and fotos_validas:
        foto_principal = fotos_validas[0]["url"]

    distancia = None

    if (
        user_lat
        and user_lon
        and e.latitude
        and e.longitude
    ):
        distancia = calcular_distancia(
            user_lat,
            user_lon,
            e.latitude,
            e.longitude
        )

    return {
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
        "avaliacao_media": e.avaliacao_media,

        "cpf": e.cpf,
        "cnpj": e.cnpj,

        "servico_id": e.servico_id,

        "foto_principal": foto_principal,
        "fotos": fotos_validas,

        "distancia_km": distancia
    }

# =========================================================
# 🔍 LISTAR EMPRESAS
# =========================================================
@router.get(
    "/",
    response_model=List[EmpresaResponse]
)
def listar_empresas(
    db: Session = Depends(get_db),
    servico_id: Optional[int] = None,
    cidade: Optional[str] = None,
    bairro: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
):

    query = db.query(Empresa)

    if servico_id:
        query = query.filter(
            Empresa.servico_id == servico_id
        )

    if cidade:
        query = query.filter(
            Empresa.cidade.ilike(f"%{cidade}%")
        )

    if bairro:
        query = query.filter(
            Empresa.bairro.ilike(f"%{bairro}%")
        )

    empresas = query.all()

    resultado = [
        empresa_to_dict(
            e,
            latitude,
            longitude
        )
        for e in empresas
    ]

    if latitude and longitude:
        resultado.sort(
            key=lambda x:
            x["distancia_km"]
            if x["distancia_km"]
            else 9999
        )

    return resultado

# =========================================================
# 🔍 DETALHE EMPRESA
# =========================================================
@router.get(
    "/{empresa_id}",
    response_model=EmpresaResponse
)
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

    return empresa_to_dict(empresa)

# =========================================================
# ➕ CRIAR EMPRESA
# =========================================================
@router.post(
    "/",
    response_model=EmpresaResponse
)
def criar_empresa(
    data: EmpresaCreate,
    db: Session = Depends(get_db)
):

    if data.servico_id == 0:
        raise HTTPException(
            status_code=400,
            detail="servico_id inválido"
        )

    servico = db.query(Servico).filter(
        Servico.id == data.servico_id
    ).first()

    if not servico:
        raise HTTPException(
            status_code=404,
            detail="Serviço não encontrado"
        )

    try:

        empresa = Empresa(
            **data.model_dump()
        )

        db.add(empresa)
        db.commit()
        db.refresh(empresa)

        return empresa_to_dict(empresa)

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =========================================================
# ✏️ ATUALIZAR EMPRESA
# =========================================================
@router.put(
    "/{empresa_id}",
    response_model=EmpresaResponse
)
def atualizar_empresa(
    empresa_id: int,
    data: EmpresaUpdate,
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

    update_data = data.model_dump(
        exclude_unset=True
    )

    if "servico_id" in update_data:

        if update_data["servico_id"] == 0:
            raise HTTPException(
                status_code=400,
                detail="servico_id inválido"
            )

        servico = db.query(Servico).filter(
            Servico.id == update_data["servico_id"]
        ).first()

        if not servico:
            raise HTTPException(
                status_code=404,
                detail="Serviço não encontrado"
            )

    try:

        for key, value in update_data.items():
            setattr(empresa, key, value)

        db.commit()
        db.refresh(empresa)

        return empresa_to_dict(empresa)

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =========================================================
# ❌ DELETAR EMPRESA
# =========================================================
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
        "msg": "Empresa deletada"
    }

# =========================================================
# 📸 UPLOAD LOCAL
# =========================================================
@router.post("/{empresa_id}/fotos")
def upload_foto_local(
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

    try:

        filename = f"{uuid4()}_{file.filename}"

        filepath = (
            f"uploads/empresas/{filename}"
        )

        with open(filepath, "wb") as buffer:
            buffer.write(file.file.read())

        total_fotos = db.query(EmpresaFoto).filter(
            EmpresaFoto.empresa_id == empresa_id
        ).count()

        foto = EmpresaFoto(
            empresa_id=empresa_id,
            url=filepath,
            principal=(total_fotos == 0)
        )

        db.add(foto)
        db.commit()
        db.refresh(foto)

        return {
            "msg": "Foto enviada",
            "foto": {
                "id": foto.id,
                "url": gerar_url_imagem(filepath),
                "principal": foto.principal
            }
        }

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =========================================================
# ☁️ UPLOAD CLOUDINARY
# =========================================================
@router.post("/{empresa_id}/upload-cloudinary")
def upload_foto_cloudinary(
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

    try:

        resultado = cloudinary.uploader.upload(
            file.file,
            folder="bsm/empresas"
        )

        url = resultado.get("secure_url")

        total_fotos = db.query(EmpresaFoto).filter(
            EmpresaFoto.empresa_id == empresa_id
        ).count()

        foto = EmpresaFoto(
            empresa_id=empresa_id,
            url=url,
            principal=(total_fotos == 0)
        )

        db.add(foto)
        db.commit()
        db.refresh(foto)

        return {
            "msg": "Upload Cloudinary OK",
            "foto": {
                "id": foto.id,
                "url": url,
                "principal": foto.principal
            }
        }

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Erro upload: {str(e)}"
        )

# =========================================================
# ⭐ DEFINIR FOTO PRINCIPAL
# =========================================================
@router.put(
    "/{empresa_id}/foto-principal/{foto_id}"
)
def definir_principal(
    empresa_id: int,
    foto_id: int,
    db: Session = Depends(get_db)
):

    foto = db.query(EmpresaFoto).filter(
        EmpresaFoto.id == foto_id,
        EmpresaFoto.empresa_id == empresa_id
    ).first()

    if not foto:
        raise HTTPException(
            status_code=404,
            detail="Foto não encontrada"
        )

    db.query(EmpresaFoto).filter(
        EmpresaFoto.empresa_id == empresa_id
    ).update({
        "principal": False
    })

    foto.principal = True

    db.commit()

    return {
        "msg": "Foto principal definida"
    }

# =========================================================
# ❌ EXCLUIR FOTO
# =========================================================
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

    empresa_id = foto.empresa_id
    era_principal = foto.principal

    db.delete(foto)
    db.commit()

    if era_principal:

        nova_principal = db.query(EmpresaFoto).filter(
            EmpresaFoto.empresa_id == empresa_id
        ).first()

        if nova_principal:
            nova_principal.principal = True
            db.commit()

    return {
        "msg": "Foto removida"
    }