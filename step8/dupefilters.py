import hashlib 
from request import Request 
from abc import ABC, abstractmethod 

class BaseDupeFilter(ABC):

    def open(self): 
        print(f"[{self.__class__.__name__}] opened.")

    def close(self):
        print(f"[{self.__class__.__name__}] closed.")

    @abstractmethod
    def request_seen(self, request: Request) -> bool:...


class MemoryDipeFilter(BaseDupeFilter):

    def __init__(self):
        self._seen = set() 

    @staticmethod
    def _fingerprint(request: Request) -> str:
        return hashlib.sha1(request.url.encode("utf-8")).hexdigest()

    def request_seen(self, request: Request) -> bool:
        fp = self._fingerprint(request=request)
        if fp in self._seen:
            return True 
        self._seen.add(fp)
        return False

