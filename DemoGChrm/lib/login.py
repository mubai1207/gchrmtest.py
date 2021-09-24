# _*_ coding:utf-8 _*_
import configparser
import json
import os
import hashlib
import sys
import re
from DemoGChrm.lib.log import Log
from DemoGChrm.config import setting
from DemoGChrm.lib.sendRequests import send_requests
from DemoGChrm.lib.getJsonPath import getJson

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
log = Log().getLog()
cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='UTF-8')
headers = eval(cf.get('headers', 'HEADERS-Chrome'))


class LoginHrm:
    """登录"""

    def __init__(self, login_PATH, login_user=None, login_pwd=None):
        log.debug("登录环境--->{0}".format(login_PATH))
        USER = cf.get("user", "USER_1")
        if login_user:
            self.login_name = login_user
        else:
            self.login_name = USER

        if login_pwd:
            self.pwd = login_pwd
        else:
            self.pwd = self.login_name
        self.hrmapi = cf.get(login_PATH, "hrmapi")
        self.corp_id = cf.get(login_PATH, 'corp_id')

    def login(self):
        key_url = self.hrmapi + "/hrm/user/rsa/public/key/query"
        login_url = self.hrmapi + "/hrm/user/login"

        get_key_data = {"n": {"user_code": self.login_name}, "a": {"source": "1284"}, "v": {}}
        response_key = send_requests(method='post', url=key_url, data=json.dumps(get_key_data))
        is_true(response_key, '获取登录key')

        random_key = response_key['n']['random_key']
        pwd = self.pwd + random_key
        md5 = hashlib.md5()
        md5.update(pwd.encode('utf-8'))
        pwd_md5 = md5.hexdigest()
        login_data = {"n": {"user_code": self.login_name, "user_pwd": pwd_md5, "corp_id": self.corp_id}, "a": {"source": "1284"}}
        response_login = send_requests(method='post', url=login_url, data=json.dumps(login_data))
        is_true(response_login, '登录结果')
        # session_id = getJson(response_login, 'session_id')[0]
        # if session_id:
        #     session["session_id"] = session_id
        #     with open(setting.SESSION_FILE, 'w', encoding='utf8')as fp:
        #         json.dump(session, fp, ensure_ascii=False)
        return response_login


class LoginWorkBase:
    """招聘平台登录"""

    def __init__(self, login_PATH, login_phone=None):
        log.debug("登录环境--->{0}".format(login_PATH))
        self.login_phone = login_phone
        self.hrmapi = cf.get(login_PATH, "hrmapi")
        self.corp_id = cf.get(login_PATH, 'corp_id')
        self.gcgateway = cf.get(login_PATH, "gcgateway")
        self.send_message = cf.get(login_PATH, "send_message")
        self.session = getJson(login_hrm(login_PATH), 'session_id')[0]

    def login(self):
        """获取登录验证码"""
        get_message_data = {"n": {"out_organ_id": self.corp_id, "phone": self.login_phone, "project_id": "hrm", "notice_title": 120},
                            "a": {"source": "1"},
                            "v": {}}
        get_message_url = self.gcgateway + "/unify_users/user/get/phone/code"
        response_get_message = send_requests(method='post', url=get_message_url, data=json.dumps(get_message_data))
        code_id = getJson(response_get_message, 'code_id')[0]
        is_true(response_get_message, '获取登录验证码')

        '''执行验证码发送任务'''
        send_message_url = self.send_message + '/unify_users/notice/job/send/message'
        response_send_message = send_requests(method='post', url=send_message_url)
        is_true(response_send_message, '执行验证码发送任务')

        '''查询发送的验证码'''
        notice_message_url = self.gcgateway + '/unify_message/notice/message/query'
        notice_message_data = {"n": {"user_name": "", "user_phone": self.login_phone, "message_content": "", "send_type": "295"},
                               "a": {"source": "1284"},
                               "v": {"session_id": self.session},
                               "f": {"indexpage": 1, "repaging": "1", "pagesize": 10}}
        response_notice_message = send_requests(method='post', url=notice_message_url, data=json.dumps(notice_message_data))
        message_content = getJson(response_notice_message, 'message_content')[0]
        code_number = re.findall(r"\d+", message_content)[0]

        '''验证码登录'''
        phone_login_data = {"a": {"source": "1"},
                            "n": {"corp_id": self.corp_id, "code_id": code_id, "code_number": code_number, "phone": self.login_phone}, "v": {}}
        phone_login_url = self.hrmapi + "/hrm/user/check/phone/code"
        response_phone_login = send_requests(method='post', url=phone_login_url, data=json.dumps(phone_login_data))
        is_true(response_phone_login, '用户登录结果')
        return response_phone_login


def is_true(obj, msg):
    if getJson(obj, 'message')[0] == '成功':
        log.info(msg + "成功")
    else:
        log.error('{0}失败,失败信息--->{1}'.format(msg, obj))


def login_hrm(path, user=None, pwd=None):
    return LoginHrm(login_user=user, login_pwd=pwd, login_PATH=path).login()


def login_work_base(path, phone):
    return LoginWorkBase(login_phone=phone, login_PATH=path).login()


if __name__ == '__main__':
    # print(login_hrm(user="GC0200074603961341", path='test'))
    print(login_work_base(phone="15103477778", path='test'))
