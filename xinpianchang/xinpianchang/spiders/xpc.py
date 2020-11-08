import re
import time

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from xinpianchang.items import XinpianchangItem

class XpcSpider(scrapy.Spider):
    name = 'xpc'
    allowed_domains = ['https://www.xinpianchang.com/']
    start_urls = ['https://www.xinpianchang.com/channel/index/type-/sort-like/duration_type-0/resolution_type-/page-{}'.format(i) for i in range(1,21)]

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def parse(self, response):
        item = XinpianchangItem()
        data_articleids = response.xpath("//div[@class='channel-con']/ul/li/@data-articleid").extract()

        for data_articleid in data_articleids:
            url = 'https://www.xinpianchang.com/a{}?from=ArticleList'.format(data_articleid)
            # print(url)
            self.driver.get(url)
            time.sleep(2)
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'vjs-play-control')))
            source = self.driver.page_source
            down_url = re.findall('src="(.*)" pw',source)
            title = re.findall('<title>(.*)</title>', source)
            item['url'] = down_url
            item['title'] = title

            yield item
        # next_page = response.xpath("//a[@class='layui-laypage-next']/@data-page").get()
        # # print(next_page)
        # if next_page:
        #     next_page = '?page=' + next_page
        #     next_url = response.urljoin(next_page)
        #     # print(next_url)
        #     yield scrapy.Request(next_url, callback=self.parse)