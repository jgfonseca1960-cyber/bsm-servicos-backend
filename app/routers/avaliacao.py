from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.avaliacao_model import Avaliacao
from app.models.empresa_model import Empresa
from app.schemas.avaliacao_schema import AvaliacaoCreate


router = APIRouter(
    prefix="/avaliacoes",
    tags=["Avaliações"]
)


# =========================
# 🔥 FUNÇÃO AUXILIAR: atualizar média
# =========================
def atualizar_media_empresa(db: Session, empresa_id: int):

    media = db.query(func.avg(Avaliacao.nota)).filter(
        Avaliacao.empresa_id == empresa_id
    ).scalar()

    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if empresa:
        empresa.avaliacao_media = round(media or 0, 1)
        db.commit()


# =========================
# ⭐ CRIAR AVALIAÇÃO
# =========================
@router.post("/")
def criar(av: AvaliacaoCreate, db: Session = Depends(get_db)):

    existe = db.query(Avaliacao).filter(
        Avaliacao.usuario_id == av.usuario_id,
        Avaliacao.empresa_id == av.empresa_id
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Usuário já avaliou esta empresa"
        )

    nova = Avaliacao(**av.dict())

    db.add(nova)
    db.commit()
    db.refresh(nova)

    # 🔥 atualiza média automaticamente
    atualizar_media_empresa(db, av.empresa_id)

    return nova


# =========================
# 📋 LISTAR TODAS
# =========================
@router.get("/")
def listar(db: Session = Depends(get_db)):
    return db.query(Avaliacao).all()


# =========================
# 🏢 LISTAR POR EMPRESA
# =========================
@router.get("/empresa/{empresa_id}")
def por_empresa(empresa_id: int, db: Session = Depends(get_db)):

    return db.query(Avaliacao).filter(
        Avaliacao.empresa_id == empresa_id
    ).all()


# =========================
# ⭐ MÉDIA DA EMPRESA
# =========================
@router.get("/media/{empresa_id}")
def media(empresa_id: int, db: Session = Depends(get_db)):

    m = db.query(func.avg(Avaliacao.nota)).filter(
        Avaliacao.empresa_id == empresa_id
    ).scalar()

    return {
        "empresa_id": empresa_id,
        "media": round(m or 0, 1)
    }


# =========================
# 🏆 RANKING DE EMPRESAS
# =========================
@router.get("/ranking")
def ranking(db: Session = Depends(get_db)):

    r = db.query(
        Avaliacao.empresa_id,
        func.avg(Avaliacao.nota).label("media"),
        func.count(Avaliacao.id).label("total")
    ).group_by(
        Avaliacao.empresa_id
    ).order_by(
        func.avg(Avaliacao.nota).desc()
    ).all()

    return [
        {
            "empresa_id": item.empresa_id,
            "media": round(item.media or 0, 1),
            "total_avaliacoes": item.total
        }
        for item in r
    ]