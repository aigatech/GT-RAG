import logging
import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class RateMyProfessorsScraper(BaseScraper):
    """
    Scraper for Rate My Professors school pages, designed to extract ratings and
    professor information.
    """

    rejectList = [
        "compare",
        "add"
        ]

    def __init__(self):
        """
        Initializes the RateMyProfessorsScraper with the base URL of Rate My Professors.
        """
        super().__init__(base_url='https://www.ratemyprofessors.com')

    def scrape(self, url):
        """
        Scrapes the content of a Rate My Professors school page and returns a structured
        dictionary with ratings and key information.

        Args:
            url (str): The URL of the Rate My Professors school page to scrape.

        Returns:
            dict: A dictionary containing the scraped data.
        """
        logging.info(f"Visiting: {url}")
        if url in self.visited_urls:
            return
        
        # Reject any redundant URLs or unnecessary internal links
        if (any word in url for word in rejectList):
            return
        if ("www.ratemyprofessors.com" not in url):
            return
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            data = {"url": url}

            # Extract the title
            title_element = soup.find('h1', class_='NameTitle__Name')
            data['title'] = title_element.text.strip() if title_element else "No Title"

            # Extract summary of school ratings
            summary_element = soup.find('div', class_='SchoolSummary')
            if summary_element:
                data['summary'] = summary_element.text.strip()

            # Extract bullet points for professor ratings
            bullet_points = []
            for prof in soup.find_all('div', class_='ProfessorCard'):
                prof_name = prof.find('span', class_='NameTitle__Name').text.strip()
                prof_rating = prof.find('span', class_='Rating__RatingValue').text.strip()
                bullet_points.append(f"{prof_name}: {prof_rating}")
            data['bullet_points'] = bullet_points

            # Extract additional sections (e.g., top tags)
            additional_sections = {}
            tag_section = soup.find('div', class_='TagCloud')
            if tag_section:
                tags = [tag.text.strip() for tag in tag_section.find_all('div', class_='TagCloud__Tag')]
                additional_sections['Top Tags'] = tags
            data['additional_sections'] = additional_sections

            self.visited_urls.add(url)
            return data

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        return {}
