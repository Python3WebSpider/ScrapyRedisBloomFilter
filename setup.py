import io
from setuptools import setup, find_packages
import scrapy_redis_bloomfilter


def read_file(filename):
    with io.open(filename) as fp:
        return fp.read().strip()


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name='scrapy-redis-bloomfilter',
    version=scrapy_redis_bloomfilter.__version__,
    description='Scrapy Redis BloomFilter',
    keywords=['scrapy', 'redis', 'bloomfilter'],
    author=scrapy_redis_bloomfilter.__author__,
    email=scrapy_redis_bloomfilter.__email__,
    license='MIT',
    install_requires=read_requirements('requirements.txt'),
    packages=find_packages(),
)
