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
        base_url = "https://www.zoomit.ir/archive/?sort=Newest&publishDate=All&readingTime=All&pageNumber={}"

        for page in range(1, 2):  
            full_url = base_url.format(page)
            self.driver.get(full_url)
            time.sleep(5)

            html = self.driver.page_source
            response = HtmlResponse(
                url=self.driver.current_url,
                body=html,
                encoding="utf-8"
            )

            yield from self.parse(response)

        self.driver.quit()


    def parse(self, response):
        links = response.css("div.scroll-m-16 a::attr(href)").getall()

        for url in links:
            yield response.follow(url, callback=self.parse_article)


    def parse_article(self, response):
        title = response.css("h1.sc-9996cfc-0.ieMlRF::text").get()
        tags = response.css("div.sc-a11b1542-0.fCUOzW a span::text").getall()

        cover_figure = response.css("figure.sc-50b37c60-0")
        cover_image = cover_figure.css("img::attr(src)").get()

        inline_figures = response.css("figure.grid")
        inline_images_with_captions = []
        for fig in inline_figures:
            img_url = fig.css("img::attr(src)").get()
            caption = fig.css("figcaption::text").get()
            inline_images_with_captions.append({
                "url": img_url,
                "caption": caption.strip() if caption else None
            })

        paragraphs = []
        for p in response.css("p"):
            text = ''.join(p.css("*::text").getall()).strip()
            if text:
                paragraphs.append(text)

        yield {
            "title": title.strip() if title else None,
            "tags": [tag.strip() for tag in tags if tag.strip()],
            "cover_image": {
                "url": cover_image,
                "caption": title.strip() if title else None  
            },
            "inline_images": inline_images_with_captions,
            "content": paragraphs
        }
