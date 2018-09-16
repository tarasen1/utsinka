import scrapy


class LaptopItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    discountReason =  scrapy.Field()
    screenSize = scrapy.Field()
    screenResol = scrapy.Field()
    screenMate = scrapy.Field()
    processor = scrapy.Field()
    ram = scrapy.Field()
    hdd = scrapy.Field()
    ssd = scrapy.Field()
    gpu_brand = scrapy.Field()
    gpu_mem = scrapy.Field()
    extras = scrapy.Field()
    os = scrapy.Field()
    weight = scrapy.Field()
    color = scrapy.Field()
    url = scrapy.Field()
