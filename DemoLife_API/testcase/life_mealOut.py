# _*_ coding:utf-8 _*_

import configparser
import os
import sys
import threading

import jsonpath
import requests
from DemoLife_API.lib.log import Log
from DemoLife_API.lib.login_PW import Login_PW
from DemoLife_API.lib.login_PWD import Login_PWD
from DemoLife_API.config import setting

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='UTF-8')
log = Log().getLog()


class MealOut(threading.Thread):
    """出餐"""

    def __init__(self, login_phone, login_PATH, num, user_pwd):
        """
        :param login_phone: 登录手机号
        :param login_PATH: 登录环境（默认lsmart，可选择lsmart/gray/pro）
        :param num: 出餐数量（默认全部，填写出餐数量）
        """
        threading.Thread.__init__(self)
        self.s = requests
        self.login_phone = login_phone
        self.num = str(num)
        self.platform = 'LIFE_BUSINESS'
        self.headers = eval(cf.get("headers", "HEADERS-SM"))

        self.LIFE_APP = cf.get(login_PATH, "lifeapp")
        if user_pwd:
            self.token, self.shopId, self.id = Login_PWD(login_phone=self.login_phone, user_pwd=user_pwd, login_PATH=login_PATH, platform=self.platform).login('token', 'shopId',
                                                                                                                                                               'id')
        else:
            self.token, self.shopId, self.id = Login_PW(login_phone=self.login_phone, login_PATH=login_PATH, platform=self.platform).login('token', 'shopId', 'id')
        self.mealout_url = self.LIFE_APP + "/app/business/oms/order/mealout"
        self.shop_name = self._getShopName()
        self.order_data = self._getOrder()

    def _getShopName(self):
        global shopName
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
            "queryType": "3",
            "id": self.id,
            "token": self.token,
            "platform": self.platform
        }
        try:
            response_orderList = self.s.post(url=orderList_url, data=orderList_data, headers=self.headers).json()
            log.info("返回店铺待出餐内容--->{0}".format(response_orderList))
            if response_orderList["statusCode"] == 0 and response_orderList["total"] != 0:
                _orders = jsonpath.jsonpath(response_orderList, "$..orderNo")
                order_list = list(set(_orders))
            else:
                log.info("该店铺_{0}，没有待出餐的订单".format(self.shop_name))
        except Exception as e:
            log.error("出错信息--->{0}".format(e))
        order_list.sort()
        log.info("返回的待出餐订单--->{0}".format(len(order_list)))
        return order_list

    def run(self):
        if self.order_data:
            try:
                if self.num.isdigit():
                    self.order_data = self.order_data[0:int(self.num)]
                log.info("店铺_{0}_待出餐数量--->{1}".format(self.shop_name, len(self.order_data)))
                if self.order_data:
                    for order in self.order_data:
                        mealout_data = {
                            "id": self.id,
                            "orderId": order,
                            "token": self.token,
                            "platform": self.platform,
                        }
                        response_mealout = self.s.post(url=self.mealout_url, data=mealout_data, headers=self.headers).json()
                        log.info("确定出餐返回内容--->{0}".format(response_mealout))
                        if response_mealout["statusCode"] == 0:
                            log.info("店铺_{0}，订单：{1}_确定出餐成功!".format(self.shop_name, order))
                        else:
                            log.info("店铺_{0}，订单：{1}_出餐失败--->{2}".format(self.shop_name, order, response_mealout["message"]))
                else:
                    log.info("店铺_{0}（登录手机号{1}），没有需要出餐的数据".format(self.shop_name, self.login_phone))
            except Exception as e:
                log.info("店铺出餐出错了--->{0}".format(e))


def business_main(num=None, login_PATH='lsmart', user_pwd=None):
    Business = cf.get("user", "Business").split(",")
    threads = []
    for phone in Business:
        threads.append(MealOut(login_phone=phone, login_PATH=login_PATH, num=num, user_pwd=user_pwd))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    business_main()
# MealOut(login_phone=18758100002, login_PATH='lsmart', num='1').run()
