import logging
import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class NicheScraper(BaseScraper):
    """
    Scraper for Niche college pages, designed to extract information about
    institutions.
    """

    def __init__(self):
        """
        Initializes the NicheScraper with the base URL of Niche.
        """
        super().__init__(base_url='https://www.niche.com')

    def scrape(self, url):
        """
        Scrapes the content of a Niche college page and returns a structured
        dictionary with the main content and key metrics.

        Args:
            url (str): The URL of the Niche college page to scrape.

        Returns:
            dict: A dictionary containing the scraped data.
        """
        logging.info(f"Visiting: {url}")
        if url in self.visited_urls:
            return

        if "georgia-institute-of-technology" not in url \
                or "college-of-computing-georgia-institute-of-technology" not in url \
                or "college-of-sciences-georgia-institute-of-technology" not in url \
                or "georgia-tech-college-of-design" not in url \
                or "georgia-tech-college-of-engineering" not in url \
                or "ivan-allen-college-of-liberal-arts" not in url \
                or "scheller-college-of-business" not in url:

            logging.warning("URL does not contain georgia tech info")
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
            summary_element = soup.find('div', class_='sc-jcFjpl')
            if summary_element:
                data['summary'] = summary_element.text.strip()

            # Extract bullet points
            bullet_points = []
            for div in soup.find_all('div', class_='sc-kIHeex'):
                bullet_points.append(div.text.strip())
            data['bullet_points'] = bullet_points

            # Extract additional metrics
            additional_sections = {}
            metrics = soup.find_all('div', class_='sc-iQKALj')
            for metric in metrics:
                key = metric.find('h2')
                value = metric.find('span')
                if key and value:
                    additional_sections[key.text.strip()] = value.text.strip()
            data['additional_sections'] = additional_sections

            self.visited_urls.add(url)
            return data

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        return {}
