# -*- coding: utf-8 -*-
import scrapy
from test2.items import Test2Item


class DuanziproSpider(scrapy.Spider):
    name = 'duanziPro'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://duanziwang.com/category/经典段子/']

    # 数据解析
    # def parse(self, response):
    #     # 数据解析名称和内容
    #     article_list = response.xpath('/html/body/section/div/div/main/article')
    #     for article in article_list:
    #         # 下面解析出来的内容不是字符串数据，所以此处的xpath与etree中的xpath使用方式不同
    #         # xpath返回的列表中存储的是Selector对象，我们要获取的字符串数据被存储在了该对象的data属性中
    #         # 取出的是Selector对象
    #         # title = article.xpath('./div[1]/h1/a/text()')[0].extract()
    #         # content = article.xpath('./div[2]/p/text()')[0].extract()
    #
    #         # 将Selector对象中的data属性值取出
    #         # extract()就是将data属性值取出
    #         # title = article.xpath('./div[1]/h1/a/text()')[0].extract()
    #         # content = article.xpath('./div[2]/p/text()')[0].extract()
    #
    #         # extract_first():将列表中的第一个元素表示的Selector对象中的data属性值取出
    #         title = article.xpath('./div[1]/h1/a/text()').extract_first()
    #         content = article.xpath('./div[2]/p/text()').extract_first()
    #
    #         # extract():直接使用列表调用extract()：可以将列表中的每一个元素Selector中的data属性取出
    #         # title = article.xpath('./div[1]/h1/a/text()').extract()
    #         # content = article.xpath('./div[2]/p/text()').extract()
    #         print(title, content)
    #         # break

    # 将解析到的数据进行持久化存储：基于终端指令的持久化存储
    # def parse(self, response):
    #     all_data = []
    #     article_list = response.xpath('/html/body/section/div/div/main/article')
    #     for article in article_list:
    #         # extract_first():将列表中的第一个列表元素表示的Selector对象中的data属性值取出
    #         title = article.xpath('./div[1]/h1/a/text()').extract_first()
    #         content = article.xpath('./div[2]/p/text()').extract_first()
    #         dict = {
    #             'title':title,
    #             'content':content
    #         }
    #         all_data.append(dict)
    #     return all_data

    # 将解析到的数据进行持久化存储：基于管道的持久化存储
    def parse(self, response):
        all_data = []
        article_list = response.xpath('/html/body/section/div/div/main/article')
        for article in article_list:
            # extract_first():将列表中的第一个列表元素表示的Selector对象中的data属性值取出
            title = article.xpath('./div[1]/h1/a/text()').extract_first()
            content = article.xpath('./div[2]/p/text()').extract_first()

            # 实例化一个item对象，将解析到的数据存储到该对象中
            item = Test2Item()
            # 也可以使用字典
            # item = dict()
            # 不可用通过.的形式调用属性
            item['title'] = title
            item['content'] = content

            # 将item对象提交给管道
            yield item




