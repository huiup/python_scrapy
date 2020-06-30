# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from redis import Redis


class Test2Pipeline:
    fp = None

    # 重写父类的两个方法
    def open_spider(self, spider):
        print('我是open_spider()，我只会在爬虫开始时执行一次')
        self.fp = open('duanzi.txt', 'w', encoding='utf-8')

    def close_spider(self, spider):
        print('我是close_spider()，我只会在爬虫结束时执行一次')
        self.fp.close()

    # 该方法是用来接受item对象
    # 参数item：就是接受到的item对象。一次只能接收一个item，说明该方法会被调用多次
    def process_item(self, item, spider):
        # 将item存储到文本文件
        self.fp.write(item['title'] + ':' + item['content'] + '\n')
        return item


# 将数据存储到mysql中
class MysqlPipeline(object):
    conn = None
    cursor = None

    # 重写父类的两个方法
    def open_spider(self, spider):
        self.conn = pymysql.Connect(host='localhost', user='root', password='huihuiyo', db='scrapy', charset='utf8')
        print(self.conn)

    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()
        sql = 'insert into spider values ("%s","%s")' % (item['title'], item['content'])
        # 事务处理
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()


class RedisPipeline(object):
    conn = None
    # 只有redis模块的版本为2.10.6才支持把字典写入redis
    # pip install -U redis==2.10.6
    def open_spider(self, spider):
        self.conn = Redis(host='127.0.0.1', port='6379')
        print(self.conn)

    def process_item(self, item, spider):
        self.conn.lpush('duanziData', item)
