import logging
import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class USNewsScraper(BaseScraper):
    """
    Scraper for U.S. News college pages, designed to extract rankings and key
    information.
    """

    # Extensive reject list to filter out irrelevant URLs
    rejectList = [
        "/my-account", "/login", "/register", "mailto:", "javascript:void(0)", "/terms-of-service",
        "/privacy-policy", "/contact-us", "/newsletter", "/about-us", "/careers", "/advertise", "/press",
        "/store", "/site-map", "/faqs", "/subscriptions", "/privacy", "/terms", "/feedback", "/mobile",
        "/rss", "/copyright", "/site-index", "/security", "/do-not-sell", "/cookie-policy",
        "/newsletter-signup", "/disclosures", "/disclaimer", "/forbidden", "/error", "/video", "/photos",
        "/slideshows", "/rankings", "/news", "/opinion", "/travel", "/health", "/money", "/education",
        "/cars", "/best-colleges/rankings", "/best-graduate-schools", "/education/online-education",
        "/education/best-high-schools", "/education/best-global-universities", "/best-colleges?school-name=",
        "/best-colleges/search", "/search", "/directory", "/compare", "/find-a-school", "/financial-aid",
        "/student-life", "/academics", "/crime-safety", "/campus-info", "/save", "/save-school", "/user",
        "/scholarship-search", "/scholarships", "/college-application", "/paying-for-college", 
        "/college-rankings", "/college-finder", "/ask-experts", "/blog", "/donottrack", "/settings",
        "/unsubscribe", "/help", "/shop", "/gift-subscriptions", "/coupons", "/custom-content", 
        "/subscription", "/articles", "/home", "/weather", "/business", "/people", "/topics", "/policy",
        "/politics", "/events", "/world-report", "/article", "/tag", "/videos", "/press-room", 
        "/publications", "/author", "/partners", "/categories", "/collections", "/membership", 
        "/offers", "/galleries", "/media-kit", "/email", "/404", "/500", "facebook.com", "twitter.com", 
        "linkedin.com", "instagram.com", "youtube.com", "pinterest.com", "plus.google.com", 
        "accounts.usnews.com",
    ]

    def __init__(self):
        """
        Initializes the USNewsScraper with the base URL of U.S. News.
        """
        super().__init__(base_url='https://www.usnews.com')

    def scrape(self, url):
        """
        Scrapes the content of a U.S. News college page and returns a structured
        dictionary with rankings and key data.

        Args:
            url (str): The URL of the U.S. News college page to scrape.

        Returns:
            dict: A dictionary containing the scraped data.
        """
        logging.info(f"Visiting: {url}")
        if url in self.visited_urls:
            return

        self.visited_urls.add(url)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            data = {"url": url}

            # Extract the title
            title_element = soup.find('h1')
            data['title'] = title_element.text.strip() if title_element else "No Title"

            # Extract summary content
            summary_element = soup.find('div', class_='SummaryCard__CardContent')
            if summary_element:
                data['summary'] = summary_element.text.strip()

            # Extract rankings and key metrics
            bullet_points = []
            metrics = soup.find_all('li', class_='CardInfo__Item')
            for metric in metrics:
                bullet_points.append(metric.text.strip())
            data['bullet_points'] = bullet_points

            # Extract tables (e.g., tuition, enrollment)
            tables = []
            table_sections = soup.find_all('div', class_='Table__TableContainer')
            for section in table_sections:
                table_data = []
                rows = section.find_all('div', class_='Table__Row')
                for row in rows:
                    cells = row.find_all('div', class_='Table__Cell')
                    cell_text = [cell.text.strip() for cell in cells]
                    table_data.append(cell_text)
                tables.append(table_data)
            data['tables'] = tables

            # Recursively scrape internal links
            for link in soup.find_all('a', href=True):
                next_url = link['href']
                # Check if the URL is absolute or relative
                if next_url.startswith('/'):
                    next_url = self.base_url + next_url
                elif not next_url.startswith('http'):
                    continue  # Skip malformed URLs

                # Reject any unwanted URLs
                if any(substring in next_url for substring in self.rejectList):
                    logging.info(f"Skipping URL: {next_url}")
                    continue

                # Only process URLs that start with the base URL and haven't been visited
                if next_url.startswith(self.base_url) and next_url not in self.visited_urls:
                    logging.info(f"Recursively scraping: {next_url}")
                    self.scrape(next_url)

            return data

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        return {}
