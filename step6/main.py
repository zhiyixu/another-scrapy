# main.py
from spiders import QuotesSpider
from engine import Engine

if __name__ == "__main__":
    spider = QuotesSpider()
    engine = Engine(spider)
    engine.start()
