#-*- encoding: utf-8 -*-
import redis
from copy import deepcopy
from scrapy import cmdline
import pymongo

from geospider.spiders.shop_main_spider import ShopMainSpider

client = pymongo.MongoClient('mongodb://localhost:27017')
db_name = 'geospider'
db = client[db_name]

def start():
    #conn_table = db['task']
    #print conn_table.find_one({'_id': ObjectId('591eb2df9c1da9154b001832')}).get('starturls')

    b = deepcopy(ShopMainSpider)
    b.name='5953322595a1551602965038'
    b.redis_key = "5953322595a1551602965038:start_urls"
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    # r.sadd("myspider:start_urls", 'http://news.qq.com/')
    r.lpush("5953322595a1551602965038:start_urls", "http://www.dangdang.com/")
    # r.lpush("aaa:start_urls", "http://news.sohu.com/")
    b.allowed_domains=["dangdang.com"]
    cmdline.execute("scrapy crawl 5953322595a1551602965038".split())

    # process = CrawlerProcess(get_project_settings())
    # process.crawl(news_spider)
    # process.start()  # the script will block here until the crawling is finished

def pause():
    cmdline.execute("".split())

if __name__ == '__main__':
    start()

