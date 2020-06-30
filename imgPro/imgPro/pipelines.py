# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline  # 提供了数据下载功能(包括视音频)
import scrapy


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# 该默认管道无法帮助我们请求图片数据，因此不用此管道
# class ImgproPipeline:
#     def process_item(self, item, spider):
#         print(item)
#         return item

# 管道需要接收item中的图片地址和名称，然后再在管道中请求到图片
# 的数据对其进行持久化存储

class ImgsPipeline(ImagesPipeline):
    # 根据图片地址发起请求
    def get_media_requests(self, item, info):
        # print(item)
        yield scrapy.Request(url=item['url'], meta={'item': item})

    # 返回图片名称即可
    def file_path(self, request, response=None, info=None):
        # 通过request获取meta，而不是response
        item = request.meta['item']
        print(item)
        fil_path = item['name']
        return fil_path  # 只需要返回图片名字,需在setting中设置IMAGES_STORE(图片保存路径)

    # 将item传递给下一个即将被执行的管道类
    def item_completed(self, results, item, info):
        return item
