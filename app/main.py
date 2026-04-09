from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

app = FastAPI()

@app.get("/ver-colunas")
def ver_colunas(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'empresas'
    """))
    return [row[0] for row in result]