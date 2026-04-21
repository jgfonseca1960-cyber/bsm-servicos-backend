from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os
import shutil
import uuid

from app.database import get_db
from app.models.empresa_model import Empresa
from app.models.foto_model import Foto
from app.models.avaliacao_model import Avaliacao

from app.schemas.empresa_schema import EmpresaCreate, EmpresaUpdate

router = APIRouter(
    prefix="/empresa",  # 🔥 PADRÃO CORRETO
    tags=["Empresa"]
)

# =========================
# 📁 CONFIG UPLOAD
# =========================
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# =========================
# 📸 UPLOAD DE FOTO
# =========================
@router.post("/{empresa_id}/upload")
def upload_foto(
    empresa_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    foto = Foto(
        empresa_id=empresa_id,
        caminho=f"/uploads/{filename}",
        principal=False
    )

    db.add(foto)
    db.commit()
    db.refresh(foto)

    return {"url": foto.caminho}


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
def listar_empresas(db: Session = Depends(get_db)):
    empresas = db.query(Empresa).all()
    resultado = []

    for e in empresas:
        fotos = db.query(Foto).filter(Foto.empresa_id == e.id).all()

        avaliacoes = db.query(Avaliacao).filter(
            Avaliacao.empresa_id == e.id
        ).all()

        media = 0
        if avaliacoes:
            media = sum([a.nota for a in avaliacoes]) / len(avaliacoes)

        lista_fotos = [
            {
                "id": f.id,
                "url": f.caminho
            }
            for f in fotos
        ]

        resultado.append({
            "id": e.id,
            "nome": e.nome,
            "descricao": e.descricao,
            "telefone": e.telefone,
            "email": getattr(e, "email", None),

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
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    fotos = db.query(Foto).filter(
        Foto.empresa_id == empresa.id
    ).all()

    avaliacoes = db.query(Avaliacao).filter(
        Avaliacao.empresa_id == empresa.id
    ).all()

    media = 0
    if avaliacoes:
        media = sum([a.nota for a in avaliacoes]) / len(avaliacoes)

    lista_fotos = [
        {
            "id": f.id,
            "url": f.caminho
        }
        for f in fotos
    ]

    return {
        "id": empresa.id,
        "nome": empresa.nome,
        "descricao": empresa.descricao,
        "telefone": empresa.telefone,
        "email": getattr(empresa, "email", None),

        "endereco": empresa.endereco,
        "bairro": empresa.bairro,
        "cidade": empresa.cidade,
        "estado": empresa.estado,
        "cep": empresa.cep,

        "latitude": empresa.latitude,
        "longitude": empresa.longitude,

        "avaliacao_media": media,
        "servico_id": empresa.servico_id,

        "fotos": lista_fotos
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
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    update_data = dados.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(empresa, key, value)

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
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    db.delete(empresa)
    db.commit()

    return {"message": "Empresa removida com sucesso"}