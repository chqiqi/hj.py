# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Identity

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
    #毒害物质数据-
    dangerInfoTxt = scrapy.Field()
    #毒害物质数据
    dangerInfoUrl = scrapy.Field()
    #类目名称
    catalogTitle = scrapy.Field()
    # 分子结构图
    formulaImgAddr = scrapy.Field()
    formulaImgUrl = scrapy.Field(
        output_processor=Identity()
    )


