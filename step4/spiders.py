# spiders.py
from spider import Spider
from lxml import html


class QuotesSpider(Spider):
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, raw_html: str):
        """解析页面，提取数据"""
        tree = html.fromstring(raw_html)
        quotes = tree.xpath('//div[@class="quote"]')

        for quote in quotes:
            text = quote.xpath('.//span[@class="text"]/text()')[0]
            author = quote.xpath('.//span/small[@class="author"]/text()')[0]
            yield {"quote": text, "author": author}