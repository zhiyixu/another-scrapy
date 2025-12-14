from typing import Optional, Iterable, Union
from request import Request 
from spider import Spider

class Middleware:

    def open_spider(self, spider: Spider):
        print(f"[{self.__class__.__name__}] open_spider")

    def close_spider(self, spider: Spider):
        print(f"[{self.__class__.__name__}] open_spider")

class UserAgentMiddleware(Middleware):

    def __init__(self, useragent: Optional[str]=None):
        self.user_agent = useragent or "another-scrapy-bot/1.0"
    
    def process_request(self, request: Request):

        headers = request.headers or {}
        headers.setdefault("User-Agent", self.user_agent)
        request.headers = headers 

class RetryMiddleware(Middleware):

    def __init__(self, max_reties: int=2):
        self.max_reties = max_reties 

    def process_exception(self, request: Request, exception: Exception):

        current = getattr(request, "_retries", 0)
        if current > self.max_reties:
            return None 
        request._retries = current + 1 # dynamic binding # type: ignore
        print(f"[RetryMiddleware] retry {request.url} {request._retries} times.") # type: ignore
        import requests
        resp = requests.get(request.url, headers=request.headers or {})
        resp.raise_for_status()
        return resp.text


class SpiderMidderware(Middleware):...


class StartLogMiddleware(SpiderMidderware):

    def process_start_requests(self, start_requests: Iterable[Request], spider: Spider):
        for req in start_requests:
            print(f"[StartLogMiddleware] start request: {req.url}")
            yield req 

class HtmlGuardMiddleware(SpiderMidderware):

    def process_spider_input(self, html_text: str, spider: Spider):
        if not html_text or not html_text.strip():
            raise ValueError("Empty response.")
        
class SpiderExceptionFallbackMiddleware(SpiderMidderware):

    def process_spider_exception(self, html_text: str, exception: Exception, spider: Spider):
        yield {
            "type": "spider_exception",
            "spider": getattr(spider, "name", spider.__class__.__name__),
            "error": repr(exception)
        }

class EinsteinOnlyMiddleware(SpiderMidderware):

    def process_spider_output(self, html_text: str, results: Iterable[Union[Request, dict]], spider: Spider):
        for r in results:
            if isinstance(r, Request):
                yield r 
            else:
                if r.get("author") == "Albert Einstein":
                    yield r