# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ZlsproPipeline:
    def process_item(self, item, spider):
        # 获取redis链接对象
        # 第三方库redis升级到3.0后仅接受用户数据为字节、字符串或数字（整数，长整数和浮点数）
        # 写入item会报错，需要使用低版本的redis
        # pip install redis==2.10.6
        conn = spider.conn
        conn.lpush('movieData', item)
        return item
