# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrawlTestSpider(CrawlSpider):
    name = 'crawl_test'
    # allowed_domains = ['www.521609.com']
    start_urls = ['http://www.521609.com/daxuexiaohua/']

    # 实例化LinkExtractor对象
    # 连接提取器：根据指定规则(allow参数)在页面中进行链接(url)的提取
    # allow='正则'：提取链接的规则
    link = LinkExtractor(allow=r'list\d+\.html')
    # link = LinkExtractor(allow=r'')  # 取出网站全站的链接
    rules = (
        # 实例化一个Rule对象
        # 规则解析器：接受链接提取器提取到的链接，对其发起请求，然后根据指定规则(callback)解析数据
        Rule(link, callback='parse_item', follow=True),
        # follow=True：
        # 将链接提取器作用到 链接提取器提取到的页码所对应的页面中
    )

    def parse_item(self, response):
        print(response)
        # 基于response实现数据解析
        # response.xpath()
