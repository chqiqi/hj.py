import scrapy
from scrapy.http import Request
from urllib import parse
import json
import time
from hj.items import HjItem

class ChemicalbookSpider(scrapy.Spider):
    name = 'chemicalbook'
    allowed_domains = ['www.chemicalbook.com']
    start_urls = ['https://www.chemicalbook.com/ProductIndex.aspx']

    def parse(self, response):
        catalog1List = response.css("a.T1")
        for catalog1 in catalog1List:
            catalog1Url = catalog1.css("a::attr(href)").extract_first("")
            catalog1Title = catalog1.css("a::text").extract_first("")
            print(catalog1Url)
            yield Request(url=parse.urljoin(response.url, catalog1Url), meta={"catalog1Title": catalog1Title,"currUrl":catalog1Url},
                          callback=self.parsePage)

    def parsePage(self, response):
        meta = response.meta
        currUrl = meta.get("currUrl", "")
        if currUrl.startswith( '/ProductChemicalProperties' ):
            item = HjItem()
            baseInfoTrs = response.css("tr[class^='ProdSupplierGN_ProductA']")
            for baseInfo in baseInfoTrs:
                baseInfoTds = baseInfo.css("td")
                if len(baseInfoTds) == 2:
                    fieldName = baseInfoTds[0].css("td::text").extract_first("")
                    fieldValue = baseInfoTds[1].css("td a::text").extract_first("")
                    yield item
        else:
            subCatalogs = response.xpath("//div[@id='tabsort']//a")
            if len(subCatalogs) == 1:
                detailUrls = response.xpath("//dl/dd/em/a")
                for detailUrl in detailUrls:
                    url = detailUrl.css("a::attr(href)").extract_first("")
                    if url.startswith( '/ProductChemicalProperties' ):
                        meta['currUrl'] = url
                        yield Request(url=parse.urljoin(response.url, url),
                                      meta=meta,
                                      callback=self.parsePage)
            else:
                for subCatalog in subCatalogs:
                    subCatalogUrl = subCatalog.css("a::attr(href)").extract_first("")
                    meta['currUrl'] = subCatalogUrl
                    yield Request(url=parse.urljoin(response.url, subCatalogUrl),
                                  meta=meta,
                                  callback=self.parsePage)



