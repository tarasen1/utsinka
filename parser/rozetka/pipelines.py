import pymongo
from scrapy.exporters import CsvItemExporter


class LaptopCSVPipeline(object):
    def open_spider(self, spider):
        f = open('{}.csv'.format(spider.start_urls[0].replace('/','_')), 'ab')
        self.exporter = CsvItemExporter(f)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.exporter.file.close()
    def process_item(self, item, spider):
        print(':DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
        self.exporter.export_item(item)
        return item


class MongoPipeline(object):
    def __init__(self, mongo_server, mongo_port, mongo_db, mongo_coll):
        self.mongo_server = mongo_server
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db
        self.mongo_coll = mongo_coll


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_server=crawler.settings.get('MONGO_SERVER'),
            mongo_port = crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_coll = crawler.settings.get('MONGO_COLLECTION')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("localhost", 27017)#self.mongo_server, self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        print(':XDXDXDXDXDXDXDXDXDXDXDXDXDXDXDXDXDXDXDXDXDXDXDXDXDXDXDXDXDXDXDXD')
        self.db[self.mongo_coll].insert_one(dict(item))
        return item
