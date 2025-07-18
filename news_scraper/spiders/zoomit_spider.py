import scrapy
from selenium import webdriver
from scrapy.http import HtmlResponse
import time

class ZoomitSpider(scrapy.Spider):
    name = "zoomit"

    def __init__(self, *args, **kwargs):
        super(ZoomitSpider, self).__init__(*args, **kwargs)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  
        self.driver = webdriver.Chrome(options=options)

    def start_requests(self):
        self.driver.get("https://www.zoomit.ir/archive/")
        time.sleep(5)  
        html = self.driver.page_source

        response = HtmlResponse(
            url=self.driver.current_url,
            body=html,
            encoding="utf-8"
        )

        self.driver.quit()
        yield from self.parse(response)

    def parse(self, response):
        links = response.css("div.scroll-m-16 a::attr(href)").getall()

        for url in links:
            yield response.follow(url, callback=self.parse_article)

    def parse_article(self, response):
        pass
      
