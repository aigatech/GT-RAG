CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS embeddings (
    id SERIAL PRIMARY KEY,
    title TEXT,
    url TEXT,
    embedding VECTOR(4096),  
    content TEXT
);
