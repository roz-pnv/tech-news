import scrapy
from selenium import webdriver
from scrapy.http import HtmlResponse
import time

from news_scraper.items import ZoomitArticleItem
from news_scraper.utils.date import parse_persian_datetime

class ZoomitSpider(scrapy.Spider):
    name = "zoomit"

    def __init__(self, pages=None, *args, **kwargs):
        super(ZoomitSpider, self).__init__(*args, **kwargs)

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=options)
        self.failed_items = []  

        if pages:
            self.pages = [int(p) for p in pages.split(",")]
        else:
            self.pages = [1]


    def start_requests(self):
        base_url = "https://www.zoomit.ir/archive/?sort=Newest&publishDate=All&readingTime=All&pageNumber={}"

        try:
            for page in self.pages:
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

        finally:
            self.driver.quit()


    def parse(self, response):
        links = response.css("div.scroll-m-16 a::attr(href)").getall()

        for url in links:
            full_url = response.urljoin(url)
            yield scrapy.Request(url=full_url, callback=self.parse_article)


    def parse_article(self, response):
        try:
            title = response.css("h1.sc-9996cfc-0.ieMlRF::text").get()
            tags = response.css("div.sc-a11b1542-0.fCUOzW a span::text").getall()

            date_text = response.css("div.sc-a11b1542-0.iSQiSE span.sc-9996cfc-0.inKOvi::text").get()
            published_at = parse_persian_datetime(date_text)

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

            item = ZoomitArticleItem(
                title=title.strip() if title else None,
                tags=[tag.strip() for tag in tags if tag.strip()],
                published_at=published_at,
                cover_image={
                    "url": cover_image,
                    "caption": title.strip() if title else None
                },
                inline_images=inline_images_with_captions,
                content="\n\n".join(paragraphs),
                source_url=response.url
            )

            yield item

        except Exception as e:
            self.failed_items.append({
                "url": response.url,
                "error": str(e),
            })
            self.logger.error(f"Error scraping {response.url}: {e}")
