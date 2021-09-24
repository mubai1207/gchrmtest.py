# _*_ coding:utf-8 _*_

import configparser
import os
import sys
import threading
import time

import requests
from queue import Queue
from DemoLife_API.lib.log import Log
from DemoLife_API.lib.login_PWD import Login_PWD
from DemoLife_API.lib.login_PW import Login_PW
from DemoLife_API.config import setting
from DemoLife_API.testcase.life_deliveryOrder import deliveryOrderList

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

log = Log().getLog()
cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='UTF-8')


class CheckAndSorting(threading.Thread):
    """扫码核验"""

    def __init__(self, login_phone, q, login_PATH, user_pwd):
        """
        :param login_phone: 登录手机号
        :param login_PATH: 登录环境（默认lsmart，可选择lsmart/gray/pro）
        """
        threading.Thread.__init__(self)
        self._queue = q
        self.s = requests
        self.login_phone = login_phone
        self.headers = eval(cf.get("headers", "HEADERS-SM"))

        self.platform = 'LIFE_DELIVERY'

        if user_pwd:
            self.token, self.userName, self.id = Login_PWD(login_phone=self.login_phone, user_pwd=user_pwd, login_PATH=login_PATH, platform=self.platform).login('token',
                                                                                                                                                                 'userName', 'id')
        else:
            self.token, self.userName, self.id = Login_PW(self.login_phone, login_PATH, platform=self.platform).login('token', 'userName', 'id')

        self.LIFE_APP = cf.get(login_PATH, "lifeapp")
        self.doCheckAndSorting_url = self.LIFE_APP + "/app/delivery/oms/order/doCheckAndSorting"

    def run(self):

        try:
            log.info("待核验订单数量--->{0}".format(self._queue.qsize()))
            while not self._queue.empty():
                order = self._queue.get()

                doCheckAndSorting_data = {
                    "orderNo": order,
                    "id": self.id,
                    "token": self.token,
                    "testAccount": "1",
                    "platform": self.platform,
                }
                log.info("扫码核验请求data--->{0}".format(doCheckAndSorting_data))
                response_doCheckAndSorting = self.s.post(url=self.doCheckAndSorting_url, data=doCheckAndSorting_data, headers=self.headers).json()
                log.info("核验返回内容--->{0}".format(response_doCheckAndSorting))
                if response_doCheckAndSorting["statusCode"] == 0:
                    log.info("订单号：{0}，核验成功--->核检员：{1}（登录手机号：{2}）".format(order, self.userName, self.login_phone))
                else:
                    log.info("订单号：{0}，核验失败--->{1}".format(order, response_doCheckAndSorting["message"]))
            else:
                log.info("没有需要核验的数据")
        except Exception as e:
            log.info("核验出错--->{0}".format(e))


def check_main(login_PATH='lsmart', user_pwd=None):
    Checks = cf.get("user", "Check").split(",")
    Admin = cf.get("user", "Admin").split(",")
    q = Queue()
    threads = []

    order_data = deliveryOrderList(login_phone=Admin[0], login_PATH=login_PATH, user_pwd=user_pwd)._getOrder(statue=60)
    for order in order_data:
        q.put(order)
    time.sleep(1)
    for phone in Checks:
        threads.append(CheckAndSorting(login_phone=phone, q=q, login_PATH=login_PATH, user_pwd=user_pwd))

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    check_main(login_PATH='gray', user_pwd='a111111')
