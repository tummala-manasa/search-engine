import scrapy
import json
from pathlib import Path
from bs4 import BeautifulSoup

class ReactSpider(scrapy.Spider):
    name = 'react_beauty_dev'
    allowed_domains = ['react.dev']
    start_urls = [ 'https://react.dev/learn']
    
    custom_settings = {
        'DEPTH_LIMIT': 2,  # Set maximum depth
    }
    page_count = 0
    
    def parse(self, response):
        try:
            self.page_count += 1

            page_title = response.css('h1::text').get()
            filename = f"react-{self.page_count}.json"

            if self.page_count > 300: # limit to 300 files
                return
            
            soup = BeautifulSoup(response.body, 'html.parser')
            a = ""
            for string in soup.strings:
                a = a + repr(string) + ', '

            data = {
                "id": self.page_count,
                "url": response.url,
                "title": page_title,
                "content": a,
            }

            with open(filename, "w") as f:
                json.dump(data, f, ensure_ascii=False)
                self.log(f"Saved file {filename} {response.url}")
        except:
            self.page_count -= 1
        
        # Follow links to other pages
        for next_page in response.css('a::attr(href)').getall():
            yield response.follow(next_page, callback=self.parse)
