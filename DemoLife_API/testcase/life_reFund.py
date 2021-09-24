# _*_ coding:utf-8 _*_

import configparser
import os
import sys
import threading

import jsonpath
import requests
from DemoLife_API.lib.log import Log
from DemoLife_API.lib.login_PW import Login_PW
from DemoLife_API.config import setting

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='UTF-8')
log = Log().getLog()


class ReFund(threading.Thread):
    """确认退款"""

    def __init__(self, login_phone, login_PATH, num):
        """
        :param login_phone: 登录手机号
        :param login_PATH: 登录环境（默认lsmart，可选择lsmart/gray/pro）
        :param num: 退款数量（默认全部，填写退款数量）
        """
        threading.Thread.__init__(self)
        self.s = requests
        self.login_phone = login_phone
        self.num = str(num)
        self.headers = eval(cf.get("headers", "HEADERS-SM"))

        self.platform = 'LIFE_BUSINESS'
        self.LIFE_APP = cf.get(login_PATH, "lifeapp")
        self.token, self.shopId, self.id = Login_PW(self.login_phone, login_PATH, platform=self.platform).login('token', 'shopId', 'id')
        self.refund_url = self.LIFE_APP + "/app/business/oms/order/refund"
        self.shop_name = self._getShopName()
        self.order_data = self._getOrder()

    def _getShopName(self):
        shopDetail_url = self.LIFE_APP + "/app/business/bms/shop/shopDetail"
        shopDetail_data = {
            "id": self.id,
            "token": self.token,
            "platform": self.platform
        }
        try:
            response_shopDetail = self.s.post(url=shopDetail_url, data=shopDetail_data, headers=self.headers).json()
            if response_shopDetail["statusCode"] == 0:
                shopName = jsonpath.jsonpath(response_shopDetail, "$..shopName")[0]
            else:
                log.info("没有获取到店铺名称--->{0}".format(response_shopDetail["message"]))
        except Exception as e:
            log.error("出错信息--->{0}".format(e))
        log.info("返回的店铺名称--->{0}".format(shopName))
        return shopName

    def _getOrder(self):
        order_list = []
        orderList_url = self.LIFE_APP + "/app/business/oms/order/orderList"

        orderList_data = {
            "offset": "0",
            "limit": "1000",
            "queryType": "5",
            "id": self.id,
            "token": self.token,
            "platform": self.platform
        }
        try:
            response_orderList = self.s.post(url=orderList_url, data=orderList_data, headers=self.headers).json()
            log.info("返回店铺待退款内容--->{0}".format(response_orderList))
            if response_orderList["statusCode"] == 0 and response_orderList["total"] != 0:
                _orders = jsonpath.jsonpath(response_orderList, "$..orderNo")
                order_list = list(set(_orders))
            else:
                log.info("该店铺_{0}，没有待退款的订单".format(self.shop_name))
        except Exception as e:
            log.error("出错信息--->{0}".format(e))
        order_list.sort()
        log.info("返回的待退款订单--->{0}".format(len(order_list)))
        return order_list

    def run(self):
        if self.order_data:
            try:
                if self.num.isdigit():
                    self.order_data = self.order_data[0:int(self.num)]
                log.info("店铺_{0}_待退款数量--->{1}".format(self.shop_name, len(self.order_data)))
                if self.order_data:
                    for order in self.order_data:
                        refund_data = {
                            "id": self.id,
                            "orderId": order,
                            "refundStatus": 20,
                            "token": self.token,
                            "platform": self.platform,
                        }
                        response_refund = self.s.post(url=self.refund_url, data=refund_data, headers=self.headers).json()
                        log.info("确定退款返回内容--->{0}".format(response_refund))
                        if response_refund["statusCode"] == 0:
                            log.info("店铺_{0}，订单：{1}_确定退款成功!".format(self.shop_name, order))
                        else:
                            log.info("店铺_{0}，订单：{1}_退款失败--->{2}".format(self.shop_name, order, response_refund["message"]))
                else:
                    log.info("店铺_{0}（登录手机号{1}），没有需要退款的数据".format(self.shop_name, self.login_phone))
            except Exception as e:
                log.info("店铺退款出错了--->{0}".format(e))


def business_main(num=None, login_PATH='lsmart'):
    Business = cf.get("user", "Business").split(",")
    threads = []
    for phone in Business:
        threads.append(ReFund(login_phone=phone, login_PATH=login_PATH, num=num))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    # business_main()
    ReFund(login_phone=18866666660, login_PATH='lsmart', num=None).run()
