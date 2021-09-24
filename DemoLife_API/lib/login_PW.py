# _*_ coding:utf-8 _*_
import configparser
import re
import sys
import os
import jsonpath
import requests
from DemoLife_API.lib.log import Log
from DemoLife_API.config import setting

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='UTF-8')
log = Log().getLog()


class Login_PW:
    """
    验证码登陆，仅支持测试环境使用
    """

    def __init__(self, login_phone, login_PATH, school_code=None, platform=None):
        """
        :param login_phone: 登录手机号
        :param platform: 登录平台（YUNMA_APP/LIFE_BUSINESS/LIFE_DELIVERY）
        """
        self.s = requests
        self.login_phone = login_phone
        self.platform = platform
        self.school_code = school_code
        self.headers = eval(cf.get("headers", "HEADERS-SM"))

        log.info("登录环境--->{0}".format(login_PATH))
        log.info("登录平台--->{0}".format(self.platform))
        if login_PATH not in ('lsmart', 'pre'):
            log.info("验证码登陆，仅支持测试环境使用")
            sys.exit(0)
        self.COMPUS = cf.get(login_PATH, "compus")
        self.LIFE_APP = cf.get(login_PATH, "lifeapp")
        self.LIFE = cf.get(login_PATH, "life")
        self.AUTH = cf.get(login_PATH, "auth")

        self.login_data = {
            "mobilePhone": self.login_phone,
            "verificationCode": "2",
            "osType": "Android",
            "platform": self.platform,
            # "testAccount": 1
        }

    def login(self, *args):
        """
        :param args: 需要返回的值
        :return: 返回内容
        """
        data = []
        if self.platform == 'YUNMA_APP':
            self.login_data["schoolCode"] = self.school_code
            login_url = self.COMPUS + "/login/doLoginByVerificationCode"
        else:
            login_url = self.LIFE_APP + '/app/login/doLoginByVerificationCode'
        log.info("登录url--->{0}".format(login_url))
        log.info("登录请求data--->{0}".format(self.login_data))

        try:
            response_data = self.s.post(url=login_url, data=self.login_data, headers=self.headers).json()

            if response_data["statusCode"] == 0:
                if response_data["data"]["schoolCode"] != self.school_code and self.platform == 'YUNMA_APP':
                    log.info("登录学校错了--->{0}，切换学校".format(response_data["data"]["schoolName"]))
                    user_id = jsonpath.jsonpath(response_data, "$..id")[0]
                    token = jsonpath.jsonpath(response_data, "$..token")[0]
                    deviceId = jsonpath.jsonpath(response_data, "$..deviceId")[0]
                    response_data = self._changeSchool(user_id, token, deviceId)
                log.info("登录返回数据--->{0}".format(response_data))
                for arg in args:
                    data.append(jsonpath.jsonpath(response_data, "$..%s" % (arg,))[0])
                log.info("登录返回内容--->{0}".format(data))
                return data
            else:
                log.info("登录失败，错误信息--->{0}".format(response_data["message"]))
                return None
        except Exception as e:
            log.error("出错信息--->{0}".format(e))

    def _changeSchool(self, user_id, token, deviceId):
        change_url = self.COMPUS + "/compus/user/changeSchool"
        change_data = {
            "deviceId": deviceId,
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
            log.info("登录data--->{0}".format(getCode_data))
            response_getCode = requests.get(url=getCode_url, params=getCode_data, headers=self.headers).text
            code = re.findall(r'\"([a-zA-Z0-9]{17,})\"', response_getCode)[0]
            log.info("code--->{0}".format(code))
            url_getUser4Authorize = self.LIFE + "/api/ums/login/getUser4Authorize"
            data_getUser4Authorize = {
                "code": code,
                "userId": "",
                "schoolCode": "",
            }
            log.info("请求data信息--->{0}".format(data_getUser4Authorize))
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
    print(Login_PW(login_phone='18866674052', login_PATH='pre', school_code='12061', platform='YUNMA_APP').login('token', 'id'))
