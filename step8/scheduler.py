import queue 
from request import Request
from typing import Union, Any
from dupefilters import BaseDupeFilter 
from queues import BaseQueue, FIFOQueue 
import asyncio

class Scheduler:

    def __init__(self):
        self.queue = queue.Queue()
        self.seen_urls = set() 

    def add_request(self, request: Request) -> None:
        if request.url not in self.seen_urls:
            self.seen_urls.add(request.url)
            self.queue.put(request)
        else:
            print(f"Skip: {request.url}")

    def get_request(self) -> Union[Request, Any]:
        if not self.queue.empty():
            return self.queue.get()
        return None 
    
    def has_requests(self):
        return not self.queue.empty()
    

class BaseScheduler:

    def open(self): ...

    def close(self): ...

    def enqueue_request(self, request: Request) -> bool:

        raise NotImplementedError 
    
    def next_request(self) -> Request | None:
        raise NotImplementedError 
    
    def has_pending_requests(self) -> bool:
        raise NotImplementedError 
    
class SimpleScheduler(BaseScheduler):

    def __init__(self, dupefilter: BaseDupeFilter, q: BaseQueue | None=None):
        self.dupefilter = dupefilter
        self.q = q or FIFOQueue()

    def open(self):
        self.dupefilter.open() 

    def close(self):
        self.dupefilter.close()

    def enqueue_request(self, request: Request) -> bool:
        if self.dupefilter.request_seen(request=request):
            return False 
        self.q.push(request=request)
        return True 
    
    def next_request(self) -> Request | None:
        return self.q.pop()
    
    def has_pending_requests(self) -> bool:
        return len(self.q)>0
    
class AsyncScheduler:

    def __init__(self, dupefilter: BaseDupeFilter, maxsize: int=0):
        self.dupefilter = dupefilter 
        self.q = asyncio.Queue(maxsize=maxsize)

    async def open(self):
        self.dupefilter.open() 

    async def close(self):
        self.dupefilter.close() 

    async def enqueue_request(self, request: Request) -> bool:
        if self.dupefilter.request_seen(request=request):
            return False 
        await self.q.put(request)
        return True 
    
    async def next_request(self) -> Request:
        return await self.q.get() 
    
    def task_done(self):
        """
        标记一个任务已经完成
        """
        self.q.task_done()

    async def join(self):
        await self.q.join()