import logging
import time
from .defaults import BLOOMFILTER_HASH_NUMBER, BLOOMFILTER_BIT, DUPEFILTER_DEBUG
from . import defaults
from scrapy_redis.connection import get_redis_from_settings
from .bloomfilter import BloomFilter
from scrapy_redis.dupefilter import RFPDupeFilter as BaseDupeFilter

logger = logging.getLogger(__name__)


class RFPDupeFilter(BaseDupeFilter):
    """Redis-based request duplicates filter.

    This class can also be used with default Scrapy's scheduler.

    """
    
    logger = logger
    
    def __init__(self, server, key, debug, bit, hash_number):
        """Initialize the duplicates filter.

        Parameters
        ----------
        server : redis.StrictRedis
            The redis server instance.
        key : str
            Redis key Where to store fingerprints.
        debug : bool, optional
            Whether to log filtered requests.

        """
        self.server = server
        self.key = key
        self.debug = debug
        self.bit = bit
        self.hash_number = hash_number
        self.logdupes = True
        self.bf = BloomFilter(server, self.key, bit, hash_number)
    
    @classmethod
    def from_settings(cls, settings):
        """Returns an instance from given settings.

        This uses by default the key ``dupefilter:<timestamp>``. When using the
        ``scrapy_redis.scheduler.Scheduler`` class, this method is not used as
        it needs to pass the spider name in the key.

        Parameters
        ----------
        settings : scrapy.settings.Settings

        Returns
        -------
        RFPDupeFilter
            A RFPDupeFilter instance.


        """
        server = get_redis_from_settings(settings)
        # XXX: This creates one-time key. needed to support to use this
        # class as standalone dupefilter with scrapy's default scheduler
        # if scrapy passes spider on open() method this wouldn't be needed
        # TODO: Use SCRAPY_JOB env as default and fallback to timestamp.
        key = defaults.DUPEFILTER_KEY % {'timestamp': int(time.time())}
        debug = settings.getbool('DUPEFILTER_DEBUG', DUPEFILTER_DEBUG)
        bit = settings.getint('BLOOMFILTER_BIT', BLOOMFILTER_BIT)
        hash_number = settings.getint('BLOOMFILTER_HASH_NUMBER', BLOOMFILTER_HASH_NUMBER)
        return cls(server, key=key, debug=debug, bit=bit, hash_number=hash_number)
    
    @classmethod
    def from_crawler(cls, crawler):
        """Returns instance from crawler.

        Parameters
        ----------
        crawler : scrapy.crawler.Crawler

        Returns
        -------
        RFPDupeFilter
            Instance of RFPDupeFilter.

        """
        instance = cls.from_settings(crawler.settings)
        return instance
    
    @classmethod
    def from_spider(cls, spider):
        """Returns instance from crawler.

        Parameters
        ----------
        spider :

        Returns
        -------
        RFPDupeFilter
            Instance of RFPDupeFilter.

        """
        settings = spider.settings
        server = get_redis_from_settings(settings)
        dupefilter_key = settings.get("SCHEDULER_DUPEFILTER_KEY", defaults.SCHEDULER_DUPEFILTER_KEY)
        key = dupefilter_key % {'spider': spider.name}
        debug = settings.getbool('DUPEFILTER_DEBUG', DUPEFILTER_DEBUG)
        bit = settings.getint('BLOOMFILTER_BIT', BLOOMFILTER_BIT)
        hash_number = settings.getint('BLOOMFILTER_HASH_NUMBER', BLOOMFILTER_HASH_NUMBER)
        print(key, bit, hash_number)
        instance = cls(server, key=key, debug=debug, bit=bit, hash_number=hash_number)
        return instance
    
    def request_seen(self, request):
        """Returns True if request was already seen.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        bool

        """
        fp = self.request_fingerprint(request)
        # This returns the number of values added, zero if already exists.
        if self.bf.exists(fp):
            return True
        self.bf.insert(fp)
        return False
    
    def log(self, request, spider):
        """Logs given request.

        Parameters
        ----------
        request : scrapy.http.Request
        spider : scrapy.spiders.Spider

        """
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False
        spider.crawler.stats.inc_value('bloomfilter/filtered', spider=spider)
