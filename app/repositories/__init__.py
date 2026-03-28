def init_db():
    print("🔥 Resetando banco...")

    import app.models

    Base.metadata.create_all(bind=engine)

    criar_admin()

    print("✅ Banco pronto!")