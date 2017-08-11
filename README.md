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