from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.empresa_model import Empresa

router = APIRouter()  # ❗ SEM prefixo aqui


# =========================
# 📌 LISTAR EMPRESAS
# =========================
@router.get("/empresas")
def listar_empresas(db: Session = Depends(get_db)):
    try:
        empresas = db.query(Empresa).all()

        resultado = []
        for e in empresas:
            resultado.append({
                "id": e.id,
                "nome": getattr(e, "nome", ""),
                "telefone": getattr(e, "telefone", ""),
                "email": getattr(e, "email", ""),
                "endereco": getattr(e, "endereco", ""),
                "latitude": getattr(e, "latitude", None),
                "longitude": getattr(e, "longitude", None),
            })

        return resultado

    except Exception as e:
        print("❌ ERRO LISTAR EMPRESAS:", str(e))
        return {"erro": str(e)}


# =========================
# 🔥 ROTA COMPATÍVEL
# =========================
@router.get("/listar")
def listar_empresas_compat(db: Session = Depends(get_db)):
    return listar_empresas(db)


# =========================
# 🔍 DETALHAR EMPRESA
# =========================
@router.get("/detalhe/{empresa_id}")
def detalhe_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return {
        "id": empresa.id,
        "nome": getattr(empresa, "nome", ""),
        "telefone": getattr(empresa, "telefone", ""),
        "email": getattr(empresa, "email", ""),
        "endereco": getattr(empresa, "endereco", ""),
        "latitude": getattr(empresa, "latitude", None),
        "longitude": getattr(empresa, "longitude", None),
    }


# =========================
# ➕ CRIAR EMPRESA
# =========================
@router.post("/")
def criar_empresa(data: dict, db: Session = Depends(get_db)):
    try:
        empresa = Empresa(**data)

        db.add(empresa)
        db.commit()
        db.refresh(empresa)

        return {"msg": "Empresa criada com sucesso", "id": empresa.id}

    except Exception as e:
        print("❌ ERRO CRIAR EMPRESA:", str(e))
        return {"erro": str(e)}


# =========================
# ✏️ ATUALIZAR EMPRESA
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

        return {"msg": "Empresa atualizada com sucesso"}

    except Exception as e:
        print("❌ ERRO ATUALIZAR:", str(e))
        return {"erro": str(e)}


# =========================
# ❌ DELETAR EMPRESA
# =========================
@router.delete("/{empresa_id}")
def deletar_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    try:
        db.delete(empresa)
        db.commit()

        return {"msg": "Empresa deletada com sucesso"}

    except Exception as e:
        print("❌ ERRO DELETAR:", str(e))
        return {"erro": str(e)}
