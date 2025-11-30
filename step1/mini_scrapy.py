import queue
import requests
from dataclasses import dataclass, field
from typing import Callable, Iterable, List, Union


# ------------ 请求 & 爬虫 --------------

@dataclass
class Request:
    url: str
    callback: Callable[[str], Iterable[Union["Request", dict]]]


@dataclass
class Spider:
    start_urls: List[str] = field(default_factory=list)

    def __init__(self, start_urls=None):
        if start_urls is not None:
            self.start_urls = start_urls
        else:
            self.start_urls = self.start_urls

    def start_requests(self) -> Iterable[Request]:
        """相当于 Scrapy 里的 start_requests"""
        for url in self.start_urls:
            # 这里把要抓的 URL 封装成 Request 对象
            yield Request(url=url, callback=self.parse)

    def parse(self, html: str) -> Iterable[Union[Request, dict]]:
        """子类必须重写：如何从 html 里提取数据 / 新的请求"""
        raise NotImplementedError


# ------------ 引擎核心 --------------

class Engine:
    def __init__(self, spider: Spider):
        self.spider = spider
        self.q = queue.Queue()

    def open_spider(self):
        """打开爬虫时，先把初始请求放进队列"""
        for req in self.spider.start_requests():
            self.q.put(req)

    def _download(self, request: Request) -> str:
        """超级简化的下载器"""
        resp = requests.get(request.url)
        resp.raise_for_status()
        return resp.text

    def start(self):
        """核心循环：从队列拿 Request -> 下载 -> 回调处理"""
        self.open_spider()
        while not self.q.empty():
            req = self.q.get()
            html = self._download(req)
            for result in req.callback(html):
                if isinstance(result, Request):
                    # 新的请求，继续加入队列
                    self.q.put(result)
                else:
                    # 简单认为是 item，打印出来
                    print("ITEM:", result)


# ------------ 一个示例 Spider --------------

class QuotesSpider(Spider):
    start_urls = ["https://www.baidu.com/"]

    def parse(self, html: str):
        """为了简单，这里不真正解析，只是演示流程"""
        yield {"html_length": len(html)}


# ------------ 程序入口 --------------

if __name__ == "__main__":
    spider = QuotesSpider()
    print(spider)
    engine = Engine(spider)
    engine.start()
