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
    titleMapping = {"中文名称:":"name","英文名称:":"enname","CAS号:":"casno","分子式:":"formula","分子量:":"weight","毒害物质数据":"dangerInfoTxt"}

    def parse(self, response):
        catalog1List = response.css("a.T1")
        for catalog1 in catalog1List:
            catalog1Url = catalog1.css("a::attr(href)").extract_first("")
            catalog1Title = catalog1.css("a::text").extract_first("")
            print(catalog1Url)
            yield Request(url=parse.urljoin(response.url, catalog1Url), meta={"catalogTitle": catalog1Title,"currUrl":catalog1Url},
                          callback=self.parsePage)

    def parsePage(self, response):
        time.sleep(2)
        meta = response.meta
        catalogTitle = meta.get("catalogTitle","")
        currUrl = meta.get("currUrl", "")
        if currUrl.startswith( '/ProductChemicalProperties' ):
            needHandle = False
            item = HjItem()
            item['catalogTitle'] = catalogTitle
            baseInfoTrs = response.css("tr[class^='ProdSupplierGN_ProductA']")
            for baseInfo in baseInfoTrs:
                baseInfoTds = baseInfo.css("td")
                if len(baseInfoTds) == 2:
                    fieldName = baseInfoTds[0].css("td::text").extract_first("")
                    fieldValue = baseInfoTds[1].css("td a::text").extract_first("")
                    if fieldValue == "":
                        fieldValue = baseInfoTds[1].css("td::text").extract_first("")
                    if self.titleMapping.__contains__(fieldName):
                        mapField = self.titleMapping[fieldName]
                        item[mapField] = fieldValue
                        needHandle = True
                        #单独取一下链接
                        if mapField == 'dangerInfoTxt':
                            item['dangerInfoUrl'] = baseInfoTds[1].css("td a::attr(href)").extract_first("")
            if needHandle:
                yield item
        else:
            subCatalogs = response.xpath("//div[@id='tabsort']//a")
            if len(subCatalogs) == 1:
                detailUrls = response.xpath("//dl/dd/em/a")
                for detailUrl in detailUrls:
                    url = detailUrl.css("a::attr(href)").extract_first("")
                    txt = detailUrl.css("a::text").extract_first("")
                    if url.startswith( '/ProductChemicalProperties' ):
                        meta['currUrl'] = url
                        meta['catalogTitle'] = "{}/{}".format(catalogTitle,txt)
                        yield Request(url=parse.urljoin(response.url, url),
                                      meta=meta,
                                      callback=self.parsePage)
            else:
                for subCatalog in subCatalogs:
                    subCatalogUrl = subCatalog.css("a::attr(href)").extract_first("")
                    txt = subCatalog.css("a::text").extract_first("")
                    meta['currUrl'] = subCatalogUrl
                    meta['catalogTitle'] = "{}/{}".format(catalogTitle, txt)
                    yield Request(url=parse.urljoin(response.url, subCatalogUrl),
                                  meta=meta,
                                  callback=self.parsePage)



