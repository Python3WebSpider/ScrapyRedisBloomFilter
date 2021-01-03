from scrapy.utils.misc import load_object
from scrapy_redis.scheduler import Scheduler as BaseScheduler


class Scheduler(BaseScheduler):
    
    def open(self, spider):
        """
        Override open method because newest scrapy-redis does not use from_spider when initializing df object
        Parameters
        ----------
        spider

        Returns
        -------

        """
        self.spider = spider
        
        try:
            self.queue = load_object(self.queue_cls)(
                server=self.server,
                spider=spider,
                key=self.queue_key % {'spider': spider.name},
                serializer=self.serializer,
            )
        except TypeError as e:
            raise ValueError("Failed to instantiate queue class '%s': %s",
                             self.queue_cls, e)
        
        try:
            self.df = load_object(self.dupefilter_cls).from_spider(spider)
        except TypeError as e:
            raise ValueError("Failed to instantiate dupefilter class '%s': %s",
                             self.dupefilter_cls, e)
        
        if self.flush_on_start:
            self.flush()
        # notice if there are requests already in the queue to resume the crawl
        if len(self.queue):
            spider.log("Resuming crawl (%d requests scheduled)" % len(self.queue))
