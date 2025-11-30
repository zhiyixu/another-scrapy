# engine.py
import queue
import requests
from request import Request
from spiders import Spider

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
