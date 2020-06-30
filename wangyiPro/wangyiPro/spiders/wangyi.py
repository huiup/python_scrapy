# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from wangyiPro.items import WangyiproItem


class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://news.163.com/']
    model_urls = []  # 每一个板块对应的url

    # 实例化一个全局的浏览器对象
    bro = webdriver.Chrome(executable_path='D:\scrapy\chromedriver.exe')

    # 解析每一个板块所对应的url
    def parse(self, response):
        li_list = response.xpath(
            '//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        indexs = [3, 4, 6, 7, 8]
        for index in indexs:
            model_li = li_list[index]
            model_url = model_li.xpath('./a/@href').extract_first()
            self.model_urls.append(model_url)
            for url in self.model_urls:
                yield scrapy.Request(url=url, callback=self.parse_model)

    # 解析新闻标题+新闻详情页的url
    def parse_model(self, response):
        # 直接对response解析新闻标题数据是无法获取该数据的(动态加载)
        # 满足需求的响应对象就是包含了动态加载数据的response
        # 满足需求的response和不满足的response区别在哪里？
        #   -区别在于响应数据不同。我可以使用中间件将不满足需求的响应数据篡改成
        # 包含了动态加载数据的响应数据，将其变成满足需求的响应数据
        div_list = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div/div/ul/li/div/div')
        for div in div_list:
            title = div.xpath('./div/div[1]/h3/a/text()').extract_first()
            news_detail_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()
            if news_detail_url:
                item = WangyiproItem()
                item['title'] = title
                # 对新闻详情页的url发起请求
                yield scrapy.Request(url=news_detail_url, callback=self.parse_new_detail, meta={'item': item})

    def parse_new_detail(self, response):
        # 解析新闻内容
        content = response.xpath('//*[@id="endText"]/p/text()').extract()
        content = ''.join(content)
        item = response.meta['item']
        item['content'] = content
        yield item


    # 爬虫类父类的方法，会在爬虫结束最后一刻执行
    def closed(self,spider):
        self.bro.quit()