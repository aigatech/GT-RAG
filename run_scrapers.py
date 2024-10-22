# run_scrapers.py

def run_gt_web_scraper():
    from scrapers.gt_web import GTWebsiteScraper
    gt_urls = [
        'https://www.gatech.edu/',
        'https://news.gatech.edu/',
        'https://admission.gatech.edu/',
        'https://registrar.gatech.edu/',
        'https://studentlife.gatech.edu/'
    ]
    for url in gt_urls:
        scraper = GTWebsiteScraper(base_url=url)
        scraper.start_scraping()

def run_niche_scraper():
    from firecrawl import FirecrawlApp
    app = FirecrawlApp(api_key='YOUR_API_KEY')  # Replace with your actual API key
    crawl_result = app.crawl_url(
        'https://www.niche.com/colleges/georgia-institute-of-technology/', 
        params={ 
            'limit': 2,  # Adjust the limit as needed
            'scrapeOptions': {'formats': ['html']}
        },
        poll_interval=30
    )

    for index, page in enumerate(crawl_result['data']):
        output_file = f'niche_crawl_result_page_{index + 1}.txt' 
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(page['html'])
        print(f'Niche Page {index + 1} has been written to {output_file}')

def run_rate_my_prof_scraper():
    from scrapers.ratemyprof_api import RateMyProfApi
    georgia_tech = RateMyProfApi(361)
    georgia_tech.CompileAllProfReviews()
    print("RateMyProfessors data has been compiled.")

def run_simple_wiki_scraper():
    from scrapers.simple_wiki import SimpleWikiScraper
    url = 'https://simple.wikipedia.org/wiki/Georgia_Institute_of_Technology'
    scraper = SimpleWikiScraper()
    data = scraper.scrape(url)
    with open('simple_wiki_data.txt', 'w', encoding='utf-8') as f:
        f.write(str(data))
    print("Simple Wikipedia data saved to simple_wiki_data.txt.")

def run_us_news_scraper():
    from firecrawl import FirecrawlApp
    app = FirecrawlApp(api_key='YOUR_API_KEY')  # Replace with your actual API key
    crawl_result = app.crawl_url(
        'https://www.usnews.com/best-colleges/georgia-institute-of-technology-1569', 
        params={ 
            'limit': 2,  # Adjust the limit as needed
            'scrapeOptions': {'formats': ['html']}
        },
        poll_interval=30
    )

    for index, page in enumerate(crawl_result['data']):
        output_file = f'us_news_crawl_result_page_{index + 1}.txt' 
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(page['html'])
        print(f'US News Page {index + 1} has been written to {output_file}')

if __name__ == '__main__':
    run_gt_web_scraper()
    run_niche_scraper()
    run_rate_my_prof_scraper()
    run_simple_wiki_scraper()
    run_us_news_scraper()
