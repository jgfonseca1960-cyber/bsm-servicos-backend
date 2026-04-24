from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from app.database import get_db
from app.models.empresa_model import Empresa
from app.models.empresa_foto_model import EmpresaFoto
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
# 🔧 TRATAR URL (FIX GLOBAL)
# =========================
def tratar_url(url: str):
    if not url:
        return None

    if url.startswith("http"):
        return url

    return gerar_url_imagem(url)


# =========================
# 🔧 SERIALIZER (CORRIGIDO)
# =========================
def empresa_to_dict(e: Empresa):
    fotos_validas = []

    for f in (e.fotos or []):
        url = tratar_url(f.url)

        if not url:
            continue

        fotos_validas.append({
            "id": f.id,
            "url": url,
            "principal": f.principal
        })

    # 🔥 definir principal
    foto_principal = None

    for f in fotos_validas:
        if f["principal"]:
            foto_principal = f["url"]
            break

    # 🔥 fallback automático
    if not foto_principal and fotos_validas:
        foto_principal = fotos_validas[0]["url"]

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
        "fotos": fotos_validas
    }


# =========================
# 📌 LISTAGEM
# =========================
@router.get("/")
def listar_empresas(db: Session = Depends(get_db), skip: int = 0, limit: int = 50):
    empresas = db.query(Empresa).offset(skip).limit(limit).all()
    return [empresa_to_dict(e) for e in empresas]


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
    return {"msg": "Empresa atualizada"}


# =========================
# ❌ DELETAR
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

    resultado = cloudinary.uploader.upload(
        await file.read(),
        folder="empresas"
    )

    url = resultado.get("secure_url")
    public_id = resultado.get("public_id")

    existe_principal = db.query(EmpresaFoto).filter(
        EmpresaFoto.empresa_id == empresa_id,
        EmpresaFoto.principal == True
    ).first()

    foto = EmpresaFoto(
        empresa_id=empresa_id,
        url=url,
        public_id=public_id,
        principal=False if existe_principal else True
    )

    db.add(foto)
    db.commit()

    return {"msg": "Foto enviada", "url": url}


# =========================
# ⭐ DEFINIR PRINCIPAL
# =========================
@router.put("/id/{empresa_id}/foto/{foto_id}/principal")
def definir_foto_principal(empresa_id: int, foto_id: int, db: Session = Depends(get_db)):
    db.query(EmpresaFoto).filter(
        EmpresaFoto.empresa_id == empresa_id
    ).update({"principal": False})

    foto = db.query(EmpresaFoto).filter(
        EmpresaFoto.id == foto_id
    ).first()

    if not foto:
        raise HTTPException(status_code=404, detail="Foto não encontrada")

    foto.principal = True
    db.commit()

    return {"msg": "Foto principal definida"}