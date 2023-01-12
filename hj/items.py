# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HjItem(scrapy.Item):
    #中文名称
    name = scrapy.Field()
    #英文名称
    enname = scrapy.Field()
    #CAS号
    casno = scrapy.Field()
    #分子式
    formula = scrapy.Field()
    #分子量
    weight = scrapy.Field()
    #毒害物质数据
    dangerInfoUrl = scrapy.Field()


