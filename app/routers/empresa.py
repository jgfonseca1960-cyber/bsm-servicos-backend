from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import SessionLocal
from app.models.empresa_model import Empresa
from app.models.usuario_model import Usuario
from app.models.avaliacao_model import Avaliacao
from app.schemas.empresa_schema import EmpresaCreate, EmpresaResponse
from app.core.security import verificar_token, get_password_hash
from math import radians, cos, sin, asin, sqrt
from app.database import get_db
from app.models.usuario import Usuario
from app.auth import get_current_user


router = APIRouter(prefix="/empresas", tags=["Empresas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def criar_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):

    nova_empresa = Empresa(
        nome=empresa.nome,
        cidade=empresa.cidade,
        categoria=empresa.categoria,
        usuario_id=usuario.id
    )

    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)

    return nova_empresa

@router.get("/ranking")
def ranking(db: Session = Depends(get_db)):
    res = db.query(
        Empresa.nome,
        func.avg(Avaliacao.nota).label("media"),
        func.count(Avaliacao.id).label("total_avaliacoes")
    ).join(Avaliacao, Avaliacao.empresa_id == Empresa.id, isouter=True)\
     .group_by(Empresa.id).order_by(func.avg(Avaliacao.nota).desc()).all()

    return [{"empresa": r[0], "media": float(r[1] or 0), "total_avaliacoes": r[2]} for r in res]

@router.get("/buscar")
def buscar(servico: str, cidade: str, db: Session = Depends(get_db)):
    empresas = db.query(Empresa).filter(
        Empresa.tipo_servico.ilike(f"%{servico}%"),
        Empresa.cidade.ilike(f"%{cidade}%")
    ).all()
    return empresas

def calcular_distancia(lat1, lon1, lat2, lon2):

    # fórmula haversine
    lon1, lat1, lon2, lat2 = map(radians,
    [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    km = 6371 * c

    return km

@router.get("/proximas")
def empresas_proximas(
    latitude: float,
    longitude: float,
    db: Session = Depends(get_db)
):

    empresas = db.query(Empresa).all()

    resultado = []

    for empresa in empresas:

        distancia = calcular_distancia(
            latitude,
            longitude,
            empresa.latitude,
            empresa.longitude
        )

        resultado.append({
            "id": empresa.id,
            "nome": empresa.nome,
            "tipo_servico": empresa.tipo_servico,
            "distancia_km": round(distancia, 2)
        })

    resultado.sort(key=lambda x: x["distancia_km"])

    return resultado