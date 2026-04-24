from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.empresa_model import Empresa
from app.models.empresa_foto_model import EmpresaFoto
import os

router = APIRouter(
    prefix="/utils",
    tags=["Utils"]
)

UPLOAD_DIR = "uploads/empresas"


# =========================
# 🧹 LIMPEZA DE ARQUIVOS LOCAIS
# =========================
@router.delete("/limpar-fotos-antigas")
def limpar_fotos_antigas():
    try:
        if not os.path.exists(UPLOAD_DIR):
            return {"msg": "Pasta não existe"}

        deletadas = 0

        for file in os.listdir(UPLOAD_DIR):
            path = os.path.join(UPLOAD_DIR, file)

            try:
                if os.path.isfile(path):
                    os.remove(path)
                    deletadas += 1
            except Exception as e:
                print("Erro ao deletar:", e)

        return {
            "msg": "Limpeza concluída",
            "arquivos_deletados": deletadas
        }

    except Exception as e:
        print("❌ ERRO:", e)
        return {"erro": "Falha ao limpar arquivos"}


# =========================
# 🔥 LIMPEZA DO BANCO (CORRIGIDA)
# =========================

@router.delete("/limpar-fotos-quebradas-db")
def limpar_fotos_quebradas(db: Session = Depends(get_db)):
    from app.models.empresa_foto_model import EmpresaFoto

    fotos = db.query(EmpresaFoto).all()

    removidas = 0
    corrigidas = 0

    for foto in fotos:
        # 🔥 REMOVE QUALQUER FOTO LOCAL (Render)
        if "onrender.com/uploads" in foto.url:
            db.delete(foto)
            removidas += 1
            continue

        # 🔥 GARANTE URL LIMPA (evita //uploads bugado)
        if "//uploads" in foto.url:
            foto.url = foto.url.replace("//uploads", "/uploads")
            corrigidas += 1

    db.commit()

    return {
        "msg": "Limpeza completa executada",
        "removidas": removidas,
        "corrigidas": corrigidas
    }

@router.delete("/limpar-fotos-locais-do-banco")
def limpar_fotos_locais(db: Session = Depends(get_db)):
    fotos = db.query(EmpresaFoto).all()

    deletadas = 0

    for foto in fotos:
        if foto.url and "uploads/empresas" in foto.url:
            db.delete(foto)
            deletadas += 1

    db.commit()

    return {
        "msg": "Fotos locais removidas do banco",
        "total_deletadas": deletadas
    }