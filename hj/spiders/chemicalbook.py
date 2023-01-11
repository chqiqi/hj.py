import scrapy
from scrapy.http import Request
from urllib import parse
import json
import time

class ChemicalbookSpider(scrapy.Spider):
    name = 'chemicalbook'
    allowed_domains = ['www.chemicalbook.com']
    start_urls = ['https://www.chemicalbook.com/ProductIndex.aspx']

    def parse(self, response):
        catalog1List = response.css("a.T1")
        for catalog1 in catalog1List:
            catalog1Url = catalog1.css("a::attr(href)").extract_first("")
            catalog1Title = catalog1.css("a::attr(href)").extract_first("")
            print(catalog1Url)
            yield Request(url=parse.urljoin(response.url, catalog1Url), meta={"catalog1Title": catalog1Title},
                          callback=self.parseCatalog1Page)

    def parseCatalog1Page(self, response):
        pass