from app.core.security import criar_token

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == data.email).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not pwd_context.verify(data.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Senha inválida")

    token = criar_token({
        "sub": str(usuario.id),
        "is_admin": usuario.is_admin
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }