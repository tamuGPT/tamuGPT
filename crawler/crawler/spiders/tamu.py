import os
import scrapy
from urllib.parse import urlparse


class TamuSpider(scrapy.Spider):
    name = "tamu"
    allowed_domains = ["tamu.edu"]
    start_urls = ["https://tamu.edu"]
    data_dir = 'data'

    def parse(self, response):
        # Save the current page
        self.save_page(response)

        # Extract links from the webpage
        links = response.css('a::attr(href)').getall()

        for link in links:
            if link.startswith('http://') or link.startswith('https://'):
                yield response.follow(link, callback=self.parse)
            else:
                self.log(f"Skipping non-HTTP/HTTPS URL: {link}")

    def save_page(self, response):
        # Extract the URL of the webpage
        url = response.url

        # Extract the domain name from the URL
        domain = urlparse(url).netloc

        # Create a directory for the domain if it doesn't exist
        domain_dir = os.path.join(self.data_dir, domain)

        # Generate a filename based on the URL
        filename = urlparse(url).path.lstrip('/')
        print("filename: ", filename)
        if not filename:
            filename = 'index.html'
        elif filename.endswith('/'):
            filename += 'index.html'
        else:
            filename += '.html'
        print("HTML filename: ", filename)

        filepath = os.path.join(domain_dir, filename)
        directory = os.path.dirname(filepath)
        os.makedirs(directory, exist_ok=True)

        with open(filepath, 'wb') as f:
            f.write(response.body)

        self.log(f'Saved file {filepath}')
