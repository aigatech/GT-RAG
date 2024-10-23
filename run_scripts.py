from scrapers.gt_wiki_scraper import GTWikiScraper
from scrapers.simple_wiki_scraper import SimpleWikiScraper
from scrapers.niche_scraper import NicheScraper
from scrapers.usnews_scraper import USNewsScraper
from scrapers.ratemyprofessors_scraper import RateMyProfessorsScraper
from scrapers.gtwebscraper import GTWebsiteScraper

def run_scrapers():
    """
    Runs all scrapers for the specified URLs and prints the structured data.
    """

    # Define the URLs to scrape and their corresponding scraper classes
    urls_and_scrapers = [
        # ('https://gt-student-wiki.org/mediawiki/index.php/Main_Page', GTWikiScraper),
        # ('https://simple.wikipedia.org/wiki/Georgia_Institute_of_Technology', SimpleWikiScraper),
        # ('https://www.niche.com/colleges/georgia-institute-of-technology/', NicheScraper),
        # ('https://www.usnews.com/best-colleges/georgia-institute-of-technology-1569', USNewsScraper),
        # ('https://www.ratemyprofessors.com/school/361', RateMyProfessorsScraper),
        ('https://www.gatech.edu/', GTWebsiteScraper),
        ('https://news.gatech.edu/', GTWebsiteScraper),
        ('https://admission.gatech.edu/', GTWebsiteScraper),
        ('https://registrar.gatech.edu/', GTWebsiteScraper),
        ('https://studentlife.gatech.edu/', GTWebsiteScraper)
    ]

    # Iterate over each URL and its corresponding scraper class
    for url, ScraperClass in urls_and_scrapers:
        scraper = ScraperClass(url)  
        data = scraper.start_scraping
        print(f"\nScraped data from {url}:\n", data)

if __name__ == "__main__":
    run_scrapers()  
