@app.get("/add-cep")
def add_cep(db: Session = Depends(get_db)):
    db.execute(text("""
        ALTER TABLE empresas ADD COLUMN IF NOT EXISTS cep VARCHAR
    """))
    db.commit()
    return {"msg": "CEP adicionado!"}