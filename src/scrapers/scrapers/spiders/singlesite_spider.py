import scrapy
import json
import os
import re
from datetime import datetime
from urllib.parse import urlparse, urljoin
import html2text
import dateutil.parser as dateparser 

class SingleSiteSpider(scrapy.Spider):
    name = "singlesite_spider"
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1,  # Adjust as needed
    }

    def __init__(self, start_url=None, *args, **kwargs):
        super(SingleSiteSpider, self).__init__(*args, **kwargs)
        if start_url is None:
            raise ValueError('You must provide a start_url')
        self.start_url = start_url.rstrip('/')  # Remove trailing slash if any
        self.start_urls = [self.start_url]
        parsed_uri = urlparse(self.start_url)
        domain = parsed_uri.netloc
        self.allowed_domains = [domain]
        self.site_name = domain.replace('.', '_')
        # Create a directory for the site if it doesn't exist
        if not os.path.exists(self.site_name):
            os.makedirs(self.site_name)
        # Counter for the number of pages scraped
        self.page_count = 0
        self.max_pages = 1000  # Limit to 1000 pages

    def parse(self, response):
        # Check if the response contains text/html content
        content_type = response.headers.get('Content-Type', b'').decode('utf-8').lower()
        if 'text/html' in content_type:
            self.page_count += 1

            # Convert HTML to Markdown
            converter = html2text.HTML2Text()
            converter.ignore_links = False  # Keep links
            markdown_content = converter.handle(response.text)

            # Extract metadata
            title = response.css('title::text').get() or ''
            last_modified = self.extract_last_modified_date(response)

            page_data = {
                'metadata': {
                    'url': response.url,
                    'date_updated': last_modified,
                    'title': title.strip(),
                },
                'data': markdown_content,
            }

            # Generate a filename based on the URL
            filename = os.path.join(
                self.site_name,
                response.url.replace('http://', '')
                             .replace('https://', '')
                             .replace('/', '_')
                             .replace('?', '_') + '.json'
            )
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(page_data, f, ensure_ascii=False, indent=4)

            # Follow links within the site if limit not reached
            if self.page_count < self.max_pages:
                for href in response.css('a::attr(href)').getall():
                    # Resolve relative URLs
                    href = urljoin(response.url, href)
                    # Check if the URL starts with the start_url
                    if href.startswith(self.start_url):
                        # Skip URLs with binary file extensions
                        if href.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.pdf', '.zip', '.exe')):
                            self.logger.info(f"Skipping binary file URL: {href}")
                            continue
                        yield response.follow(href, self.parse)
        else:
            # If content is not text/html, skip processing
            self.logger.info(f"Skipping non-text response: {response.url}")

    def extract_last_modified_date(self, response):
        # 1. Try 'Last-Modified' HTTP header
        last_modified = response.headers.get('Last-Modified')
        if last_modified:
            try:
                date_str = last_modified.decode('utf-8')
                parsed_date = self.parse_date(date_str)
                if parsed_date:
                    return parsed_date
            except UnicodeDecodeError:
                pass  # Continue to next method

        # 2. Try meta tags with various attributes
        meta_date_selectors = [
            "//meta[@http-equiv='last-modified']/@content",
            "//meta[@name='last-modified']/@content",
            "//meta[@property='article:modified_time']/@content",
            "//meta[@property='og:updated_time']/@content",
            "//meta[@name='date']/@content",
            "//meta[@name='dcterms.modified']/@content",
            "//meta[@name='DC.date.modified']/@content",
            "//meta[@name='revised']/@content",
        ]
        for selector in meta_date_selectors:
            date_str = response.xpath(selector).get()
            if date_str:
                parsed_date = self.parse_date(date_str)
                if parsed_date:
                    return parsed_date

        # 3. Try JSON-LD structured data
        json_ld_data = response.xpath('//script[@type="application/ld+json"]/text()').getall()
        for json_ld in json_ld_data:
            try:
                data = json.loads(json_ld)
                if isinstance(data, dict):
                    date_published = data.get('dateModified') or data.get('datePublished')
                    if date_published:
                        parsed_date = self.parse_date(date_published)
                        if parsed_date:
                            return parsed_date
                elif isinstance(data, list):
                    for item in data:
                        date_published = item.get('dateModified') or item.get('datePublished')
                        if date_published:
                            parsed_date = self.parse_date(date_published)
                            if parsed_date:
                                return parsed_date
            except json.JSONDecodeError:
                continue

        # 4. As a last resort, return None
        return None

    def parse_date(self, date_str):
        # Normalize and parse the date string
        try:
            # Remove any timezone abbreviations which dateparser might not handle
            date_str = re.sub(r'\b[A-Z]{2,}\b', '', date_str)
            parsed_date = dateparser.parse(date_str)
            if parsed_date:
                return parsed_date.isoformat()
        except (ValueError, TypeError, OverflowError):
            pass
        return None
