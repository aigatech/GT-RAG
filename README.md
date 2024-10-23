# Georgia Tech Embedding Pipeline

This repository contains a pipeline that processes scraped data, generates embeddings using NVIDIA NIM embeddings, and stores them in a PostgreSQL database with `pgvector`.

## Setup Instructions

1. Install PostgreSQL with `pgvector` extension:
   ```bash
   sudo apt-get install postgresql
   psql -c "CREATE EXTENSION vector;"
