import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapers.spiders.singlesite_spider import SingleSiteSpider

with open('config.json', 'r') as f:
    config = json.load(f)
    urls = config.get('urls', [])

process = CrawlerProcess(get_project_settings())

for url in urls:
    process.crawl(SingleSiteSpider, start_url=url)

process.start()
