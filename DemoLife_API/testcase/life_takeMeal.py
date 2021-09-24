# _*_ coding:utf-8 _*_

import configparser
import os
import sys

import jsonpath
import requests
import threading
from DemoLife_API.lib.log import Log
from DemoLife_API.lib.login_PWD import Login_PWD
from DemoLife_API.lib.login_PW import Login_PW
from DemoLife_API.config import setting

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
log = Log().getLog()

cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='UTF-8')


class TakeMeal(threading.Thread):
    """取餐扫码"""

    def __init__(self, login_phone, login_PATH, user_pwd=None):
        threading.Thread.__init__(self)
        self.s = requests.session()
        self.login_phone = login_phone
        self.headers = eval(cf.get("headers", "HEADERS-SM"))

        self.platform = 'LIFE_DELIVERY'
        if user_pwd:
            self.token, self.userName, self.id = Login_PWD(login_phone=self.login_phone, user_pwd=user_pwd, login_PATH=login_PATH, platform=self.platform).login('token',
                                                                                                                                                                 'userName', 'id')
        else:
            self.token, self.userName, self.id = Login_PW(self.login_phone, login_PATH, platform=self.platform).login('token', 'userName', 'id')
        self.LIFE_APP = cf.get(login_PATH, "lifeapp")
        self.takeMeal_url = self.LIFE_APP + "/app/delivery/oms/order/takeMeal"
        self.order_data = self._getOrder()

    def _getOrder(self):
        order_list = {}
        shopGroupList_url = self.LIFE_APP + "/app/delivery/oms/order/shopGroupList"
        scanTakeList_url = self.LIFE_APP + "/app/delivery/oms/order/scanTakeList"
        shopGroupList_data = {
            "offset": "0",
            "limit": "100",
            "deliveryDetailStatus": "40",
            "id": self.id,
            "token": self.token,
            "platform": self.platform
        }
        try:
            response_shopGroupList = self.s.post(url=shopGroupList_url, data=shopGroupList_data, headers=self.headers).json()
            log.info("返回待取餐店铺内容--->{0}".format(response_shopGroupList))
            if all([response_shopGroupList["statusCode"] == 0, response_shopGroupList["total"] != 0]):
                _shopIds = jsonpath.jsonpath(response_shopGroupList, "$..shopId")
                for shopId in _shopIds:
                    shopGroupList_data["shopId"] = shopId
                    log.info("shopId--->{0}".format(shopId))
                    response_scanTakeList = self.s.post(url=scanTakeList_url, data=shopGroupList_data, headers=self.headers).json()
                    log.info("返回待取餐内容--->{0}".format(response_scanTakeList))
                    if response_scanTakeList["statusCode"] == 0:
                        _orderNo = jsonpath.jsonpath(response_scanTakeList, "$..orderNo")
                        _detailStatus = jsonpath.jsonpath(response_scanTakeList, "$..deliveryDetailStatus")
                        _order = dict(zip(_orderNo, _detailStatus))
                        order_list = dict(order_list, **_order)
                    else:
                        log.info("返回待取餐订单失败--->{0}".format(response_scanTakeList["message"]))
            else:
                log.info("该取餐员_{0}（登录手机号_{1}），没有需要待取餐的数据".format(self.userName, self.login_phone))
        except Exception as e:
            log.info("查询出错：".format(e))
        log.info("过滤已取餐的订单")
        if order_list:
            # for keys, values in order_list.items():
            #     if values == 50:
            #         del_keys.append(keys)
            # del_keys = [keys for keys, values in order_list.items() if values == 50]
            for key in [keys for keys, values in order_list.items() if values == 50]:
                del order_list[key]

        log.info("返回的待取餐订单--->{0}".format(order_list))
        return order_list

    def run(self):
        log.info("取餐员_{1}，待取餐数量--->{0}".format(len(self.order_data), self.userName))
        if self.order_data:
            for order in self.order_data.keys():
                try:
                    takeMeal_data = {
                        "orderNo": order,
                        "id": self.id,
                        "token": self.token,
                        "testAccount": "1",
                        "platform": self.platform,
                    }
                    response_mealout = self.s.post(url=self.takeMeal_url, data=takeMeal_data, headers=self.headers).json()
                    log.info("取餐返回内容--->{0}".format(response_mealout))
                    if response_mealout["statusCode"] == 0:
                        log.info("订单：{0}，取餐成功--->取餐员:{1}（登录手机号：{2}）".format(order, self.userName, self.login_phone))
                    else:
                        log.info("订单号:{0}，取餐失败：{1}".format(order, response_mealout["message"]))

                except Exception as e:
                    log.info("取餐出错：".format(e))


def take_main(login_PATH='lsmart', user_pwd=None):
    Takes = cf.get("user", "Meal").split(",")
    threads = []
    for phone in Takes:
        threads.append(TakeMeal(login_phone=phone, login_PATH=login_PATH, user_pwd=user_pwd))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    take_main(login_PATH='lsmart')
    # TakeMeal(login_phone=18866674051).run()
