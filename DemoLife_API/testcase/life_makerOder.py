# _*_ coding:utf-8 _*_

import configparser
import os
import re
import sys
import time
import random
import threading
import jsonpath
import requests
from DemoLife_API.lib.log import Log
from DemoLife_API.lib.login_PW import Login_PW
from DemoLife_API.lib.login_PWD import Login_PWD
from DemoLife_API.lib.bind_Card import BindCard
from DemoLife_API.config import setting

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
log = Log().getLog()

cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='UTF-8')


class MakerOder:
    """本地生活-下单"""

    def __init__(self, login_phone, num, login_PATH, school_code, user_pwd):
        """
        :param login_phone: 登录手机号
        :param login_PATH: 登录环境（默认lsmart，可选择lsmart/gray/pro）
        :param num: 下单数量（默认1）
        """
        # threading.Thread.__init__(self)

        self.s = requests
        self.number = num
        self.login_phone = login_phone
        self.platform = 'YUNMA_APP'
        self.school_code = school_code
        self.headers = eval(cf.get("headers", "HEADERS-SM"))
        if user_pwd:
            self.login = Login_PWD(login_phone=self.login_phone, user_pwd=user_pwd, login_PATH=login_PATH, platform=self.platform, school_code=self.school_code)
        else:
            self.login = Login_PW(self.login_phone, login_PATH, platform=self.platform, school_code=self.school_code)
        self.headers["Cookie"] = self.login.login_customer()

        self.COMPUS = cf.get(login_PATH, "compus")
        self.LIFE = cf.get(login_PATH, "life")
        self.AUTH = cf.get(login_PATH, "auth")
        self.PAY = cf.get(login_PATH, "PAY")

        self.login_url = self.COMPUS + "/login/doLoginByVerificationCode"  # 登录
        self.createOrder_url = self.LIFE + "/api/oms/order/createOrder"  # 创建订单
        self.token_url = self.LIFE + "/api/common/token/get"  # 获取token
        self.choose_url = self.PAY + "/pay/unified/choose.shtml"  # 预下单
        self.pay_url = self.PAY + "/pay/unified/doCardPay"  # 支付
        self.cashier_url = self.PAY + "/pay/unified/toCashier.shtml"
        self.address_url = self.LIFE + "/api/cms/consumer/address/list"
        self.goods_id = [
            # {"shopId": "2011021028310017500", "orderGoodsList": [{"goodsId": "2011031305590184500", "goodsNumber": 1, "specsId": "2103346284049301505"}]},
            {"shopId": "2011021028310017500", "orderGoodsList": [{"goodsId": "2011021448230173500", "goodsNumber": 1, "specsId": "2103346284286279681"}]},
            {"shopId": "2011021028310017500", "orderGoodsList": [{"goodsId": "2011031305590184500", "goodsNumber": 1, "specsId": "2103346284049301505"}]}
            # {"shopId": "2011021426080021500", "orderGoodsList": [{"goodsId": "2011021615580179500", "goodsNumber": 1, "specsId": "2011021615580303500"}]}
            # {"shopId": "2011021426080021500", "orderGoodsList": [{"goodsId": "2011021615580179500", "goodsNumber": 1, "specsId": "2011021615580303500"}]}
        ]
        self.address_id = {"addressId": self._getAddress(), "expectDate": time.strftime('%Y-%m-%d'), "remarks": "", "coverType": "", "expectArrivedTime": "",
                           "shopTableName": "", "shopTableId": "","phone": self.login_phone}
        self.id, self.token = self.login.login('id', 'token')
        BindCard(self.s, self.id, self.token, login_PATH, self.school_code, self.platform).bindCard()

    def run(self):
        try:
            log.info("下单数量--->{0}".format(int(self.number)))
            for num in range(0, int(self.number)):  # number代o表创建订单的数量
                self.address_id["orderType"] = random.randint(1, 1)
                param = dict(random.choice(self.goods_id), **self.address_id)
                createOrder = {
                    "param": "%s" % param,
                    "submitToken": "%s" % self._get_OrderToken()
                }

                log.info("账号_{1}，下单data--->{0}".format(createOrder, self.login_phone))
                response_createOrder = self.s.post(url=self.createOrder_url, data=createOrder, headers=self.headers).json()  # 创建订单
                log.info("创建订单返回内容--->{0}".format(response_createOrder))
                if response_createOrder["statusCode"] == 0:
                    cashierAddress = response_createOrder["data"]["cashierAddress"]
                    pay_order = cashierAddress.split("=")[1]
                    log.info("No.{2}、订单：{1}，创建成功--->账号_{0}".format(self.login_phone, self._get_LifeOrder(pay_order), num + 1))
                    self._E_pay(pay_order, cashierAddress)
                else:
                    log.info("账号_{0}，订单创建失败：{1}".format(self.login_phone, response_createOrder["message"]))
        except Exception as e:
            log.error('出错信息--->{0}'.format(e))

    def _getAddress(self):
        try:
            response_address = self.s.post(url=self.address_url, data=None, headers=self.headers).json()  # 创建订单
            if response_address["statusCode"] == 0:
                get_address = jsonpath.jsonpath(response_address, "$..id")[0]
                log.info('获取的下单地址--->{0}'.format(get_address))
                return get_address
            else:
                log.error('获取下单地址，出错信息--->{0}'.format(response_address["message"]))
                return None
        except Exception as e:
            log.error('出错信息--->{0}'.format(e))

    def _get_LifeOrder(self, tran_no):
        try:
            data_Cashier = {"tran_no": tran_no}
            log.info('请求data_Cashier--->{0}'.format(data_Cashier))
            response_Cashier = self.s.get(url=self.cashier_url, params=data_Cashier, headers=self.headers).text
            LifeOrder = re.findall(r'-([0-9]{19,})<', response_Cashier)[0]
            log.info('获取的订单号--->{0}'.format(LifeOrder))
            return LifeOrder
        except Exception as e:
            log.error('出错信息--->{0}'.format(e))

    def _get_OrderToken(self):
        try:
            response_token = self.s.post(url=self.token_url, data=None, headers=self.headers).json()  # 创建订单
            if response_token["statusCode"] == 0:
                get_token = response_token["data"]
                log.info('获取的下单token--->{0}'.format(get_token))
                return get_token
            else:
                log.error('获取下单token出错信息--->{0}'.format(response_token["message"]))
                return None
        except Exception as e:
            log.error('出错信息--->{0}'.format(e))

    def _payBack(self, tran_no):
        order = self._get_LifeOrder(tran_no)
        url = "https://lifeapi.lsmart.wang/callback/order/payBack"
        data = {
            "cp_tran_no": order,
            "tran_state": 2,
            "pay_type": "CARDPAY",
            "pay_name": "一卡通支付"
        }

        response_pay = self.s.post(url=url, data=data, headers=self.headers)
        if response_pay.status_code == 200:
            log.info("订单%s支付成功" % order)
        else:
            log.info("账号_%s，订单支付失败：%s" % (self.login_phone, response_pay.status_code))

    def _C_pay(self, tran_no, payPageUrl=None):
        order = self._get_LifeOrder(tran_no)

        choose_data = {
            "tranNo": tran_no,
            "channelCode": "normal",
            "payType": "CARDPAY",  # EPAY
            "scene": 1,
            "payPageUrl": payPageUrl
        }

        pay_data = {
            "tranNo": tran_no,
            "password": "112233",
        }

        try:
            response_choose = self.s.post(url=self.choose_url, data=choose_data, headers=self.headers).json()  # 预下单
            log.info('一卡通支付预下单返回内容--->{0}'.format(response_choose))
            if response_choose["statusCode"] == 0:
                response_pay = self.s.post(url=self.pay_url, data=pay_data, headers=self.headers).json()  # 支付
                log.info('一卡通支付返回内容--->{0}'.format(response_choose))
                if response_pay["statusCode"] == 0:
                    log.info('订单：{0}，一卡通支付成功'.format(order))
                else:
                    log.info('订单：{0}，一卡通支付失败--->{1}'.format(order, response_pay["message"]))
            else:
                log.info('一卡通预下单失败--->{0}'.format(response_choose["message"]))
        except Exception as e:
            log.error('一卡通出错信息--->{0}'.format(e))

    def _E_pay(self, tran_no, payPageUrl=None):
        order = self._get_LifeOrder(tran_no)

        choose_data = {
            "tranNo": tran_no,
            "channelCode": "normal",
            "payType": "EPAY",  # EPAY
            "scene": 1,
            "payPageUrl": payPageUrl
        }
        self.E_pay_url = self.PAY + "/eacct/pay/doPay"
        # E_pay_url = "https://unifiedpay.lsmart.wang/eacct/pay/doPay"
        E_pay_data = {
            "tranNo": tran_no,
            "validCode": "112233",
        }

        try:
            response_choose = self.s.post(url=self.choose_url, data=choose_data, headers=self.headers).json()  # 预下单
            log.info('工行支付预下单返回内容--->{0}'.format(response_choose))
            if response_choose["statusCode"] == 0:
                response_pay = self.s.post(url=self.E_pay_url, data=E_pay_data, headers=self.headers).json()  # 支付
                log.info('工行支付返回内容--->{0}'.format(response_choose))
                if response_pay["statusCode"] == 0:
                    log.info('订单：{0}，工行支付成功'.format(order))
                else:
                    log.info('订单：{0}，工行支付失败--->{1}'.format(order, response_pay["message"]))
            else:
                log.info('工行预下单失败--->{0}'.format(response_choose["message"]))
        except Exception as e:
            log.error('工行出错信息--->{0}'.format(e))


def maker_main(num=1, login_PATH='pre', school_code="12061", user_pwd=None):
    LoginPhone = cf.get("user", "LoginPhone").split(",")
    log.info("登录手机号--->{0}".format(LoginPhone))
    threads = []
    for phone in LoginPhone:
        t = threading.Thread(target=MakerOder(login_phone=phone, num=num, login_PATH=login_PATH, school_code=school_code, user_pwd=user_pwd).run())
        t.start()
        time.sleep(0.5)

    for t in threads:
        t.join()


if __name__ == '__main__':
    maker_main(1)
    # MakerOder(login_phone=18866674052, num=10, login_PATH='lsmart', school_code='12061').run()
