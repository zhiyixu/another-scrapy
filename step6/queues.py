import queue 
from request import Request 
from abc import ABC, abstractmethod 


class BaseQueue(ABC):

    @abstractmethod
    def push(self, request: Request): ...

    @abstractmethod
    def pop(self) -> Request | None: ...

    def __len__(self) -> int:
        raise NotImplementedError


class FIFOQueue(BaseQueue):

    def __init__(self):
        self._q = queue.Queue() 

    def push(self, request: Request):
        self._q.put(request)

    def pop(self) -> Request | None:
        if self._q.empty():
            return None 
        return self._q.get()
    
    def __len__(self) -> int:
        return self._q.qsize()


class PriorityQueue(BaseQueue):


    def __init__(self):
        self._q = queue.PriorityQueue()
        self._seq = 0 

    def push(self, request: Request):
        pr = getattr(request, "prioirty", 0)
        self._seq += 1 
        self._q.put((pr, self._seq, request))

    def pop(self) -> Request | None:
        if self._q.empty():
            return None 
        _, _, req = self._q.get() 
        return req 
    
    def __len__(self):
        return self._q.qsize()





