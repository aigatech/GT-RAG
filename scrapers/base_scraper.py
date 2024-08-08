import os
import re
import logging
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    """
    Abstract base class for web scrapers. Provides common functionality such as
    logging setup and filename sanitization.
    """

    def __init__(self, base_url):
        """
        Initializes the BaseScraper with a base URL and sets up logging.

        Args:
            base_url (str): The base URL for the scraper.
        """
        self.base_url = base_url
        self.visited_urls = set()  # Keeps track of visited URLs to avoid re-scraping
        self.directory = "scraped_data"  # Directory to store scraped data
        self.setup_logging()  # Initialize logging configuration

    def setup_logging(self):
        """
        Sets up the logging configuration for the scraper.
        """
        logging.basicConfig(
            level=logging.INFO,  # Set logging level to INFO
            format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
            handlers=[logging.StreamHandler()]  # Output log to console
        )

    def sanitize_filename(self, filename):
        """
        Sanitizes a filename by replacing invalid characters with underscores.

        Args:
            filename (str): The filename to sanitize.

        Returns:
            str: The sanitized filename.
        """
        return re.sub(r'[<>:"/\\|?*]', '_', filename)

    @abstractmethod
    def scrape(self, url):
        """
        Abstract method to be implemented by subclasses to scrape a given URL.

        Args:
            url (str): The URL to scrape.
        """
        pass
