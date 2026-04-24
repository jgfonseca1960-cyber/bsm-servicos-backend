from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from app.database import get_db
from app.models.empresa_model import Empresa
from app.models.empresa_foto_model import EmpresaFoto

# 🔥 UTIL
from app.utils.files import gerar_url_imagem

router = APIRouter(tags=["Empresas"])


# =========================
# 📦 SCHEMAS
# =========================
class EmpresaCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ativo: Optional[bool] = True
    avaliacao_media: Optional[float] = None
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    servico_id: Optional[int] = None


class EmpresaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ativo: Optional[bool] = None
    avaliacao_media: Optional[float] = None
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    servico_id: Optional[int] = None


# =========================
# 🔧 TRATAMENTO DE URL (🔥 CORREÇÃO PRINCIPAL)
# =========================
def tratar_url(url: str):
    if not url:
        return None

    # 🔥 Cloudinary → usa direto
    if url.startswith("http"):
        return url

    # 🔥 Local → monta URL
    return gerar_url_imagem(url)


# =========================
# 🔧 SERIALIZER
# =========================
def empresa_to_dict(e: Empresa):
    foto_principal = None
    galeria = []

    for f in (e.fotos or []):
        url = tratar_url(f.url)

        if not url:
            continue

        if f.principal:
            foto_principal = url
        else:
            galeria.append({
                "id": f.id,
                "url": url
            })

    # fallback automático
    if not foto_principal and galeria:
        foto_principal = galeria[0]["url"]

    return {
        "id": e.id,
        "nome": e.nome,
        "descricao": e.descricao,
        "telefone": e.telefone,
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
        "fotos": galeria
    }


# =========================
# 📌 LISTAGEM
# =========================
@router.get("/")
def listar_empresas(db: Session = Depends(get_db), skip: int = 0, limit: int = 50):
    try:
        empresas = db.query(Empresa).offset(skip).limit(limit).all()
        return [empresa_to_dict(e) for e in empresas]

    except Exception as e:
        print("ERRO LISTAGEM:", e)
        raise HTTPException(status_code=500, detail="Erro interno no servidor")


# =========================
# 🔍 DETALHE
# =========================
@router.get("/id/{empresa_id}")
def detalhe_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return empresa_to_dict(empresa)


# =========================
# ➕ CRIAR
# =========================
@router.post("/")
def criar_empresa(data: EmpresaCreate, db: Session = Depends(get_db)):
    empresa = Empresa(**data.model_dump())
    db.add(empresa)
    db.commit()
    db.refresh(empresa)

    return {"msg": "Empresa criada", "id": empresa.id}


# =========================
# ✏️ ATUALIZAR
# =========================
@router.put("/id/{empresa_id}")
def atualizar_empresa(empresa_id: int, data: EmpresaUpdate, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(empresa, key, value)

    db.commit()
    db.refresh(empresa)

    return {"msg": "Empresa atualizada"}


# =========================
# ❌ DELETAR EMPRESA
# =========================
@router.delete("/id/{empresa_id}")
def deletar_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    db.delete(empresa)
    db.commit()

    return {"msg": "Empresa deletada"}


# =========================
# 📸 UPLOAD FOTO (CLOUDINARY)
# =========================
@router.post("/id/{empresa_id}/upload-foto")
async def upload_foto(
    empresa_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    import cloudinary.uploader

    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    try:
        resultado = cloudinary.uploader.upload(
            await file.read(),
            folder="empresas"
        )

        url = resultado.get("secure_url")
        public_id = resultado.get("public_id")

        # 🔥 verifica se já existe principal
        existe_principal = db.query(EmpresaFoto).filter(
            EmpresaFoto.empresa_id == empresa_id,
            EmpresaFoto.principal == True
        ).first()

        foto = EmpresaFoto(
            empresa_id=empresa_id,
            url=url,
            public_id=public_id,
            principal=False if existe_principal else True  # 🔥 PRIMEIRA FOTO vira principal
        )

        db.add(foto)
        db.commit()

        return {
            "msg": "Foto enviada com sucesso",
            "url": url
        }

    except Exception as e:
        print("Erro Cloudinary:", e)
        raise HTTPException(status_code=500, detail="Erro ao enviar imagem")


# =========================
# ⭐ DEFINIR FOTO PRINCIPAL
# =========================
@router.put("/id/{empresa_id}/foto/{foto_id}/principal")
def definir_foto_principal(
    empresa_id: int,
    foto_id: int,
    db: Session = Depends(get_db)
):
    foto = db.query(EmpresaFoto).filter(
        EmpresaFoto.id == foto_id,
        EmpresaFoto.empresa_id == empresa_id
    ).first()

    if not foto:
        raise HTTPException(status_code=404, detail="Foto não encontrada")

    db.query(EmpresaFoto).filter(
        EmpresaFoto.empresa_id == empresa_id
    ).update({"principal": False})

    foto.principal = True
    db.commit()

    return {"msg": "Foto principal definida com sucesso"}


# =========================
# 🗑️ DELETAR FOTO
# =========================
@router.delete("/id/{empresa_id}/foto/{foto_id}")
def deletar_foto(
    empresa_id: int,
    foto_id: int,
    db: Session = Depends(get_db)
):
    import cloudinary.uploader

    foto = db.query(EmpresaFoto).filter(
        EmpresaFoto.id == foto_id,
        EmpresaFoto.empresa_id == empresa_id
    ).first()

    if not foto:
        raise HTTPException(status_code=404, detail="Foto não encontrada")

    try:
        # 🔥 se for principal → define outra automaticamente
        if foto.principal:
            outra = db.query(EmpresaFoto).filter(
                EmpresaFoto.empresa_id == empresa_id,
                EmpresaFoto.id != foto.id
            ).first()

            if outra:
                outra.principal = True

        # 🔥 remove do cloudinary
        if foto.public_id:
            cloudinary.uploader.destroy(foto.public_id)

        db.delete(foto)
        db.commit()

        return {"msg": "Foto deletada com sucesso"}

    except Exception as e:
        print("Erro ao deletar foto:", e)
        raise HTTPException(status_code=500, detail="Erro ao deletar foto")