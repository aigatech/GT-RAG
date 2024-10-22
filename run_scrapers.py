from firecrawl import FirecrawlApp
import os
from urllib.parse import urlparse

def scrape_urls(urls, app):
    for url in urls:
     
        crawl_result = app.crawl_url(url, 
                                    params={ 
                                        'limit': 2,  # EDIT LIMIT HERE
                                        'scrapeOptions': {'formats': ['markdown']}
                                    },
                                    poll_interval=30
                                )

        parsed_url = urlparse(url)
        domain = parsed_url.netloc.replace('.', '_')  
        folder_name = domain
        
  
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        

        for index, page in enumerate(crawl_result['data']):
            output_file = os.path.join(folder_name, f'crawl_result_page_{index + 1}.md') 
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(page['markdown']) 
            print(f'Page {index + 1} for {url} has been written to {output_file}')


app = FirecrawlApp(api_key='ADD API KEY')


urls = [
    'https://gt-student-wiki.org/mediawiki/index.php/',
    'https://simple.wikipedia.org/wiki/Georgia_Institute_of_Technology',
    'https://www.niche.com/colleges/georgia-institute-of-technology/',
    'https://www.usnews.com/best-colleges/georgia-institute-of-technology-1569',
    'https://www.ratemyprofessors.com/school/361',
    'https://www.gatech.edu/',
    'https://news.gatech.edu/',
    'https://admission.gatech.edu/',
    'https://registrar.gatech.edu/',
    'https://studentlife.gatech.edu/'
]

scrape_urls(urls, app)
