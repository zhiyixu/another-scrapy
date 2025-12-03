from typing import Optional 
from request import Request 


class Middleware:

    def open_spider(self, spider):
        print(f"[{self.__class__.__name__}] open_spider")

    def close_spider(self, spider):
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
        request._retries = current + 1 
        print(f"[RetryMiddleware] retry {request.url} {request._retries} times.")
        import requests
        resp = requests.get(request.url, headers=request.headers or {})
        resp.raise_for_status()
        return resp.text
