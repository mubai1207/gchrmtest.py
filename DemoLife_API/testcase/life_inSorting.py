# _*_ coding:utf-8 _*_

import configparser
import os
import sys
import time

import jsonpath
import requests
import threading
from DemoLife_API.lib.log import Log
from DemoLife_API.lib.login_PWD import Login_PWD
from DemoLife_API.lib.login_PW import Login_PW
from DemoLife_API.config import setting

log = Log().getLog()
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='UTF-8')


class SortingCenter(threading.Thread):
    """送达分拣"""

    def __init__(self, login_phone, login_PATH, user_pwd):
        super().__init__()
        self.s = requests
        self.login_phone = login_phone
        self.headers = eval(cf.get("headers", "HEADERS-SM"))

        self.platform = 'LIFE_DELIVERY'

        if user_pwd:
            self.token, self.id, self.userName = Login_PWD(login_phone=self.login_phone, user_pwd=user_pwd, login_PATH=login_PATH, platform=self.platform).login('token', 'id',
                                                                                                                                                                 'userName')
        else:
            self.token, self.id, self.userName = Login_PW(self.login_phone, login_PATH=login_PATH, platform=self.platform).login('token', 'id', 'userName')
        self.LIFE_APP = cf.get(login_PATH, "lifeapp")
        self.batchInSortingCenter_url = self.LIFE_APP + "/app/delivery/oms/order/inSortingCenter"
        self.order_data = self._getOrder()

    def _getOrder(self):
        order_list = []
        processList_url = self.LIFE_APP + "/app/delivery/oms/order/processListData"
        processList_data = {
            "offset": "0",
            "limit": "1000",
            "deliveryDetailStatus": "50",
            "id": self.id,
            "token": self.token,
            "platform": self.platform
        }
        try:
            response_processList = self.s.post(url=processList_url, data=processList_data, headers=self.headers).json()
            log.info("返回待分拣内容--->{0}".format(response_processList))
            if response_processList["statusCode"] == 0 and response_processList["total"] != 0:
                _orders = jsonpath.jsonpath(response_processList, "$..orderNo")
                order_list = _orders
            else:
                log.info("该取餐员_{0}，没有待分拣的订单".format(self.userName))
        except Exception as e:
            log.error("出错信息--->{0}".format(e))
        log.info("返回的待分拣的订单--->{0}".format(len(order_list)))
        return order_list

    def run(self):
        try:
            if self.order_data:
                log.info("取餐员_{1}，待送达分拣订单数量--->{0}".format(len(self.order_data), self.userName))
                for order in self.order_data:
                    batchInSortingCenter_data = {
                        "orderNo": order,
                        "id": self.id,
                        "token": self.token,
                        "testAccount": "1",
                        "platform": self.platform,
                    }
                    response_inSortingCenter = self.s.post(url=self.batchInSortingCenter_url, data=batchInSortingCenter_data, headers=self.headers).json()
                    log.info("送达分拣返回内容--->{0}".format(response_inSortingCenter))
                    if response_inSortingCenter["statusCode"] == 0:
                        log.info("订单号:{0}，送达分拣成功--->取餐员:{1}（登录手机号：{2}）".format(order, self.userName, self.login_phone))
                    else:
                        log.info("订单号:{0}，送达分拣失败--->{1}".format(order, response_inSortingCenter["message"]))
            else:
                log.info("该取餐员_{0}（登录手机号：{1}） 没有需要送达分拣的数据".format(self.userName, self.login_phone))
        except Exception as e:
            log.info("送达分拣出错：".format(e))


def sorting_main(login_PATH='lsmart', user_pwd=None):
    Takes = cf.get("user", "Meal").split(",")
    threads = []
    for phone in Takes:
        threads.append(SortingCenter(login_phone=phone, login_PATH=login_PATH, user_pwd=user_pwd))

    time.sleep(1)
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    sorting_main()
