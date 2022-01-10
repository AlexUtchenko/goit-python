# Scrapy settings for MW14 project


BOT_NAME = 'MW14'

SPIDER_MODULES = ['MW14.spiders']
NEWSPIDER_MODULE = 'MW14.spiders'



# Obey robots.txt rules
ROBOTSTXT_OBEY = True


ITEM_PIPELINES = {
   'MW14.pipelines.DuplicatesPipeline': 300,
   'MW14.pipelines.MW14SavePipeline': 300,
}

CONNECTION_STRING = 'sqlite:///MW14.db'


