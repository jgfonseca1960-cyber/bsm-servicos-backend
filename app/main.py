from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

# 👇 PRIMEIRO cria o app
app = FastAPI()

# 👇 DEPOIS as rotas
@app.get("/atualizar-banco")
def atualizar_banco(db: Session = Depends(get_db)):

    db.execute(text("""
        ALTER TABLE empresas 
        ADD COLUMN IF NOT EXISTS servico_id INTEGER
    """))

    db.execute(text("""
        CREATE TABLE IF NOT EXISTS empresa_fotos (
            id SERIAL PRIMARY KEY,
            url VARCHAR,
            empresa_id INTEGER REFERENCES empresas(id)
        )
    """))

    db.commit()

    return {"msg": "Banco atualizado com sucesso!"}