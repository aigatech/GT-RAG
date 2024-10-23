import os
import time
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

class GTWebsiteScraper:
    def __init__(self, base_url, output_folder='gt-website-scraped'):
        self.visited_urls = set()
        self.base_url = base_url
        self.output_folder = output_folder
        
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def save_page_content(self, url, content):
        filename = urlparse(url).path.replace('/', '_').strip('_') or 'index'
        filepath = os.path.join(self.output_folder, f"{filename}.txt")
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(f"URL: {url}\n\n")
            file.write(content)
        print(f"Saved: {filepath}")

    def scrape_website(self, base_url, depth=0, max_depth=3):
        if base_url in self.visited_urls or depth > max_depth:
            return
        self.visited_urls.add(base_url)
        
        try:
            response = requests.get(base_url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
        except requests.RequestException as e:
            print(f"Request failed for {base_url}: {e}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"Scraping: {base_url}")
        
        page_text = soup.get_text()
        self.save_page_content(base_url, page_text)

        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            if not urlparse(href).scheme and not href.startswith('/'):
                continue
            full_url = urljoin(base_url, href)
            
            if urlparse(full_url).netloc.lower() == urlparse(base_url).netloc.lower():
                if full_url not in self.visited_urls:
                    time.sleep(1)
                    self.scrape_website(full_url, depth + 1)

    def start_scraping(self):
        self.scrape_website(self.base_url)

# Initialize and start scraping
if __name__ == '__main__':
    base_url = 'https://www.gatech.edu'
    scraper = GTWebsiteScraper(base_url)
    scraper.start_scraping()
