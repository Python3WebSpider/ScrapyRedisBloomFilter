from scrapy_redis.defaults import *

BLOOMFILTER_HASH_NUMBER = 6
BLOOMFILTER_BIT = 30
DUPEFILTER_DEBUG = False

SCHEDULER_DUPEFILTER_KEY = '%(spider)s:bloomfilter'
