# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import requests
import json

class XinpianchangPipeline:
    def process_item(self, item, spider):
        url = 'http://localhost:2800/jsonrpc'

        download_url =item['url'][0]
        out = '{}.mp4'.format(item['title'][0])
        print('download_url:',download_url,'out:',out)
        json_rpc = json.dumps(
            {
            'id': '0',
            'jsonrpc': '2.0',
            'method': 'aria2.addUri',
            'params': ['token:7clnzqva80a0mp5h9wnj', [download_url],{'dir': 'D:/Qdown/Download', 'out': out}],
            }
        )
        response = requests.post(url=url, data=json_rpc)
        print(response.json())
        return item
