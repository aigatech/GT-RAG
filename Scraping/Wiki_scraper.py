import os
import requests
from bs4 import BeautifulSoup
import re

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def scrape_wiki(url, visited_urls=set(), directory="gt_wiki_scrape"):
    print(f"Visiting: {url}")
    if url in visited_urls:
        return

    visited_urls.add(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = sanitize_filename(f"{url.split('/')[-1]}.txt")
    filepath = os.path.join(directory, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"URL: {url}\n")

        title_element = soup.find('h1', class_='firstHeading')
        data = {}
        if title_element:
            data['title'] = title_element.text.strip()
            f.write(f"Title: {data['title']}\n")
        
        content_element = soup.find('div', id='mw-content-text')
        if content_element:
            paragraphs = content_element.find_all('p')
            data['content'] = [p.text.strip() for p in paragraphs]
            f.write("Content:\n")
            for paragraph in data['content']:
                f.write(f"\t{paragraph}\n")

            for ul in content_element.find_all('ul'):
                f.write("Bullet Points:\n")
                for li in ul.find_all('li'):
                    f.write(f"\t- {li.text.strip()}\n")
            
            for table in content_element.find_all('table'):
                f.write("Table:\n")
                for row in table.find_all('tr'):
                    cells = row.find_all(['th', 'td'])
                    cell_text = [cell.text.strip() for cell in cells]
                    f.write("\t" + "\t|\t".join(cell_text) + "\n")
        
        for link in soup.find_all('a', href=True):
            next_url = link['href']
            if next_url.startswith('/mediawiki/index.php/') and not next_url.endswith('/edit'):  # Filter internal links (excluding edit pages)
                scrape_wiki(f"https://gt-student-wiki.org{next_url}", visited_urls.copy(), directory)

url = 'https://gt-student-wiki.org/mediawiki/index.php/Main_Page'
scrape_wiki(url)
