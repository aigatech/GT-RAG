import psycopg2
from .config import settings
from .embeddings import generate_embedding

def query_embeddings(query):
    query_emb = generate_embedding(query)

    conn = psycopg2.connect(settings.POSTGRES_URL)
    cur = conn.cursor()

    cur.execute("""
    SELECT title, url, content
    FROM embeddings
    ORDER BY embedding <-> %s
    LIMIT 1;
    """, (query_emb,))

    result = cur.fetchone()
    cur.close()
    conn.close()

    return result
