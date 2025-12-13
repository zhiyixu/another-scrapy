

PIPELINES = {
    "pipelines.UpperCasePipeline": 10,
    "pipelines.CleanPipeline": 15,
}

MIDDLEWARES = {
    "middlewares.UserAgentMiddleware": 20,
    "middlewares.RetryMiddleware": 25,
}

SPIDER_MIEELEWARES = {
    "middlewares.StartLogMiddleware": 20,
    "middlewares.HtmlGuardMiddleware": 20,
    "middlewares.SpiderExceptionFallbackMiddleware": 20,
    "middlewares.EinsteinOnlyMiddleware": 20,
}