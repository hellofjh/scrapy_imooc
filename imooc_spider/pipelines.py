# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from .spiders.imooc import ImoocSpider


class ImoocSpiderPipeline:
    def process_item(self, item, spider):
        return item

class ImoocMongoDbPipeline:
    def __init__(self):
        self.client = pymongo.MongoClient(host='localhost', port=27017)  # 建立连接池
        # 创建数据库与集合后，需要在集合插入数据，数据库与集合才会真正创建
        self._db = self.client['imooc_database']  # 创建数据库
        self._col = self._db['imooc_collection']  # 创建集合

    def process_item(self, item, spider):
        if isinstance(spider, ImoocSpider): # 判读imooc爬虫类
            data = dict(item)
            self._col.insert_one(data)

        return item

class ImoocImagePipeline(ImagesPipeline):
    # 根据指定数据进行爬取
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['course_img_urls'])

    # 下载完成后 处理结果
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    # def file_path(self, request, response=None, info=None):
    #     # 用于给下载的图片设置文件名称的
    #     url = request.url
    #     file_name = url.split('/')[-1]
    #     return file_name
