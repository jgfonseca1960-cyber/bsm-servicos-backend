from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioOut

router = APIRouter(prefix="/usuario", tags=["Usuario"])


@router.post("/", response_model=UsuarioOut)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):

    existe = db.query(Usuario).filter(
        Usuario.email == usuario.email
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )

    novo = Usuario(
        email=usuario.email,
        senha=usuario.senha,
        is_admin=True
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo