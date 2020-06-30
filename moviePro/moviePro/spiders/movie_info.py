# -*- coding: utf-8 -*-
import scrapy
from moviePro.items import MovieproItem


class MovieInfoSpider(scrapy.Spider):
    name = 'movie_info'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.4567kan.com/frim/index1.html']
    url = 'https://www.4567kan.com/frim/index1-%d.html'
    page_num = 2

    def parse(self, response):
        li_list = response.xpath('/html/body/div[1]/div/div/div/div[2]/ul/li')
        for li in li_list:
            title = li.xpath('./div/a/@title').extract_first()
            detail_url = 'https://www.4567kan.com' + li.xpath('./div/a/@href').extract_first()
            item = MovieproItem()
            item['title'] = title

            # 对详情页url发起请求
            # meta作用：可以将meta字典传递给callback
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'item': item})

        if self.page_num < 3:
            new_url = format(self.url % self.page_num)
            self.page_num += 1
            yield scrapy.Request(url=new_url, callback=self.parse)

    # 用于解析详情页数据
    def parse_detail(self, response):
        # 接收传递过来的meta
        item = response.meta['item']
        desc = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[5]/span[2]/text()').extract_first()
        item['desc'] = desc

        yield item
