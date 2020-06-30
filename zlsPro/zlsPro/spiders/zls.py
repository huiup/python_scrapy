# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from redis import Redis
from zlsPro.items import ZlsproItem


class ZlsSpider(CrawlSpider):
    name = 'zls'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.4567kan.com/frim/index1.html']
    conn = Redis(host='127.0.0.1', port=6379)
    rules = (
        Rule(LinkExtractor(allow=r'index1\-\d+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # 解析电影的名称和电影详情页的url
        li_list = response.xpath('/html/body/div[1]/div/div/div/div[2]/ul/li')
        for li in li_list:
            item = ZlsproItem()
            title = li.xpath('./div/a/@title').extract_first()
            detail_url = 'https://www.4567kan.com/' + li.xpath('./div/a/@href').extract_first()

            ex = self.conn.sadd('movie_urls', detail_url)
            # ex == 1:插入成功，ex == 0插入失败
            if ex == 1:  # 说明detail_url表示的电影没有存在于记录表中
                # 爬取电影详情页数据：发起请求
                print('有新数据更新，正在爬取新数据......')
                item = ZlsproItem()
                item['title'] = title
                yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'item': item})
            else:  # 存在于记录表中
                print('暂无数据更新！')

    def parse_detail(self, response):
        # 解析电影简介
        desc = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[5]/span[2]/text()').extract_first()
        item = response.meta['item']
        item['desc'] = desc
        yield item
