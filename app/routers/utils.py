from fastapi import APIRouter
import os

router = APIRouter(
    prefix="/utils",
    tags=["Utils"]
)

UPLOAD_DIR = "uploads/empresas"


@router.delete("/limpar-fotos-antigas")
def limpar_fotos_antigas():
    if not os.path.exists(UPLOAD_DIR):
        return {"msg": "Pasta não existe"}

    deletadas = 0

    for file in os.listdir(UPLOAD_DIR):
        path = os.path.join(UPLOAD_DIR, file)

        if os.path.isfile(path):
            os.remove(path)
            deletadas += 1

    return {
        "msg": "Limpeza concluída",
        "arquivos_deletados": deletadas
    }