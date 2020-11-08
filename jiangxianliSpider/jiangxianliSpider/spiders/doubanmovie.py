import scrapy
from jiangxianliSpider.items import DoubanMovieItem

class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanmovie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250?start=0&filter=']

    def parse(self, response):
        item = DoubanMovieItem()
        selectors = response.xpath('//ol/li/div')

        for selector in  selectors:
            item['ranking'] = selector.xpath('.//em/text()').extract()[0]
            item['movie_name'] = selector.xpath('.//a/span[1]/text()').extract()[0]
            item['score'] = selector.xpath('.//span[@class="rating_num"]/text()').extract()[0]
            item['score_num'] = selector.xpath('.//span[4]/text()').extract()[0]

            yield item

        next_page =response.xpath('//span[@class="next"]/a/@href').get()
        if next_page:
            next_url = response.urljoin(next_page)

            yield scrapy.Request(next_url, callback=self.parse)
