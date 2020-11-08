# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JiangxianlispiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DoubanMovieItem(scrapy.Item):
    # 排名
    ranking = scrapy.Field()
    # 电影名称
    movie_name = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 评论人数
    score_num = scrapy.Field()

class JianShu(scrapy.Item):
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