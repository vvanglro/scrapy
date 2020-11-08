# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class JiangxianlispiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JiangxianlispiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response



    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumTaobaoDownloaderMiddleware(object):
    # 将driver创建在中间件的初始化方法中，适合项目中只有一个爬虫。
    # 爬虫项目中有多个爬虫文件的话，将driver对象的创建放在每一个爬虫文件中。
    # def __init__(self):
    #     # 在scrapy中创建driver对象，尽可能少的创建该对象。
    #     # 1. 在初始化方法中创建driver对象；
    #     # 2. 在open_spider中创建deriver对象；
    #     # 3. 不要将driver对象的创建放在process_request()；
    #     option = FirefoxOptions()
    #     option.headless = True
    #     self.driver = webdriver.Firefox(options=option)
    # 参数spider就是TaobaoSpider()类的对象

    # wb = spider.wb
    # wb.get(url=request.url)
    # wait = WebDriverWait(wb, 10)  # 创建一个等待10秒的对象
    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'layui-laypage-next')))
    # # page_num = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'layui-laypage-next')))
    # # data_page = page_num.get_attribute("data-page")
    # # 获取页面源码，这里有我们需要的动态加载的数据
    # page_text = wb.page_source
    # # 创建一个新的响应对象，并将动态加载到的数据存入该对象中，然后返回该对象
    # return HtmlResponse(url=wb.current_url, body=page_text, encoding='utf-8', request=request)
    def process_request(self, request, spider):
        if spider.name == "jiangxianli":
            spider.wb.get(request.url)
            # 由于淘宝的页面数据加载需要进行滚动，但并不是所有js动态数据都需要滚动。
            # for x in range(1, 11, 2):
            #     height = float(x) / 10
            #     js = "document.documentElement.scrollTop = document.documentElement.scrollHeight * %f" % height
            #     spider.driver.execute_script(js)
            #     time.sleep(0.2)
            WebDriverWait(spider.wb, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'layui-laypage-next')))
            spider.wb.execute_script("window.stop();")
            origin_code = spider.wb.page_source
            # 将源代码构造成为一个Response对象，并返回。
            res = HtmlResponse(url=request.url, encoding='utf8', body=origin_code, request=request)
            # res = Response(url=request.url, body=bytes(origin_code), request=request)
            return res
        # if spider.name == 'bole':
        #         #     request.cookies = {}
        #         #     request.headers.setDefault('User-Agent', '')
        #         # return None

    def process_response(self, request, response, spider):
        return response
