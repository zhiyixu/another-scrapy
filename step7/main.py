# main.py
from spiders import QuotesSpider
from engine import AsyncEngine
import asyncio

if __name__ == "__main__":
    spider = QuotesSpider()
    engine = AsyncEngine(spider, concurrency=10)
    asyncio.run(engine.start())

