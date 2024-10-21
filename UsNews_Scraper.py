from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key='ADD_API_KEY')

crawl_result = app.crawl_url('https://www.usnews.com/best-colleges/georgia-institute-of-technology-1569', 
                            params={ 
                                'limit': 2, #EDIT LIMIT HERE
                                'scrapeOptions': {'formats': [ 'html' ]}
	                           
                                
                            },
                            poll_interval=30
                            
                        )

for index, page in enumerate(crawl_result['data']):
    output_file = f'crawl_result_page_{index + 1}.txt' 
    with open(output_file, 'w') as file:
        file.write(page['html']) 

    print(f'Page {index + 1} has been written to {output_file}')