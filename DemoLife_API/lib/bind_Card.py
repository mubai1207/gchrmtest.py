# _*_ coding:utf-8 _*_
import configparser
import sys
import os
import jsonpath
import requests
from DemoLife_API.lib.log import Log
from DemoLife_API.config import setting
from DemoLife_API.lib.login_PW import Login_PW

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='UTF-8')

log = Log().getLog()


class BindCard(object):
    def __init__(self, s, id, token, login_PATH, school_code='yq025', platform=None):

        self.s = s
        self.id = id
        self.token = token
        self.platform = platform
        self.headers = eval(cf.get("headers", "HEADERS-SM"))

        self.school_code = school_code
        log.info("登录环境--->{0}".format(login_PATH))
        log.info("登录平台--->{0}".format(self.platform))
        self.COMPUS = cf.get(login_PATH, "compus")
        self.account = None

    def _getUserById(self):
        getUser_url = self.COMPUS + "/compus/user/getUserById"
        getUser_data = {
            "id": self.id,
            "schoolCode": self.school_code,
            "token": self.token,
            "platform": self.platform,
        }
        try:
            response_getUser = self.s.post(url=getUser_url, data=getUser_data, headers=self.headers).json()
            log.info("返回的用户信息--->{0}".format(response_getUser))
            if response_getUser["statusCode"] == 0:
                bindCardStatus = jsonpath.jsonpath(response_getUser, "$..bindCardStatus")[0]
                userName = jsonpath.jsonpath(response_getUser, "$..userName")[0]
                self.account = jsonpath.jsonpath(response_getUser, "$..account")[0]
            else:
                log.info("没有用户信息--->{0}".format(response_getUser["message"]))
        except Exception as e:
            log.error("出错信息--->{0}".format(e))
        if bindCardStatus == 1:
            log.info("该账号已绑卡，绑卡姓名--->{0}".format(userName))
            bindCardStatus = True
        else:
            log.info("该账号未绑卡")
            bindCardStatus = False
        return bindCardStatus

    def bindCard(self, realName="云马202", incomeAccount="YM202"):
        bindCard_url = self.COMPUS + "/compus/user/bindCard"
        bindCard_data = {
            "realName": realName,
            "incomeAccount": incomeAccount,
            "accountType": "2",
            "id": self.id,
            "schoolCode": self.school_code,
            "token": self.token,
            "platform": self.platform,
        }
        try:
            if self._getUserById() is False:
                response_bindCard = self.s.post(url=bindCard_url, data=bindCard_data, headers=self.headers).json()
                log.info("返回的绑卡信息--->{0}".format(response_bindCard))
                if response_bindCard["statusCode"] == 0 and self._getUserById():
                    log.info("账号_{0}，绑卡成功".format(self.account))
                else:
                    log.info("账号_{0}，绑卡失败--->{1}".format(self.account, response_bindCard["message"]))
            else:
                log.info("该账号_{0}，已绑卡".format(self.account))
        except Exception as e:
            log.error("出错信息--->{0}".format(e))


if __name__ == '__main__':
    bc = BindCard(login_phone=18866667777, login_PATH='lsmart', school_code=12061, platform='YUNMA_APP')
    bc.bindCard()
