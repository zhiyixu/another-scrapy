

PIPELINES = {
    "pipelines.UpperCasePipeline": 10,
    "pipelines.CleanPipeline": 15,
}

DOWNLOADER_MIDDLEWARES = {
    "middlewares.UserAgentMiddleware": 20,
    "middlewares.RetryMiddleware": 25,
}

SPIDER_MIEELEWARES = {
    "middlewares.StartLogMiddleware": 20,
    "middlewares.HtmlGuardMiddleware": 20,
    "middlewares.SpiderExceptionFallbackMiddleware": 20,
    "middlewares.EinsteinOnlyMiddleware": 20,
}

SCHEDULER = "scheduler.SimpleScheduler"

ASYNC_SCHEDULER = "scheduler.AsyncScheduler"

DUPEFILTER = "dupefilters.MemoryDipeFilter"

SCHEDILER_QUEUE = "queues.PriorityQueue"