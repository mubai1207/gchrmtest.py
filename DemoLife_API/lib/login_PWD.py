# _*_ coding:utf-8 _*_
import base64
import os
import re
import sys
import configparser
import hashlib

import jsonpath
import requests
from DemoLife_API.lib.log import Log
from DemoLife_API.config import setting
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
log = Log().getLog()
cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='UTF-8')


class Login_PWD:
    """
    密码登录
    """

    def __init__(self, login_phone, user_pwd, login_PATH, school_code=None, platform='YUNMA_APP'):
        """
        :param login_phone: 登录手机号
        :param user_pwd: 登录密码
        :param login_PATH: 登录环境（lsmart/gray/pro）
        :param school_code: 学校code（易校园平台需要传，本地生活不传）
        :param platform: 登录平台（YUNMA_APP/LIFE_BUSINESS/LIFE_DELIVERY），本地生活、易校园通过此参数判断
        """
        self.s = requests
        self.login_phone = login_phone
        self.platform = platform
        self.userPwd = user_pwd
        self.school_code = school_code
        self.headers = eval(cf.get("headers", "HEADERS-SM"))

        log.info("登录环境--->{0}".format(login_PATH))
        log.info("登录平台--->{0}".format(self.platform))
        self.COMPUS = cf.get(login_PATH, "compus")
        self.LIFE_APP = cf.get(login_PATH, "lifeapp")
        self.LIFE = cf.get(login_PATH, "life")
        self.AUTH = cf.get(login_PATH, "auth")
        self.data_getPublicKey = {
            "mobilePhone": self.login_phone,
            "testAccount": "1",
            "platform": self.platform,
        }

    def login(self, *args):
        """
        :param args: 需要返回的值
        :return: 返回内容
        """
        data = []
        if self.platform == 'YUNMA_APP':
            url_getPublicKey = self.COMPUS + "/login/getPublicKey"  # https://compusgray.xiaofubao.com/login/getPublicKey
            url_doLoginByPwd = self.COMPUS + '/login/doLoginByPwd'
            self.data_getPublicKey['schoolCode'] = self.school_code
        else:
            url_getPublicKey = self.LIFE_APP + "/app/login/getPublicKey"
            url_doLoginByPwd = self.LIFE_APP + '/app/login/doLoginByPwd'

        try:
            log.info("请求PublicKey信息--->{0}".format(self.data_getPublicKey))
            doLoginByPwd = self.s.post(url=url_getPublicKey, data=self.data_getPublicKey, headers=self.headers).json()
            log.info("返回PublicKey信息--->{0}".format(doLoginByPwd))
            if doLoginByPwd['statusCode'] == 0:
                publicKey = doLoginByPwd['data']['publicKey']
                log.info("返回的PublicKey--->{0}".format(publicKey))
                public_Key = "-----BEGIN RSA PUBLIC KEY-----\n" + publicKey + "\n-----END RSA PUBLIC KEY-----"

                log.info("md5加密输入的密码")
                md5_userPwd = hashlib.md5(self.userPwd.encode()).hexdigest()
                log.info("RSA加密登录密码")
                rsa_public_key = RSA.importKey(public_Key)
                cipher = Cipher.new(rsa_public_key)
                cipher_text = base64.b64encode(cipher.encrypt(md5_userPwd.encode(encoding='utf-8')))

                data_doLoginByPwd = {
                    "mobilePhone": self.login_phone,
                    "password": cipher_text,
                    "osType": "Android",
                    "platform": self.platform,
                }
                if self.platform == 'YUNMA_APP':
                    data_doLoginByPwd["schoolCode"] = self.school_code
                log.info("登录请求data--->{0}".format(data_doLoginByPwd))
                response_data = self.s.post(url=url_doLoginByPwd, data=data_doLoginByPwd, headers=self.headers).json()
                if response_data["statusCode"] == 0:
                    if response_data["data"]["schoolCode"] != self.school_code and self.platform == 'YUNMA_APP':
                        log.info("登录学校错了--->{0}，切换学校".format(response_data["data"]["schoolName"]))
                        user_id = jsonpath.jsonpath(response_data, "$..id")[0]
                        token = jsonpath.jsonpath(response_data, "$..token")[0]
                        response_data = self._changeSchool(user_id, token)
                    log.info("登录返回信息--->{0}".format(response_data))
                    for arg in args:
                        data.append(jsonpath.jsonpath(response_data, "$..%s" % (arg,))[0])
                    log.info("获取登录返回的内容--->{0}".format(data))
                    return data
                else:
                    log.error("登录出错--->{0}".format(response_data['message']))
                    return response_data['message']
            else:
                log.error("PublicKey获取出错--->{0}".format(doLoginByPwd['message']))
                return doLoginByPwd['message']
        except Exception as e:
            log.error("出错信息--->{0}".format(e))

    def _changeSchool(self, user_id, token):
        change_url = self.COMPUS + "/compus/user/changeSchool"
        change_data = {
            "schoolCode": self.school_code,
            "id": user_id,
            "token": token,
            "platform": self.platform,
        }
        response_data = self.s.post(url=change_url, data=change_data, headers=self.headers).json()
        if response_data['statusCode'] == 0:
            log.info("切换学校成功--->{0}".format(jsonpath.jsonpath(response_data, "$..schoolName")))
            return response_data
        else:
            log.info("切换学校失败--->{0}".format(response_data["message"]))
            return None

    def login_customer(self):
        """
        消费端登录
        :return: 返回cookie信息
        """
        getCode_url = self.AUTH + "/authoriz/getCodeV2"
        try:
            unionid = self.login('id')[0]
            log.info("unionid--->{0}".format(unionid))
            getCode_data = {
                "bindSkip": "1",
                "authType": "2",
                "appid": "1808311525396021",
                "callbackUrl": self.LIFE + "/#/home?operatorId=1&unionid=" + str(unionid) + "&schoolCode=" + self.school_code,
                "unionid": unionid,
                "schoolCode": self.school_code,
            }
            log.info("获取code请求data--->{0}".format(getCode_data))
            response_getCode = requests.get(url=getCode_url, params=getCode_data, headers=self.headers).text
            code = re.findall(r'\"([a-zA-Z0-9]{17,})\"', response_getCode)[0]
            log.info("code--->{0}".format(code))
            url_getUser4Authorize = self.LIFE + "/api/ums/login/getUser4Authorize"
            data_getUser4Authorize = {
                "code": code,
                "userId": "",
                "schoolCode": "",
            }
            log.info("认证请求data信息--->{0}".format(data_getUser4Authorize))
            response_getUser = requests.post(url=url_getUser4Authorize, data=data_getUser4Authorize, headers=self.headers)
            log.info("认证返回信息--->{0}".format(response_getUser.json()))
            cookies = requests.utils.dict_from_cookiejar(response_getUser.cookies)
            log.info("cookies信息--->{0}".format(cookies))
            cookie = "shiroJID=%s" % cookies["shiroJID"]
            log.info("返回shiroJID信息--->{0}".format(cookie))
            return cookie
        except Exception as e:
            log.error("出错信息--->{0}".format(e))


if __name__ == '__main__':
    print(Login_PWD(login_phone='18866674052', user_pwd='a111111', login_PATH='lsmart', school_code='12061', platform='YUNMA_APP').login('id', 'deviceId', 'token'))
    # print(Login_PWD(login_phone='18866674052', user_pwd='a111112', login_PATH='lsmart', platform='LIFE_BUSINESS').login('id', 'bmsUserId', 'shopId', 'token'))
