from scrapy.cmdline import execute
import os
import sys
if __name__ == '__main__':

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy','crawl','duquanben'])
    # execute(['scrapy','crawl','duquanben','-s','CLOSESPIDER_ITEMCOUNT=100'])
