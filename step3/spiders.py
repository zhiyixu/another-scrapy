# spiders.py
from dataclasses import dataclass, field
from typing import Iterable, Callable, Union
from request import Request
from lxml import html


@dataclass
class Spider:
    start_urls: list = field(default_factory=list)

    def __init__(self, start_urls=None):
        if start_urls is not None:
            self.start_urls = start_urls
        else:
            self.start_urls = self.start_urls

    def start_requests(self) -> Iterable[Request]:
        """相当于 Scrapy 里的 start_requests"""
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, html: str) -> Iterable[Union[Request, dict]]:
        """子类必须重写：如何从 html 里提取数据 / 新的请求"""
        raise NotImplementedError

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