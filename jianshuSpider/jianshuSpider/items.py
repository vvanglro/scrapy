# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JianShu(scrapy.Item):
    url = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 写作时间
    writing_time = scrapy.Field()
    # 字数
    word_count = scrapy.Field()
    # 阅读数量
    pageview = scrapy.Field()