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


class ImoocSpiderPipeline:
    def __init__(self):
        self.client = pymongo.MongoClient(host='localhost', port=27017)  # 建立连接池
        # 创建数据库与集合后，需要在集合插入数据，数据库与集合才会真正创建
        self._db = self.client['test_database']  # 创建数据库
        self._col = self._db['test_collection']  # 创建集合

    def process_item(self, item, spider):
        data = dict(item)
        self._col.insert_one(data)
        return item

class ImoocImagePipeline(ImagesPipeline):
    # 根据指定数据进行爬取
    def get_media_requests(self, item, info):
        for image_url in item['course_img_urls']:
            yield scrapy.Request(image_url)

    # 下载完成后 处理结果
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        # item['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        # 用于给下载的图片设置文件名称的
        url = request.url
        file_name = url.split('/')[-1]
        return file_name
