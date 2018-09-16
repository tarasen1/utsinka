import scrapy
from scrapy.crawler import CrawlerProcess
from items import LaptopItem
import datetime
import re


class LaptopRozSpider(scrapy.Spider):
    name = "laptop_roz"
    custom_settings = {
        'ITEM_PIPELINES': {
                               'pipelines.MongoPipeline': 300,
                               'pipelines.LaptopCSVPipeline': 200,
                            },
        'FEED_EXPORT_FIELDS' : ['name', 'avaible', 'price', 'currency', 'category', 'sku', 'time', 'size', 'region', 'descr', 'url'],
        'MONGO_SERVER' : 'localhost',
        'MONGO_PORT' : 27017,
        'MONGO_DB' : 'utsinka',
        'MONGO_COLLECTION' : 'laptops'
    }
    # settings = {
    #     'MONGO_SERVER' : 'localhost',
    #     'MONGO_PORT' : 27017,
    #     'MONGO_DB' : 'utsinka',
    #     'MONGO_COLLECTION' : 'laptops'
    # }
    def __init__(self, *args, **kwargs):
        super(LaptopRozSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_urls')]
        self.counter = 0

    def parse(self, response):
        num_pages = response.css('a.novisited.paginator-catalog-l-link::text').extract()
        num_pages = max([int(el) for el in num_pages if el.isnumeric() ])
        for page in range(1, num_pages+1):
            new_resp = response.urljoin('page={}/'.format(page))
            yield scrapy.Request(new_resp, callback=self.parseGoods)
    def parseGoods(self, response):
        goods = response.css('div.g-i-tile.g-i-tile-catalog')

        for result in goods:
            if result.extract().find('name="more_goods">')>0:
                return
            else:
                self.counter += 1
                print('##########################\n',self.counter)
                item = LaptopItem()
                item['name'] = result.css('div.g-i-tile-i-title.clearfix').css('a::text').extract_first()[1:-1]
                item['price'] = int(result.css('div.g-price-uah::text').extract_first().encode('ascii', 'ignore'))
                item['old_price'] = int(result.css('div.g-price-old-uah::text').extract_first().encode('ascii', 'ignore'))

                item['url'] = result.css('div.g-i-tile-i-title.clearfix').css('a::attr(hrefpip)').extract_first()

                data_string = result.css('div.short-description::text').extract_first()
                print(data_string)
                data_string = data_string[1:-1].split('/')

                if data_string[-1].find('+')>0:
                    data_string.pop(-1)

                screen_info = data_string[0].split()

                item['screenSize'] = screen_info[1]
                item['screenResol'] = screen_info[2][1:-1]
                item['screenMate'] = screen_info[-1]
                del screen_info

                item['processor'] = data_string[1]
                item['ram'] = data_string[2]

                rom_info = data_string[3]
                if len(rom_info.split('+')) == 1:
                    item['hdd'] = data_string[3] if data_string[3].lower().find('hdd') > 0 else None
                    item['ssd'] = data_string[3] if data_string[3].lower().find('ssd') > 0 else None
                elif len(rom_info.split('+')) > 1:
                    item['hdd'] = [el for el in rom_info.split('+') if el.lower().find('hdd') > 0]
                    item['ssd'] = [el for el in rom_info.split('+') if el.lower().find('ssd') > 0]
                del rom_info

                gpu_info = data_string[4].split(',')
                item['gpu_brand'] = gpu_info[0]
                item['gpu_mem'] = gpu_info[1] if len(gpu_info)>1 else None

                item['extras'] = str(data_string[5:-3])[1:-1]
                item['os'] = data_string[-3]
                item['weight'] = data_string[-2]
                item['color'] = data_string[-1]

                #if item['name'] is not None:
                yield item






if __name__ == '__main__':
    process = CrawlerProcess()
    start_urls = [  'https://rozetka.com.ua/ua/utsenennye-noutbuki/c83853/'
                    ]

    for url in start_urls:
        process.crawl(LaptopRozSpider, start_urls=url)
    process.start()
