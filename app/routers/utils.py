from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.empresa_model import Empresa
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
# 🔥 LIMPEZA DO BANCO (ESSENCIAL)
# =========================
@router.delete("/limpar-fotos-quebradas-db")
def limpar_fotos_quebradas(db: Session = Depends(get_db)):
    empresas = db.query(Empresa).all()

    atualizadas = 0

    for emp in empresas:
        if emp.foto_principal and "onrender.com/uploads" in emp.foto_principal:
            emp.foto_principal = None
            atualizadas += 1

    db.commit()

    return {
        "msg": "Fotos quebradas removidas do banco",
        "total": atualizadas
    }