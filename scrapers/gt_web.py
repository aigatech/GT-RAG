import os
import time
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

class GTWebsiteScraper:
    # Extensive reject list to filter out irrelevant URLs
    rejectList = [
        "login",
        "signin",
        "signup",
        "register",
        "logout",
        "contact",
        "terms",
        "privacy",
        "search",
        "mailto:",
        "javascript:void(0)",
        "facebook.com",
        "twitter.com",
        "instagram.com",
        "linkedin.com",
        "youtube.com",
        "plus.google.com",
        "pinterest.com",
        "reddit.com",
        "mailto:",
        "/calendar",
        "/events",
        "/news",
        "/rss",
        "/feed",
        "/subscribe",
        "/unsubscribe",
        "/contact",
        "/contact-us",
        "/help",
        "/support",
        "/faq",
        "/faqs",
        "/feedback",
        "/donate",
        "/giving",
        "/sitemap",
        "/jobs",
        "/careers",
        "/employment",
        "/legal",
        "/policy",
        "/copyright",
        "/disclaimer",
        "/non-discrimination",
        "/accessibility",
        "/ethics",
        "/emergency",
        "/compliance",
        "/police",
        "/title-ix",
        "/incident-reporting",
        "/conduct",
        "/student-conduct",
        "/faculty-handbook",
        "/staff-handbook",
        "/student-handbook",
        "/policy-library",
        "/commencement",
        "/orientation",
        "/faculty-directory",
        "/staff-directory",
        "/student-directory",
        "/parking",
        "/transit",
        "/bus",
        "/shuttle",
        "/housing",
        "/dining",
        "/bookstore",
        "/library",
        "/lost-and-found",
        "/payroll",
        "/benefits",
        "/hr",
        "/human-resources",
        "/bursar",
        "/admission",
        "/financial-aid",
        "/scholarships",
        "/loans",
        "/study-abroad",
        "/internships",
        "/co-op",
        "/athletics",
        "/sports",
        "/recreation",
        "/clubs",
        "/organizations",
        "/activities",
        "/counseling",
        "/health-services",
        "/blog",
        "/newsletter",
        "/press",
        "/media",
        "/social-media",
        "/cookies",
        "/settings",
        "/preferences",
        "/error",
        "/404",
        "/500",
        "mailto:",
        "javascript:void(0)"
    ]

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

    def scrape_website(self, base_url):
        if base_url in self.visited_urls:
            return
        self.visited_urls.add(base_url)

        try:
            response = requests.get(base_url)
            response.raise_for_status()
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
            
            # Ignore anchor links
            if '#' in href:
                continue

            full_url = urljoin(base_url, href)

            # Normalize URLs by removing 'www.'
            full_url = full_url.replace("www.", "")

            parsed_full_url = urlparse(full_url)

            # Check if the URL is within the 'gatech.edu' domain
            if parsed_full_url.netloc.endswith('gatech.edu'):
                # Reject any unwanted URLs
                if any(substring in full_url for substring in self.rejectList):
                    continue
                if full_url not in self.visited_urls:
                    time.sleep(1)  # Add delay to avoid overwhelming the server
                    self.scrape_website(full_url)


    def start_scraping(self):
        self.scrape_website(self.base_url)