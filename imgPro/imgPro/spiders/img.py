# -*- coding: utf-8 -*-
import scrapy
from imgPro.items import ImgproItem

class ImgSpider(scrapy.Spider):
    name = 'img'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://pic.netbian.com/4kdongman/']
    url2 = 'http://pic.netbian.com/4kdongman/index_%d.html'
    page_num = 2

    def parse(self, response):
        # 解析图片地址和图片名称
        li_list = response.xpath('//*[@id="main"]/div[3]/ul/li')
        for li in li_list:
            img_name = li.xpath('./a/b/text()').extract_first() + '.jpg'
            img_url = 'http://pic.netbian.com/' + li.xpath('./a/img/@src').extract_first()

            item = ImgproItem()
            item['name'] = img_name
            item['url'] = img_url

            yield item

        # 爬取多页
        if self.page_num < 5:
            new_url = format(self.url2 % self.page_num)
            self.page_num += 1
            yield scrapy.Request(url=new_url, callback=self.parse)
