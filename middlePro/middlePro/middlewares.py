# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class MiddleproDownloaderMiddleware:

    # 拦截所有(正常&异常)的请求
    # 参数：request就是拦截到的请求，spider就是爬虫类(middle.py)实例化的对象
    def process_request(self, request, spider):
        print('process_request')
        # 可在此处进行一下操作
        request.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        request.headers['Cookie'] = 'xxx'

        return None

    # 拦截所有的相应
    # 参数：response就是拦截到的相应对象，request响应对象对应的请求对象
    def process_response(self, request, response, spider):
        print('process_response')
        return response

    # 拦截异常的请求
    # 参数：request就是拦截到的发生异常的请求
    # 作用：将异常的请求进行修正，将其变成正常的请求，然后对其进行重新发送
    def process_exception(self, request, exception, spider):
        # 请求的ip被禁掉，该请求就会变成一个异常请求
        # request.meta['proxy'] = 'http://ip:port' # 可在此处设置代理
        print('process_exception')
        # return request  # 将异常的请求修正后，将其进行重新发送；若不修正，将会陷入死循环

    # 用不到
    # def spider_opened(self, spider):
    #     spider.logger.info('Spider opened: %s' % spider.name)
