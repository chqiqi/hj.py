import requests
from scrapy.selector import Selector
import pymysql
pymysql.install_as_MySQLdb()
import time

conn = pymysql.connect(host='127.0.0.1', user='root', password='1234.abcd', database='hj', charset="utf8", use_unicode=True)
cursor = conn.cursor()


def crawl_ips():
    #爬取西刺的免费ip代理
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    for i in range(1,4967):
        re = requests.get("https://www.kuaidaili.com/free/inha/{0}/".format(i), headers=headers)
        time.sleep(2)
        selector = Selector(text=re.text)
        all_trs = selector.css("#list table tbody tr")

        ip_list = []
        for tr in all_trs[1:]:
            all_texts = tr.css("td::text").extract()
            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[3]
            speed = all_texts[5]

            ip_list.append((ip, port, proxy_type, speed))

        for ip_info in ip_list:
            cursor.execute(
                "insert ignore into t_proxy_ip(ip, port, speed, proxy_type) VALUES('{0}', '{1}', '{2}', '{3}')".format(
                    ip_info[0], ip_info[1], ip_info[3], ip_info[2]
                )
            )

            conn.commit()


class GetIP(object):
    def delete_ip(self, ip):
        #从数据库中删除无效的ip
        delete_sql = """
            delete from t_proxy_ip where ip='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        #判断ip是否可用
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http":proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print ("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print ("effective ip")
                return True
            else:
                print  ("invalid ip and port")
                self.delete_ip(ip)
                return False


    def get_random_ip(self):
        #从数据库中随机获取一个可用的ip
        random_sql = """
              SELECT ip, port FROM t_proxy_ip
            ORDER BY RAND()
            LIMIT 1
            """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()



#print (crawl_ips())
