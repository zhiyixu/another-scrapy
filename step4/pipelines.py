# pipelines.py
from abc import ABC, abstractmethod


class Pipeline(ABC):

    def open_spider(self, spider):
        print(f"[{self.__class__.__name__}] open_spider")

    @abstractmethod
    def process_item(self, item, spider): ...

    def close_spider(self, spider):
        print(f"[{self.__class__.__name__}] close_spider")

class UpperCasePipeline(Pipeline):

    def __init__(self, name: str="upper case"):
        self.name = name 

    def __repr__(self):
        return f"<Pipeline(name={self.name})>"

    def process_item(self, item: dict, spider):
        item["author"] = item["author"].upper()
        return item


class CleanPipeline(Pipeline):

    def __init__(self, name: str="clean"):
        self.name = name 

    def __repr__(self):
        return f"<Pipeline(name={self.name})>"
    
    def process_item(self, item: dict, spider):
        quote = item["quote"]
        quote = quote.replace(" ", "_")
        quote = quote.replace("\n", "")
        quote = quote.replace("\t", "")
        item["quote"] = quote
        return item