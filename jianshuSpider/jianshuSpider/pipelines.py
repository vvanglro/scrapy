# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import os

import pymysql
from itemadapter import ItemAdapter


from scrapy.utils.project import get_project_settings


class JianshuspiderPipeline:
    # def process_item(self, item, spider):
    #     path = 'jianshu.csv'
    #     if os.path.exists(path):
    #         with open(file=path, mode="a+",encoding='utf-8_sig', newline='') as f:
    #             writer = csv.writer(f)
    #             writer.writerow([item['url'],item['title'],item['author'],item['writing_time'],item['word_count'],item['pageview']])
    #     else:
    #         with open(file=path, mode="x",encoding='utf-8_sig', newline='') as f:
    #             writer = csv.writer(f)
    #             writer.writerow(['url','标题','作者','发表时间','字数','浏览数'])
    #             writer.writerow([item['url'],item['title'],item['author'],item['writing_time'],item['word_count'],item['pageview']])
    #
    #     return item

    def __init__(self):
        settings = get_project_settings()
        host = settings['MYSQL_HOST']
        user = settings['MYSQL_USER']
        password = settings['MYSQL_PWD']
        port = settings['MYSQL_PORT']
        charset = settings['MYSQL_CHARSET']
        self.conn = pymysql.connect(
            host=host, user=user, passwd=password,
            port=port, charset=charset
        )

        # 游标
        self.cursor = self.conn.cursor()
        # #初始化的表名
        # self.table_name='ceshisql'

    def process_item(self, item, spider):
        keys, values = zip(*item.items())
        table_name = spider.name
        db_name = spider.name + 'project'
        # 是否有项目数据库
        self.cursor.execute('show databases like "{}"'.format(db_name))
        create_db_sql = 'CREATE DATABASE {} DEFAULT CHARACTER SET UTF8 COLLATE utf8_general_ci;'
        # 如果没有则执行创建数据库语句
        self.cursor.execute(create_db_sql.format(db_name)) if self.cursor.fetchone() is None else None
        # 切换到创建好的数据库
        self.cursor.execute('use {}'.format(db_name))
        # 是否有项目表
        self.cursor.execute('show tables  like "{}"'.format(table_name))
        create_table_sql = 'create table {}(id int(5) NOT NULL auto_increment primary key,{});'
        # 如果没有则执行创建表语句
        self.cursor.execute(create_table_sql.format(table_name,','.join(map(lambda x: x + ' varchar(500)', keys)))) if self.cursor.fetchone() is None else None
        sql = "INSERT INTO `{}` ({}) VALUES ({}) ON DUPLICATE KEY UPDATE {}".format(
            table_name,
            ','.join(keys),
            ','.join(['%s'] * len(values)),
            ','.join(['`{}`=%s'.format(k) for k in keys])
        )
        self.cursor.execute(sql, values * 2)
        self.conn.commit()
        return item