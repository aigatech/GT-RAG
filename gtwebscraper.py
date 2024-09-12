import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

visited_urls = set()
output_folder = 'gt-website-scraped'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def save_page_content(url, content):
    filename = urlparse(url).path.replace('/', '_').strip('_') or 'index'
    filepath = os.path.join(output_folder, f"{filename}.txt")
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(f"URL: {url}\n\n")
        file.write(content)
    print(f"Saved: {filepath}")

def scrape_website(base_url):
    if base_url in visited_urls:
        return
    visited_urls.add(base_url)
    
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed for {base_url}: {e}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"Scraping: {base_url}")
    
    page_text = soup.get_text()
    
    save_page_content(base_url, page_text)

    links = soup.find_all('a', href=True)
    for link in links:
        href = link['href']
        full_url = urljoin(base_url, href)
        
        if urlparse(full_url).netloc == urlparse(base_url).netloc:
            if full_url not in visited_urls:
                time.sleep(1) 
                scrape_website(full_url)

start_url = "https://www.gatech.edu"
scrape_website(start_url)
