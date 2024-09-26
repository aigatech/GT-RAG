import logging
import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class USNewsScraper(BaseScraper):
    """
    Scraper for U.S. News college pages, designed to extract rankings and key
    information.
    """

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

        try:
            response = requests.get(url)
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

            self.visited_urls.add(url)
            return data

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        return {}
