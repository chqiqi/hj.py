# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
pymysql.install_as_MySQLdb()

class HjPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='1234.abcd', database='hj', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        print(item)
        insert_sql = """
                        INSERT INTO t_chemical_list
                            (name, enname, casno, formula, weight, dangerInfoTxt, dangerInfoUrl, catalogTitle)
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                    """
        self.cursor.execute(insert_sql, (
            item.get("name", ""),
            item.get("enname", ""),
            item.get("casno", ""),
            item.get("formula", ""),
            item["weight"],
            item.get("dangerInfoTxt", ""),
            item.get("dangerInfoUrl", ""),
            item.get("catalogTitle", "")
        ))
        self.conn.commit()
        return item
