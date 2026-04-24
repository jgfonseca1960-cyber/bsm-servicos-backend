from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.empresa_model import Empresa
from app.models.empresa_foto_model import EmpresaFoto

router = APIRouter(prefix="/utils", tags=["Utils"])


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
        "msg": "Fotos locais removidas",
        "total": deletadas
    }


@router.put("/corrigir-fotos-principais")
def corrigir_principal(db: Session = Depends(get_db)):
    empresas = db.query(Empresa).all()

    corrigidas = 0

    for emp in empresas:
        if not emp.fotos:
            continue

        if not any(f.principal for f in emp.fotos):
            emp.fotos[0].principal = True
            corrigidas += 1

    db.commit()

    return {"msg": "Corrigido", "total": corrigidas}