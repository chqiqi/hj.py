import scrapy


class ChemicalbookSpider(scrapy.Spider):
    name = 'chemicalbook'
    allowed_domains = ['www.chemicalbook.com']
    start_urls = ['http://www.chemicalbook.com/']

    def parse(self, response):
        pass
