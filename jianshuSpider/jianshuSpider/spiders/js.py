import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshuSpider.items import JianShu

class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = JianShu()
        item['url'] = response.url
        item['title'] = response.xpath('//h1[@class="_2zeTMs"]/text()').get()
        item['author'] = response.xpath('//div[@class="_3U4Smb"]/span/a[@class="_1OhGeD"]/text()').get()
        item['writing_time'] = response.xpath('//div[@class="_gp-ck"]//div[@class="s-dsoj"]/time/text()').get()
        item['word_count'] = response.xpath('//div[@class="_gp-ck"]//div[@class="s-dsoj"]/span/text()').extract()[0]
        item['pageview'] = response.xpath('//div[@class="_gp-ck"]//div[@class="s-dsoj"]/span/text()').extract()[1]

        yield item
