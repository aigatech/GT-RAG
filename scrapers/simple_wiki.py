import logging
import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class SimpleWikiScraper(BaseScraper):
    """
    Scraper for Simple Wikipedia pages, specifically designed to extract structured
    information from articles.
    """

    def __init__(self):
        """
        Initializes the SimpleWikiScraper with the base URL of Simple Wikipedia.
        """
        super().__init__(base_url='https://simple.wikipedia.org')

    def scrape(self, url):
        """
        Scrapes the content of a Simple Wikipedia page and returns a structured
        dictionary with the main content, bullet points, and tables.

        Args:
            url (str): The URL of the Simple Wikipedia page to scrape.

        Returns:
            dict: A dictionary containing the scraped data.
        """
        logging.info(f"Visiting: {url}")
        if url in self.visited_urls:
            return
        if "Georgia_Institute_of_Technology" not in url \
                or "Buzz_(mascot)" not in url \
                or "Bobby_Dodd_Stadium" not in url \
                or "Georgia_Tech" not in url \
                or "Bobby_Dodd_Stadium" not in url \
                or "G._Wayne_Clough" not in url:
            return


            logging.warning("URL does not contain georgia tech info")
            return

        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            data = {"url": url}

            # Extract the title
            title_element = soup.find('h1', id='firstHeading')
            data['title'] = title_element.text.strip() if title_element else "No Title"

            # Extract main content
            content_element = soup.find('div', class_='mw-parser-output')
            if content_element:
                paragraphs = content_element.find_all('p')
                data['summary'] = "\n".join(p.text.strip() for p in paragraphs if p.text.strip())

                # Extract bullet points
                bullet_points = []
                for ul in content_element.find_all('ul'):
                    for li in ul.find_all('li'):
                        bullet_points.append(li.text.strip())
                data['bullet_points'] = bullet_points

                # Extract tables
                tables = []
                for table in content_element.find_all('table', class_='wikitable'):
                    table_data = []
                    for row in table.find_all('tr'):
                        cells = row.find_all(['th', 'td'])
                        cell_text = [cell.text.strip() for cell in cells]
                        table_data.append(cell_text)
                    tables.append(table_data)
                data['tables'] = tables

            self.visited_urls.add(url)
            return data

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        return {}