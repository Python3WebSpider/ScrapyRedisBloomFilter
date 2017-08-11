# ScrapyRedisBloomFilter

## Installation

You can easily install this package with pip:

```
pip install scrapy-redis-bloomfilter
```

## Usage

Add this settings to settings.py

```python
# Ensure use this Scheduler
SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis
DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"

# Redis URL
REDIS_URL = 'redis://:foobared@localhost:6379'

# Number of Hash Functions to use, defaults to 6
BLOOMFILTER_HASH_NUMBER = 6

# Redis Memory Bit of Bloomfilter Usage, 30 means 2^30 = 128MB, defaults to 30
BLOOMFILTER_BIT = 30

# Persist
SCHEDULER_PERSIST = True
```

## Test

Here is a test of this project, usage:

```
git clone https://github.com/Python3WebSpider/ScrapyRedisBloomFilter.git
cd ScrapyRedisBloomFilter/test
scrapy crawl test
```

Note: please change REDIS_URL in settings.py.

Spider like this:

```python
from scrapy import Request, Spider

class TestSpider(Spider):
    name = 'test'
    base_url = 'https://www.baidu.com/s?wd='
    
    def start_requests(self):
        for i in range(10):
            url = self.base_url + str(i)
            yield Request(url, callback=self.parse)
            
        # Here contains 10 duplicated Requests    
        for i in range(100): 
            url = self.base_url + str(i)
            yield Request(url, callback=self.parse)
    
    def parse(self, response):
        self.logger.debug('Response of ' + response.url)
```

Result like this:

```python
{'bloomfilter/filtered': 10, # This is the number of Request filtered by BloomFilter
 'downloader/request_bytes': 34021,
 'downloader/request_count': 100,
 'downloader/request_method_count/GET': 100,
 'downloader/response_bytes': 72943,
 'downloader/response_count': 100,
 'downloader/response_status_count/200': 100,
 'finish_reason': 'finished',
 'finish_time': datetime.datetime(2017, 8, 11, 9, 34, 30, 419597),
 'log_count/DEBUG': 202,
 'log_count/INFO': 7,
 'memusage/max': 54153216,
 'memusage/startup': 54153216,
 'response_received_count': 100,
 'scheduler/dequeued/redis': 100,
 'scheduler/enqueued/redis': 100,
 'start_time': datetime.datetime(2017, 8, 11, 9, 34, 26, 495018)}
```

