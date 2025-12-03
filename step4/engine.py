# engine.py
import requests
from request import Request
from spiders import Spider
from scheduler import Scheduler
import misc
import settings

class Engine:

    def __init__(self, spider: Spider):
        self.spider = spider
        self.scheduler = Scheduler()
        self.pipes = self._dload(d=settings.PIPELINES)
        self.mwares = self._dload(d=settings.MIDDLEWARES)

    def _dload(self, d: dict):
        ll = []
        pths = sorted(d.items(), key=lambda x: x[1])
        for pth, _ in pths:
            ll.append( misc.dload(pth)() )
        return ll
    
    def _open(self, clss: list):
        for cls in clss:
            if hasattr(cls, "open_spider"):
                cls.open_spider(self.spider)

    def _close(self, clss: list):
        for cls in clss:
            if hasattr(cls, "close_spider"):
                cls.close_spider(self.spider)
       
    
    def open_spider(self):
        """打开爬虫时，先把初始请求放进队列"""
        self._open(clss=self.pipes)
        self._open(clss=self.mwares)
        for req in self.spider.start_requests():
            self.scheduler.add_request(req)

    def close_spider(self):
        self._close(clss=self.pipes)
        self._close(clss=self.mwares)
    
    def _download(self, request: Request) -> str:
        """超级简化的下载器"""
        resp = requests.get(request.url, headers=request.headers or {})
        resp.raise_for_status()
        return resp.text

    def _download_with_middlewares(self, request: Request) -> str:
        """执行 downloader middlewares + 真正下载"""

        # 1. 依次执行 process_request
        for mw in self.mwares:
            if hasattr(mw, "process_request"):
                mw.process_request(request)

        # 2. 真正下载 + 异常处理（交给 process_exception）
        try:
            response_text = self._download(request)
        except Exception as exc:
            handled = None
            for mw in reversed(self.mwares):
                if hasattr(mw, "process_exception"):
                    result = mw.process_exception(request, exc)
                    if isinstance(result, str):
                        handled = result
                        break
            if handled is None:
                # 没有中间件能处理这个异常，就直接抛出去
                raise
            response_text = handled

        # 3. 依次（反向）执行 process_response
        for mw in reversed(self.mwares):
            if hasattr(mw, "process_response"):
                response_text = mw.process_response(request, response_text)

        return response_text

    
    def start(self):
        """核心循环：从队列拿 Request -> 下载 -> 回调处理"""
        self.open_spider()
        while self.scheduler.has_requests():
            req = self.scheduler.get_request()
            html = self._download_with_middlewares(req)
            for result in req.callback(html):
                if isinstance(result, Request):
                    # 新的请求，继续加入队列
                    self.scheduler.add_request(result)
                else:
                    # 简单认为是 item，打印出来
                    item = result
                    for pipe in self.pipes:
                        if item is not None: 
                            item = pipe.process_item(item, self.spider)
                    print(item)
        self.close_spider()