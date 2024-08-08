import logging
import os
import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class GTWikiScraper(BaseScraper):
    """
    A scraper for the Georgia Tech Student Wiki. Inherits from BaseScraper and
    implements the specific scraping logic for the GT Wiki.
    """

    def __init__(self):
        """
        Initializes the GTWikiScraper with the base URL of the GT Student Wiki.
        """
        super().__init__(base_url='https://gt-student-wiki.org')

    def scrape(self, url):
        """
        Scrapes the content of a given GT Wiki page and stores it in a text file.
        Recursively follows internal links to scrape connected pages.

        Args:
            url (str): The URL of the GT Wiki page to scrape.
        """
        logging.info(f"Visiting: {url}")
        if url in self.visited_urls:
            return

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            soup = BeautifulSoup(response.content, 'html.parser')

            if not os.path.exists(self.directory):
                os.makedirs(self.directory)  # Create directory if it doesn't exist

            # Create a sanitized filename based on the URL
            filename = self.sanitize_filename(f"{url.split('/')[-1]}.txt")
            filepath = os.path.join(self.directory, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"URL: {url}\n")

                # Extract and write the title of the page
                title_element = soup.find('h1', class_='firstHeading')
                if title_element:
                    title = title_element.text.strip()
                    f.write(f"Title: {title}\n")

                # Extract and write the main content of the page
                content_element = soup.find('div', id='mw-content-text')
                if content_element:
                    paragraphs = content_element.find_all('p')
                    f.write("Content:\n")
                    for paragraph in paragraphs:
                        f.write(f"\t{paragraph.text.strip()}\n")

                    # Extract and write bullet points
                    for ul in content_element.find_all('ul'):
                        f.write("Bullet Points:\n")
                        for li in ul.find_all('li'):
                            f.write(f"\t- {li.text.strip()}\n")

                    # Extract and write tables
                    for table in content_element.find_all('table'):
                        f.write("Table:\n")
                        for row in table.find_all('tr'):
                            cells = row.find_all(['th', 'td'])
                            cell_text = [cell.text.strip() for cell in cells]
                            f.write("\t" + "\t|\t".join(cell_text) + "\n")

                self.visited_urls.add(url)  # Mark the URL as visited

                # Recursively scrape internal links
                for link in soup.find_all('a', href=True):
                    next_url = link['href']
                    if next_url.startswith('/mediawiki/index.php/') and not next_url.endswith('/edit'):
                        self.scrape(f"{self.base_url}{next_url}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
