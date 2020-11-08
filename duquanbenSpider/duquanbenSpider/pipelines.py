# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

from itemadapter import ItemAdapter


class DuquanbenspiderPipeline(object):

    def __init__(self):
        # 获取到当前文件的目录，并检查是否有 books_directory 文件夹，如果不存在则自动新建 books_directory 文件
        try:
            File_Path = os.getcwd() + '\\' + 'books_directory' + '\\'
            # print(File_Path)
            if not os.path.exists(File_Path):
                os.makedirs(File_Path)
                # return File_Path
            else:
                print("目录已存在！！！")
                # return File_Path
        except BaseException as msg:
            print("新建目录失败：%s" % msg)

    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        # self.items.sort(key=lambda i: i['order'])
        # print(self.items)
        # for item in self.items:
        #     book_name = item['book_name']
        #     with open('./books_directory/{}.txt'.format(book_name), 'a+',encoding = 'utf-8') as f:
        #         f.write(item['content'] + '\n')

        return item

    def close_spider(self, spider):
        self.items.sort(key=lambda i: i['order'])
        for item in self.items:
            book_name = item['book_name']
            with open('./books_directory/{}.txt'.format(book_name), 'a+',encoding = 'utf-8') as f:
                f.write(item['content']+ '\n')


    # def process_item(self, item, spider):
    #
    #     book_name = item['book_name']
    #     with open('./books_directory/{}.txt'.format(book_name), 'a+') as f:
    #         f.write(item['content']+ '\n')
    #
    #     return item
