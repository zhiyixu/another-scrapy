# spiders.py
from dataclasses import dataclass, field
from typing import Iterable, Callable, Union
from request import Request

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
    start_urls = ["https://www.baidu.com/"]

    def parse(self, html: str):
        """为了简单，这里不真正解析，只是演示流程"""
        yield {"html_length": len(html)}