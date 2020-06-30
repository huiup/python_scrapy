# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from time import sleep
from scrapy.http import HtmlResponse  # scrapy封装好的响应类



class WangyiproDownloaderMiddleware:
    def process_request(self, request, spider):
        return None

    # 拦截所有的响应对象
    # 整个工程发起的请求：1+5+n，相应也会有1+5+n个响应对象
    # 只有指定的5个响应对象不满足需求
    # 只将不满足需求的5个指定响应对象的响应数据进行篡改
    def process_response(self, request, response, spider):

        # 将拦截到的所有相应对象中指定的5个响应对象找出
        if request.url in spider.model_urls:
            bro = spider.bro
            # response表示的即使指定的不满足需求的5个响应对象
            # 篡改响应数据：首先先获取满足需求的响应数据，将其篡改到响应对象中
            # 满足需求的响应数据可以使用selenium获取
            bro.get(request.url)  # 对5个板块的url发起请求
            sleep(2)
            bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            sleep(2)
            # 捕获到板块页面中加载出来的全部数据(包含了动态加载数据)
            page_text = bro.page_source
            # 返回一个新的响应对象，新的对象替换原来不满足需求的旧的响应对象
            return HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)  # 5

            # 也可以这样
            # response.text = page_text #但会报错AttributeError: can't set attribute

            # return response
        else:
            return response  # 1+n

    def process_exception(self, request, exception, spider):
        pass