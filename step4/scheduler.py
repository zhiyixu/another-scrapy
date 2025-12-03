import queue 
from request import Request


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

    def get_request(self):
        if not self.queue.empty():
            return self.queue.get()
        return None 
    
    def has_requests(self):
        return not self.queue.empty()