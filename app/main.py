from sqlalchemy import text
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db

@app.get("/atualizar-banco")
def atualizar_banco(db: Session = Depends(get_db)):

    # adiciona coluna servico_id
    db.execute(text("""
        ALTER TABLE empresas 
        ADD COLUMN IF NOT EXISTS servico_id INTEGER
    """))

    # cria tabela de fotos
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS empresa_fotos (
            id SERIAL PRIMARY KEY,
            url VARCHAR,
            empresa_id INTEGER REFERENCES empresas(id)
        )
    """))

    db.commit()

    return {"msg": "Banco atualizado com sucesso!"}