from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario_model import Usuario
from app.core.security import verify_password, create_access_token
from app.schemas.auth_schema import LoginRequest

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# ✅ LOGIN PARA SWAGGER (FORM-DATA)
@router.post("/login")
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(Usuario).filter(
        Usuario.email == form_data.username
    ).first()

    if not user or not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(status_code=400, detail="Email ou senha inválidos")

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ✅ LOGIN PARA FLUTTER (JSON)
@router.post("/login-json")
def login_json(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(Usuario).filter(
        Usuario.email == data.email
    ).first()

    if not user or not verify_password(data.password, user.senha_hash):
        raise HTTPException(status_code=400, detail="Email ou senha inválidos")

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }