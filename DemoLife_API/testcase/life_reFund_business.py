# _*_ coding:utf-8 _*_

import configparser
import os
import sys
import time
import threading
import jsonpath
import requests
from DemoLife_API.lib.log import Log
from DemoLife_API.lib.login_PW import Login_PW
from DemoLife_API.config import setting

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
log = Log().getLog()

cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='UTF-8')


class RefundOder:
    """提交退款申请"""

    def __init__(self, login_phone, login_PATH, school_code):
        """
        :param login_phone: 登录手机号
        :param login_PATH: 登录环境（默认lsmart，可选择lsmart/gray/pro）
        :param num: 下单数量（默认1）
        """
        # threading.Thread.__init__(self)
        self.s = requests
        self.login_phone = login_phone
        self.platform = 'YUNMA_APP'
        self.school_code = school_code
        self.headers = eval(cf.get("headers", "HEADERS-SM"))
        self.login = Login_PW(self.login_phone, login_PATH, platform=self.platform, school_code=self.school_code)

        self.headers["Cookie"] = self.login.login_customer()
        self.LIFE = cf.get(login_PATH, "life")
        self.orderList_url = self.LIFE + "/api/oms/order/orderList"
        self.applyRefund_url = self.LIFE + "/api/oms/order/applyRefund"

    def run(self):
        try:
            log.info("账号_{0}，可取消订单数量--->{1}".format(self.login_phone, len(self._getOrder())))
            for order in self._getOrder():  # number代o表创建订单的数量
                applyRefund_data = {
                    "refundImgs": "",
                    "refundRemarks": "",
                    "refundType": 2,
                    "orderId": order
                }
                response_applyRefund = self.s.post(url=self.applyRefund_url, data=applyRefund_data, headers=self.headers).json()
                if response_applyRefund["statusCode"] == 0:
                    log.info("订单：{0}，取消成功--->账号_{1}".format(order, self.login_phone))
                else:
                    log.info("订单：{0}，取消失败：--->{1}".format(order, response_applyRefund["message"]))
        except Exception as e:
            log.error('出错信息--->{0}'.format(e))

    def _getOrder(self):
        order_list = []
        orderList_data = {
            "queryType": 1,
            "currentPage": 1
        }
        response_orderList = self.s.post(url=self.orderList_url, data=orderList_data, headers=self.headers).json()
        log.info("订单列表返回内容--->{0}".format(response_orderList))
        if response_orderList["statusCode"] == 0 and response_orderList["total"] != 0:
            dic = dict(zip(jsonpath.jsonpath(response_orderList, "$..orderNo"), jsonpath.jsonpath(response_orderList, "$..orderStatus")))
            # for key, value in dic.items():
            #     if value == 20:
            #         order_list.append(key)

            order_list = [key for key, value in dic.items() if value == 20]
        else:
            log.info("账号_{0}，订单列表获取失败--->{1}".format(self.login_phone, response_orderList["message"]))
        log.info("账号_{0}，返回订单列表--->{1}".format(self.login_phone, order_list))
        return order_list


def Refund_main(login_PATH='lsmart', school_code="12061"):
    LoginPhone = cf.get("user", "LoginPhone").split(",")
    threads = []
    for phone in LoginPhone:
        t = threading.Thread(target=RefundOder(login_phone=phone, login_PATH=login_PATH, school_code=school_code).run())
        t.start()
        time.sleep(0.5)
    for t in threads:
        t.join()


if __name__ == '__main__':
    Refund_main()
    # MakerOder(login_phone=18866674052, num=10, login_PATH='lsmart', school_code='12061').run()
