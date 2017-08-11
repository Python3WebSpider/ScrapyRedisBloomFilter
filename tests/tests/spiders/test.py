# -*- coding: utf-8 -*-
from scrapy import Request, Spider


class TestSpider(Spider):
    name = 'test'
    
    base_url = 'https://www.baidu.com/s?wd='
    
    def start_requests(self):
        for i in range(10):
            url = self.base_url + str(i)
            yield Request(url, callback=self.parse)
            
        for i in range(100):
            url = self.base_url + str(i)
            yield Request(url, callback=self.parse)
    
    def parse(self, response):
        self.logger.debug('Response of ' + response.url)
