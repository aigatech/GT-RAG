import psycopg2
from .config import settings

def get_db_connection():
    conn = psycopg2.connect(settings.POSTGRES_URL)
    return conn

def setup_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Create table for storing embeddings if it doesn't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS embeddings (
        id SERIAL PRIMARY KEY,
        title TEXT,
        url TEXT,
        embedding VECTOR(%s),
        content TEXT
    );
    """, (settings.PGVECTOR_DIMENSION,))

    conn.commit()
    cur.close()
    conn.close()
