import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapers.spiders.singlesite_spider import SingleSiteSpider
import os 
config_path = os.path.join(os.path.dirname(__file__), 'config.json')

with open(config_path, 'r') as f:
    config = json.load(f)
    urls = config.get('urls', [])

process = CrawlerProcess(get_project_settings())

for url in urls:
    process.crawl(SingleSiteSpider, start_url=url)

process.start()
