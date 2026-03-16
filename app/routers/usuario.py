from fastapi import APIRouter, Depends
from app.core.deps import get_current_user
from app.models.usuario_model import Usuario

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.get("/me")
def me(
    user: Usuario = Depends(get_current_user)
):
    return {
        "id": user.id,
        "nome": user.nome,
        "email": user.email
    }