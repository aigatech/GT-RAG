import requests
from bs4 import BeautifulSoup

def scrape_georgia_tech_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('title').get_text()
    content = ' '.join([p.get_text() for p in soup.find_all('p')])

    return {
        "title": title,
        "content": content,
        "url": url
    }
