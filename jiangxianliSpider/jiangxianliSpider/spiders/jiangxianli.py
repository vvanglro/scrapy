import scrapy
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class JiangxianliSpider(scrapy.Spider):
    name = 'jiangxianli'   #爬虫名字必须唯一
    allowed_domains = ['ip.jiangxianli.com']   #允许采集的域名
    start_urls = ['https://ip.jiangxianli.com/?page=1']   #开始采集的网站

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        self.wb = webdriver.Chrome(desired_capabilities=capa,options=options)
        # self.wb.implicitly_wait(10)
        # self.wb.maximize_window()

    def closed(self,spider):
        self.wb.quit()
        print('爬取结束，关闭浏览器')
    # 解析响应数据、提取数据或者网址等
    def parse(self, response):
        # print(response.body)
        selectors = response.xpath('//tbody/tr')  #选择所有的tr标签
        for selector in selectors:
            ip = selector.xpath('./td[1]/text()').get()   #在当前节点下继续选择
            port = selector.xpath('./td[2]/text()').get()
            # print(ip, port)
            items = {
                'ip':ip,
                'port': port
            }
            yield items
        # page_num = WebDrive
        # rWait(self.wb, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'layui-laypage-next')))
        # data_page = page_num.get_attribute("data-page")
        # print(data_page)
        # print(response.body)
        next_page = response.xpath("//a[@class='layui-laypage-next']/@data-page").get()
        # print(next_page)
        if next_page:
            next_page = '?page=' + next_page
            next_url = response.urljoin(next_page)
            # print(next_url)
            yield scrapy.Request(next_url, callback=self.parse)
    # def page_parse(self, response):
    #     #翻页操作