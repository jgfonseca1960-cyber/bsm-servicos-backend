from sqlalchemy import create_engine

url = "postgresql://postgres:123456@localhost:5432/bsm_servicos"

engine = create_engine(url)

conn = engine.connect()

print("OK")