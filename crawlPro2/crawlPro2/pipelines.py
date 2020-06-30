# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class Crawlpro2Pipeline:
    def process_item(self, item, spider):
        print(item)
        # if item.__class__.__name__ == 'Crawlpro2Item':
        #     title = item['title']
        #     status = item['status']
        #     print(title+':'+status)
        # else:
        #     content = item['content']
        #     print(content)
        return item
