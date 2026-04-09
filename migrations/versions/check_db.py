from sqlalchemy import create_engine, text
import os

# Pegando a URL do banco (Render normalmente fornece isso)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL não encontrada nas variáveis de ambiente")

engine = create_engine(DATABASE_URL)

queries = {
    "FKs que dependem de tipos_servico": """
        SELECT conname, conrelid::regclass AS table_name
        FROM pg_constraint
        WHERE confrelid = 'tipos_servico'::regclass;
    """,

    "Foreign keys apontando para tipos_servico": """
        SELECT
            tc.constraint_name,
            tc.table_name,
            ccu.table_name AS referenced_table
        FROM information_schema.table_constraints tc
        JOIN information_schema.constraint_column_usage ccu
            ON tc.constraint_name = ccu.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
        AND ccu.table_name = 'tipos_servico';
    """,

    "Constraints da tabela empresa_tipo_servico": """
        SELECT
            tc.constraint_name,
            tc.table_name,
            kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
        WHERE tc.table_name = 'empresa_tipo_servico';
    """
}

with engine.connect() as conn:
    for title, query in queries.items():
        print("\n==============================")
        print(f"{title}")
        print("==============================")

        result = conn.execute(text(query))
        rows = result.fetchall()

        if not rows:
            print("Nenhum resultado encontrado ✅")
        else:
            for row in rows:
                print(row)