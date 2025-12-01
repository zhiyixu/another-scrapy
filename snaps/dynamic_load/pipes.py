from abc import ABC, abstractmethod

class Pipe(ABC):

    @abstractmethod
    def process(self): ...

class DatPipe(Pipe):

    def __init__(self):
        self.pipe_type = "dat"

    def process(self, data: str):
        print(f"process {self.pipe_type} success, data: {data}")

    def __repr__(self):
        return f"<Pipe(type={self.pipe_type})>"

class F0Pipe(Pipe):

    def __init__(self):
        self.pipe_type = "f0"

    def process(self, data: str):
        print(f"process {self.pipe_type} success, data: {data}")

    def __repr__(self):
        return f"<Pipe(type={self.pipe_type})>"
    
class FxPipe(Pipe):

    def __init__(self):
        self.pipe_type = "fx"

    def process(self, data: str):
        print(f"process {self.pipe_type} success, data: {data}")

    def __repr__(self):
        return f"<Pipe(type={self.pipe_type})>"