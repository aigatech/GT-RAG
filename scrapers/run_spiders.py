from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapers.spiders.singlesite_spider import SingleSiteSpider

urls = [
    'https://gt-student-wiki.org/mediawiki/index.php/',
    'https://www.gatech.edu/',
    'https://news.gatech.edu/',
    'https://admission.gatech.edu/',
    'https://registrar.gatech.edu/',
    'https://studentlife.gatech.edu/',
    # URLs below have been blocked
    # 'https://www.niche.com/colleges/georgia-institute-of-technology/',
    # 'https://www.usnews.com/best-colleges/georgia-institute-of-technology-1569',
    # 'https://www.ratemyprofessors.com/school/361/',
]

process = CrawlerProcess(get_project_settings())

for url in urls:
    process.crawl(SingleSiteSpider, start_url=url)

process.start()
