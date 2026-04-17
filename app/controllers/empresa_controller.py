from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.empresa_model import Empresa

router = APIRouter()


# =========================
# 📌 LISTAR EMPRESAS
# =========================
@router.get("/empresas")
def listar_empresas(db: Session = Depends(get_db)):
    try:
        empresas = db.query(Empresa).all()

        return [
            {
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
            }
            for e in empresas
        ]

    except Exception as e:
        print("❌ ERRO LISTAR EMPRESAS:", str(e))
        return {"erro": str(e)}


# =========================
# 🔥 COMPATIBILIDADE
# =========================
@router.get("/listar")
def listar_empresas_compat(db: Session = Depends(get_db)):
    return listar_empresas(db)


# =========================
# 🔍 DETALHAR
# =========================
@router.get("/detalhe/{empresa_id}")
def detalhe_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return {
        "id": empresa.id,
        "nome": empresa.nome,
        "descricao": empresa.descricao,
        "telefone": empresa.telefone,
        "endereco": empresa.endereco,
        "bairro": empresa.bairro,
        "cidade": empresa.cidade,
        "estado": empresa.estado,
        "cep": empresa.cep,
        "latitude": empresa.latitude,
        "longitude": empresa.longitude,
        "ativo": empresa.ativo,
        "avaliacao_media": empresa.avaliacao_media,
        "cpf": empresa.cpf,
        "cnpj": empresa.cnpj,
        "servico_id": empresa.servico_id,
    }


# =========================
# ➕ CRIAR
# =========================
@router.post("/")
def criar_empresa(data: dict, db: Session = Depends(get_db)):
    try:
        empresa = Empresa(**data)

        db.add(empresa)
        db.commit()
        db.refresh(empresa)

        return {"msg": "Empresa criada", "id": empresa.id}

    except Exception as e:
        print("❌ ERRO CRIAR:", str(e))
        return {"erro": str(e)}


# =========================
# ✏️ ATUALIZAR
# =========================
@router.put("/{empresa_id}")
def atualizar_empresa(empresa_id: int, data: dict, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    try:
        for key, value in data.items():
            setattr(empresa, key, value)

        db.commit()
        db.refresh(empresa)

        return {"msg": "Empresa atualizada"}

    except Exception as e:
        print("❌ ERRO UPDATE:", str(e))
        return {"erro": str(e)}


# =========================
# ❌ DELETAR
# =========================
@router.delete("/{empresa_id}")
def deletar_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    try:
        db.delete(empresa)
        db.commit()

        return {"msg": "Empresa deletada"}

    except Exception as e:
        print("❌ ERRO DELETE:", str(e))
        return {"erro": str(e)}