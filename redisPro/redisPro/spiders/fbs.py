# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from redisPro.items import RedisproItem


class FbsSpider(RedisCrawlSpider):
    name = 'fbs'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['http://www.xxx.com/']
    redis_key = 'sunQueue'  # 可以被共享的调度器队列的名称，相当于start_urls
    # 之后需要将一个起始的url手动的添加到redis_key表示的队列中

    link = LinkExtractor(allow=r'id=1&page=\d+')
    rules = (
        Rule(link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # 获取全站的标题
        li_list = response.xpath('/html/body/div[2]/div[3]/ul[2]/li')
        for li in li_list:
            title = li.xpath('./span[3]/a/text()').extract_first()
            item = RedisproItem()
            item['title'] = title
            yield item
