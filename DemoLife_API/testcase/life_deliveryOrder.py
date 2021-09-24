# _*_ coding:utf-8 _*_

import configparser
import os
import sys

import jsonpath
import requests

from DemoLife_API.lib.log import Log
from DemoLife_API.lib.login_PWD import Login_PWD
from DemoLife_API.lib.login_PW import Login_PW
from DemoLife_API.config import setting

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

log = Log().getLog()
cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='UTF-8')
Admin = cf.get("user", "Admin").split(",")


class deliveryOrderList:
    def __init__(self, login_phone, login_PATH, user_pwd=None):
        """
        :param login_phone: 登录手机号
        :param login_PATH: 登录环境（默认lsmart，可选择lsmart/gray/pro）
        """
        self.s = requests
        self.login_phone = login_phone
        self.headers = eval(cf.get("headers", "HEADERS-SM"))

        self.platform = 'LIFE_DELIVERY'

        if user_pwd:
            self.token, self.id = Login_PWD(login_phone=self.login_phone, user_pwd=user_pwd, login_PATH=login_PATH, platform=self.platform).login('token', 'id')
        else:
            self.token, self.id = Login_PW(login_phone=self.login_phone, login_PATH=login_PATH, platform=self.platform).login('token', 'id')
        self.LIFE_APP = cf.get(login_PATH, "lifeapp")

    def _getOrder(self, statue=60):
        order_list = []
        deliveryOrder_url = self.LIFE_APP + "/app/delivery/oms/statistics/deliveryOrderListData"
        deliveryOrder_data = {
            "offset": "0",
            "limit": "10000",
            "deliveryDetailStatus": statue,
            "id": self.id,
            "token": self.token,
            "platform": self.platform
        }
        if statue == 60:
            try:
                response_deliveryOrder = self.s.post(url=deliveryOrder_url, data=deliveryOrder_data, headers=self.headers).json()
                log.info("返回待核验内容--->{0}".format(response_deliveryOrder))
                if response_deliveryOrder["statusCode"] == 0 and response_deliveryOrder["total"] != 0:
                    _orders = jsonpath.jsonpath(response_deliveryOrder, "$..orderNo")
                    order_list = _orders
                else:
                    log.info("没有待核验的订单")
            except Exception as e:
                log.error("出错信息--->{0}".format(e))
            log.info("返回的待核验的订单--->{0}".format(len(order_list)))
        else:
            try:
                response_deliveryOrder = self.s.post(url=deliveryOrder_url, data=deliveryOrder_data, headers=self.headers).json()
                log.info("返回待送达内容--->{0}".format(response_deliveryOrder))
                if response_deliveryOrder["statusCode"] == 0 and response_deliveryOrder["total"] != 0:
                    _orders = jsonpath.jsonpath(response_deliveryOrder, "$..orderNo")
                    order_list = _orders
                else:
                    log.info("没有待送达的订单")
            except Exception as e:
                log.error("出错信息--->{0}".format(e))
            log.info("返回的待送达的订单--->{0}".format(len(order_list)))
        return order_list


def OrderList_main(statue, login_PATH='lsmart', user_pwd=None):
    return deliveryOrderList(login_phone=Admin[0], login_PATH=login_PATH, user_pwd=user_pwd)._getOrder(statue=statue)


if __name__ == '__main__':
    OrderList_main(login_PATH='gray', user_pwd='a111111', statue=60)
