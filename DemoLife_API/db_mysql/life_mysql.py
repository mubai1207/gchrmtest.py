# _*_ coding:utf-8 _*_
"""
本地生活-数据库
"""

import os
import sys
import pymysql
import configparser
from DemoHealthCloud.config import setting
from DemoHealthCloud.lib.log import Log

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# --------- 读取config.ini配置文件 ---------------
cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='UTF-8')

host = cf.get("mysqlconf", "host")
port = cf.get("mysqlconf", "port")
user = cf.get("mysqlconf", "user")
password = cf.get("mysqlconf", "password")
db = cf.get("mysqlconf", "db_name")
log = Log().getLog()


class DB:
    def __init__(self):
        try:
            # 打开数据库连接
            self.conn = pymysql.connect(
                host=host,
                user=user,
                password=password,
                db=db,
                charset='utf8mb4',
                # cursorclass=cursors.DictCursor  # 如果要返回字典(dict)表示的记录，如：[{'order_no': '2010281546121918510'}, {'order_no': '2010281546191919510'}]
            )
            log.info("数据库连接成功")
        except Exception as e:
            log.info("数据库连接失败--->{0}".format(e))
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def select(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)  # 使用execute()执行SQL语句
        log.info("执行SQL语句--->{0}".format(sql))
        sql_data = cur.fetchall()  # 使用fetchall()方法获取查询结果 (接收全部的返回结果)
        log.info("数据库查询内容--->{0}".format(sql_data))

        return sql_data

    def close(self):
        log.info("关闭数据库")
        self.conn.close()


if __name__ == '__main__':
    db = DB()
    data = db.select("select order_no from oms_order where order_status=30")
    # print(data)
