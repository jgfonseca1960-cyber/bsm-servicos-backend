from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

# ✅ 1. SEMPRE PRIMEIRO
app = FastAPI()

# ✅ 2. DEPOIS TODAS AS ROTAS
@app.get("/add-cep")
def add_cep(db: Session = Depends(get_db)):
    db.execute(text("""
        ALTER TABLE empresas ADD COLUMN IF NOT EXISTS cep VARCHAR
    """))
    db.commit()
    return {"msg": "CEP adicionado!"}