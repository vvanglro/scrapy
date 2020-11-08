import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from  ..items import DuquanbenspiderItem

class DuquanbenSpider(CrawlSpider):
    name = 'duquanben'
    allowed_domains = ['www.duquanben.com']
    start_urls = ['https://www.duquanben.com/']

    # allow和restrict_xpaths匹配规则
    # callback匹配到之后的回调函数
    # process_links对匹配到的连接进行过滤修改的函数
    rules = (
        Rule(LinkExtractor(allow=(r'.*/xiazai/\d+/\d+/'), restrict_xpaths=('//*[@id="container"]/div/div[@class="hot-data"]//h5')), callback='parse_item', process_links='deal_links'),
        # Rule(LinkExtractor(allow=(r'.*/xiazai/\d+/\d+/'), restrict_xpaths=('//*[@id="container"]/div/div[@class="hot-data"]')), callback='parse_item'),
        # Rule(LinkExtractor(allow=(r'.*/xiazai/[0-9]/[0-9].*'), restrict_xpaths=('//*[@id="container"]/div/div[@class="hot-data"]')), callback='parse_item'),
        # Rule(LinkExtractor(allow=r'.*/xiazai/[0-9]/[0-9].*'), callback='parse_item', follow=True),
    )

    def deal_links(self,links):
        '''
        :param links: 匹配到的url 是个list
        :return: 返回修改完后的links连接列表
        '''
        # 要想links里返回的text有内容 则rules里的匹配规则匹配到的链接标签有包含text
        print('deal_links的links：',links)  # output: deal_links的links：[Link(url='https://www.duquanben.com/xiazai/9/9456/', text='斗破苍穹TXT下载', fragment='', nofollow=False), Link(url='https://www.duquanben.com/xiazai/5/5823/', text='盗墓笔记TXT下载', fragment='', nofollow=False), Link(url='https://www.duquanben.com/xiazai/13/13466/', text='绝世武神TXT下载', fragment='', nofollow=False), Link(url='https://www.duquanben.com/xiazai/0/910/', text='斗罗大陆TXT下载', fragment='', nofollow=False), Link(url='https://www.duquanben.com/xiazai/14/14727/', text='尸兄TXT下载', fragment='', nofollow=False), Link(url='https://www.duquanben.com/xiazai/13/13695/', text='余罪TXT下载', fragment='', nofollow=False)]
        print('deal_links的links类型：',type(links))
        for link in links:
            print('link.url是:',link.url)
        return links[:1]
    def parse_item(self, response):
        '''
        :param response:
        :return: xsurl: href="https://www.duquanben.com/xiaoshuo/9/9456/"
        '''
        print('匹配到的url：',response.url)
        xsurl = response.xpath("//span[@class='btopt']/a/@href").get()

        # if 'm.' in xsurl:
        #     xsurl = xsurl.replace('m.','www.')
        print('小说的xsurl:',xsurl)
        if xsurl:
            yield scrapy.Request(xsurl, callback=self.parse_detail)


    def parse_detail(self, response):
        '''
        :param response:
        :return:  read_url: xsurl + href="1796979.html"   https://www.duquanben.com/xiaoshuo/9/9456/1796979.html
        '''
        xsurl = response.url
        # print('这是parse_detail的xsurl：',xsurl)
        # book_name = response.xpath("//div[@class='mu_h1']/h1/text()").get()
        section_tail_url_lists = response.xpath("//ul[@class='mulu_list']/li/a/@href").extract()
        for i, section_tail_url in enumerate(section_tail_url_lists):
            read_url = xsurl + section_tail_url
            yield scrapy.Request(read_url, callback=self.parse_end, cb_kwargs={'order': i + 1})

    def parse_end(self,response,order):
        item = DuquanbenspiderItem()
        item['order'] = order
        item['book_name'] = response.xpath("//div[@class='weizhi']/a[3]/text()").get()
        title_name = response.xpath("//div[@class='h1title']/h1/text()").get()
        contentbox =''.join(response.xpath("//div[@class='contentbox']/text()").extract()).strip().replace('\r','').replace('\t','').replace('\n','').replace('\xa0','')
        # contentbox =''.join(response.xpath("//div[@class='contentbox']/text()").extract()).replace('\n','').replace('\xa0','')
        content = title_name + '\n' + contentbox
        item['content'] = content
        yield item



