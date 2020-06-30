# -*- coding: utf-8 -*-
import scrapy
from handReq.items import HandreqItem


class DuanziSpider(scrapy.Spider):
    name = 'duanzi'
    allowed_domains = ['duanziwang.com']
    start_urls = ['https://duanziwang.com/category/经典段子/1/']

    # 通用url模板
    url = 'https://duanziwang.com/category/经典段子/%d/'
    page_num = 2

    # 父类方法
    # def start_requests(self):
    #     for u in self.start_urls:
    #         yield scrapy.Request(url=u, callback=self.parse)

    # 将段子王网页中的所有页码对应的数据进行爬取
    def parse(self, response):
        all_data = []
        article_list = response.xpath('/html/body/section/div/div/main/article')
        for article in article_list:
            # extract_first():将列表中的第一个元素即Selector对象中的data属性值取出
            title = article.xpath('./div[1]/h1/a/text()').extract_first()
            content = article.xpath('./div[2]/p/text()').extract_first()

            # 实例化一个item对象，将解析到的数据存储到该对象中
            item = HandreqItem()
            item['title'] = title
            item['content'] = content
            # 将item对象提交给管道
            yield item

        if self.page_num < 5:
            new_url = format(self.url % self.page_num)
            self.page_num += 1
            # 对新的页码的url进行请求发送(手动GET请求发送)
            yield scrapy.Request(url=new_url, callback=self.parse)
