# Scrapy settings for tabebot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'tabebot'

SPIDER_MODULES = ['tabebot.spiders']
NEWSPIDER_MODULE = 'tabebot.spiders'

RETRY_TIMES = 10

EXTENSIONS = {
    'scrapy.contrib.spiderstate.SpiderState': 500,
}

RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 90,
}

ITEM_PIPELINES = {
    'tabebot.pipelines.RemoveDuplicatesPipeline': 0,
    'tabebot.pipelines.MultiJsonLinesItemPipeline': 1,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'tabebot (CHANGEME)'
