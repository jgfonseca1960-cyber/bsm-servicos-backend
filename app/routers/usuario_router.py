s
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario_model import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.get("/")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()

    return [
        {
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "tipo_usuario": u.tipo_usuario
        }
        for u in usuarios
    ]