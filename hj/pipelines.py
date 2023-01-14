# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline
from itemadapter import ItemAdapter
import pymysql
pymysql.install_as_MySQLdb()


class HjImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "formulaImgUrl" in item:
            image_file_path = []
            for ok, value in results:
                image_file_path.append(value["path"])
            if len(image_file_path)>0:
                item["formulaImgAddr"] = image_file_path[0]
        return item

class HjPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='1234.abcd', database='hj', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        print(item)
        insert_sql = """
                        INSERT INTO t_chemical_list
                            (name, enname, casno, formula, weight, dangerInfoTxt, dangerInfoUrl, catalogTitle,formulaImgAddr)
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            on duplicate key update 
                            enname=%s, casno=%s, formula=%s, weight=%s, dangerInfoTxt=%s, dangerInfoUrl=%s, catalogTitle=%s,formulaImgAddr=%s
                    """
        self.cursor.execute(insert_sql, (
            item.get("name", ""),
            item.get("enname", ""),
            item.get("casno", ""),
            item.get("formula", ""),
            item.get("weight", "0"),
            item.get("dangerInfoTxt", ""),
            item.get("dangerInfoUrl", ""),
            item.get("catalogTitle", ""),
            item.get("formulaImgAddr", ""),
            item.get("enname", ""),
            item.get("casno", ""),
            item.get("formula", ""),
            item.get("weight", "0"),
            item.get("dangerInfoTxt", ""),
            item.get("dangerInfoUrl", ""),
            item.get("catalogTitle", ""),
            item.get("formulaImgAddr", "")
        ))
        self.conn.commit()
        return item
