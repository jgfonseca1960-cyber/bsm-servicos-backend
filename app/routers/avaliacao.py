from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db

from app.models.avaliacao_model import Avaliacao
from app.models.empresa_model import Empresa
from app.models.servico_model import Servico

from app.schemas.avaliacao_schema import (
    AvaliacaoCreate,
    AvaliacaoResponse
)

from sqlalchemy import desc

from app.models.user import User

router = APIRouter(
    prefix="/avaliacoes",
    tags=["Avaliações"]
)

# =========================================================
# 🔧 CALCULAR MÉDIA
# =========================================================

def calcular_media(
    db: Session,
    empresa_id: int
):
    return db.query(
        func.avg(Avaliacao.nota)
    ).filter(
        Avaliacao.empresa_id == empresa_id
    ).scalar()


# =========================================================
# 🔄 ATUALIZAR MÉDIA EMPRESA
# =========================================================

def atualizar_media_empresa(
    db: Session,
    empresa_id: int
):

    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        return

    media = calcular_media(
        db,
        empresa_id
    )

    empresa.avaliacao_media = round(
        media or 0,
        1
    )

# =========================================================
# ⭐ CRIAR AVALIAÇÃO
# =========================================================

@router.post(
    "/",
    response_model=AvaliacaoResponse,
    status_code=status.HTTP_201_CREATED
)
def criar(
    av: AvaliacaoCreate,
    db: Session = Depends(get_db)
):

    empresa = db.query(Empresa).filter(
        Empresa.id == av.empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    existe = db.query(Avaliacao).filter(
        Avaliacao.usuario_id == av.usuario_id,
        Avaliacao.empresa_id == av.empresa_id
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Usuário já avaliou esta empresa"
        )

    if av.nota < 1 or av.nota > 5:
        raise HTTPException(
            status_code=400,
            detail="A nota deve ser entre 1 e 5"
        )

    nova = Avaliacao(
        empresa_id=av.empresa_id,
        usuario_id=av.usuario_id,
        nota=av.nota,
        comentario=av.comentario
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)

    atualizar_media_empresa(
        db,
        av.empresa_id
    )

    db.commit()

    return nova

    
# =========================================================
# 📋 LISTAR TODAS
# =========================================================

@router.get("/")
def listar(
    db: Session = Depends(get_db)
):

    return db.query(
        Avaliacao
    ).order_by(
        Avaliacao.id.desc()
    ).all()


# =========================================================
# 🏢 LISTAR POR EMPRESA
# =========================================================

@router.get("/empresa/{empresa_id}")
def por_empresa(
    empresa_id: int,
    db: Session = Depends(get_db)
):

    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    avaliacoes = db.query(
        Avaliacao
    ).filter(
        Avaliacao.empresa_id == empresa_id
    ).order_by(
        Avaliacao.id.desc()
    ).all()

    return avaliacoes
    
   
# =========================================================
# ⭐ MÉDIA DA EMPRESA
# =========================================================

@router.get("/media/{empresa_id}")
def media(
    empresa_id: int,
    db: Session = Depends(get_db)
):

    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    media = calcular_media(
        db,
        empresa_id
    )

    return {
        "empresa_id": empresa_id,
        "media": round(media or 0, 1)
    }


# =========================================================
# 🏆 RANKING EMPRESAS
# =========================================================

@router.get("/ranking")
def ranking(
    db: Session = Depends(get_db)
):

    resultado = (
        db.query(
            Empresa.id,
            Empresa.nome,
            func.coalesce(
                func.avg(Avaliacao.nota),
                0
            ).label("media"),
            func.count(
                Avaliacao.id
            ).label("total_avaliacoes")
        )
        .outerjoin(
            Avaliacao,
            Avaliacao.empresa_id == Empresa.id
        )
        .group_by(
            Empresa.id,
            Empresa.nome
        )
        .order_by(
            func.coalesce(
                func.avg(Avaliacao.nota),
                0
            ).desc(),
            func.count(
                Avaliacao.id
            ).desc()
        )
        .all()
    )

    return [
        {
            "empresa_id": item.id,
            "nome": item.nome,
            "media": round(item.media, 1),
            "total_avaliacoes": item.total_avaliacoes
        }
        for item in resultado
    ]

# =========================================================
# 🗑️ EXCLUIR AVALIAÇÃO
# =========================================================

@router.delete("/{avaliacao_id}")
def excluir_avaliacao(
    avaliacao_id: int,
    db: Session = Depends(get_db)
):

    avaliacao = db.query(Avaliacao).filter(
        Avaliacao.id == avaliacao_id
    ).first()

    if not avaliacao:
        raise HTTPException(
            status_code=404,
            detail="Avaliação não encontrada"
        )

    empresa_id = avaliacao.empresa_id

    db.delete(avaliacao)
    db.commit()

    atualizar_media_empresa(
        db,
        empresa_id
    )

    db.commit()

    return {
        "message": "Avaliação removida com sucesso"
    }

# =========================================================
# RESUMO AVALIAÇÃO
# =========================================================


@router.get("/resumo")
def resumo(db: Session = Depends(get_db)):

    total_empresas = db.query(Empresa).count()

    total_servicos = db.query(Servico).count()

    total_avaliacoes = db.query(Avaliacao).count()

    empresas_avaliadas = (
        db.query(Empresa)
        .filter(Empresa.avaliacao_media > 0)
        .count()
    )

    empresas_sem_avaliacao = (
        total_empresas - empresas_avaliadas
    )

    media = db.query(
        func.avg(Empresa.avaliacao_media)
    ).scalar()

    return {

        "total_usuarios": db.query(User).count(),

        "total_empresas": total_empresas,

        "total_servicos": total_servicos,

        "total_avaliacoes": total_avaliacoes,

        "empresas_avaliadas": empresas_avaliadas,

        "empresas_sem_avaliacao": empresas_sem_avaliacao,

        "media_geral": round(media or 0,1),
      
    }

    # =========================================================
# DASHBOARD ADMIN
# =========================================================

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):

    total_empresas = db.query(Empresa).count()

    total_servicos = db.query(Servico).count()

    total_avaliacoes = db.query(Avaliacao).count()

    empresas_avaliadas = (
        db.query(Empresa)
        .filter(Empresa.avaliacao_media > 0)
        .count()
    )

    empresas_sem_avaliacao = (
        total_empresas - empresas_avaliadas
    )

    media_geral = db.query(
        func.avg(Empresa.avaliacao_media)
    ).scalar()

    # ==========================================
    # RANKING
    # ==========================================

    ranking = (
        db.query(
            Empresa.id,
            Empresa.nome,
            func.coalesce(
                func.avg(Avaliacao.nota),
                0
            ).label("media"),
            func.count(
                Avaliacao.id
            ).label("total_avaliacoes")
        )
        .outerjoin(
            Avaliacao,
            Avaliacao.empresa_id == Empresa.id
        )
        .group_by(
            Empresa.id,
            Empresa.nome
        )
        .order_by(
            desc("media"),
            desc("total_avaliacoes")
        )
        .limit(10)
        .all()
    )

    ranking_json = [

        {
            "empresa_id": item.id,
            "nome": item.nome,
            "media": round(item.media,1),
            "total_avaliacoes": item.total_avaliacoes
        }

        for item in ranking

    ]

    # ==========================================
    # PIORES EMPRESAS
    # ==========================================

    piores = (
        db.query(
            Empresa.id,
            Empresa.nome,
            func.coalesce(
                func.avg(Avaliacao.nota),
                0
            ).label("media"),
            func.count(
                Avaliacao.id
            ).label("total_avaliacoes")
        )
        .outerjoin(
            Avaliacao,
            Avaliacao.empresa_id == Empresa.id
        )
        .group_by(
            Empresa.id,
            Empresa.nome
        )
        .having(
            func.count(Avaliacao.id) > 0
        )
        .order_by(
            "media"
        )
        .limit(10)
        .all()
    )

    piores_json = [

        {
            "empresa_id": item.id,
            "nome": item.nome,
            "media": round(item.media,1),
            "total_avaliacoes": item.total_avaliacoes
        }

        for item in piores

    ]

    # ==========================================
    # ÚLTIMAS AVALIAÇÕES
    # ==========================================

    ultimas = (
        db.query(
            Avaliacao,
            Empresa.nome
        )
        .join(
            Empresa,
            Empresa.id == Avaliacao.empresa_id
        )
        .order_by(
            Avaliacao.id.desc()
        )
        .limit(10)
        .all()
    )

    ultimas_json = []

    for av, empresa_nome in ultimas:

        ultimas_json.append({

            "id": av.id,

            "empresa": empresa_nome,

            "empresa_id": av.empresa_id,

            "usuario_id": av.usuario_id,

            "nota": av.nota,

            "comentario": av.comentario

        })

    # ==========================================
    # DISTRIBUIÇÃO DAS NOTAS
    # ==========================================

    estatisticas = {}

    for nota in range(1,6):

        quantidade = (
            db.query(Avaliacao)
            .filter(Avaliacao.nota == nota)
            .count()
        )

        estatisticas[f"nota{nota}"] = quantidade

    return {

        "resumo":{

            "total_empresas": total_empresas,

            "total_servicos": total_servicos,

            "total_avaliacoes": total_avaliacoes,

            "empresas_avaliadas": empresas_avaliadas,

            "empresas_sem_avaliacao": empresas_sem_avaliacao,

            "media_geral": round(media_geral or 0,1)

        },

        "ranking": ranking_json,

        "piores": piores_json,

        "estatisticas": estatisticas,

        "ultimas_avaliacoes": ultimas_json

    }