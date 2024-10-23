from .scrapers.georgia_tech_scraper import scrape_georgia_tech_article
from .embeddings import generate_embedding
from .database import setup_db, get_db_connection

def add_embedding_to_db(title, url, content):
    conn = get_db_connection()
    cur = conn.cursor()

    embedding = generate_embedding(content)

    cur.execute(
        "INSERT INTO embeddings (title, url, embedding, content) VALUES (%s, %s, %s, %s)",
        (title, url, embedding, content)
    )

    conn.commit()
    cur.close()
    conn.close()

def run_pipeline():
    setup_db()

    # Example URLs for scraping
    urls = [
        "https://news.gatech.edu/news/2024/09/05/mrna-and-gene-editing-tools-offer-new-hope-dengue-virus-treatment"
    ]

    for url in urls:
        article = scrape_georgia_tech_article(url)
        add_embedding_to_db(article['title'], article['url'], article['content'])

if __name__ == "__main__":
    run_pipeline()
