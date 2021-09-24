# _*_ coding:utf-8 _*_
__author__ = 'RaoPQ'

import requests
import hashlib
import json
import jsonpath

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    "accept": "application/json, text/plain, */*",
    "content-type": "application/json; charset=UTF-8"}

'''登录'''
key_url = "https://hrmapi.dingyl.com/hrm/user/rsa/public/key/query"

md5 = hashlib.md5()
key_data = {"n": {"user_code": "GC051112352635201960"}, "a": {"source": "1284"}, "v": {}}
response_key = requests.post(url=key_url, data=json.dumps(key_data), headers=HEADERS).json()
random_key = response_key['n']['random_key']
pwd = "GC051112352635201960" + random_key
md5.update(pwd.encode('utf-8'))
pwd_md5 = md5.hexdigest()
login_url = "https://hrmapi.dingyl.com/hrm/user/login"
login_data = {"n": {"user_code": "GC051112352635201960", "user_pwd": pwd_md5,
                    "corp_id": "ding62e2de207394d57f"}, "a": {"source": "1284"}}
response_login = requests.post(url=login_url, data=json.dumps(login_data), headers=HEADERS).json()
print(response_login)
session_id = jsonpath.jsonpath(response_login, "$..session_id")[0]
print(session_id)
'''新增'''
add_url = "https://hrmapitest.dingyl.com/hrm/worker/info/add"
add_data = {
    "n": {
        "template_id": "1221",
        "template_type": "771",
        "worker_info": {
            "72": {
                "user_complete_cultivate_time": -1,
                "user_file_number": "D202108231430",
                "user_name": "姓名Aa",
                "user_cert_type": "15",
                "user_cert_number": "33001119920306112x",
                "user_sex": "280",
                "user_birth_time": "1992-03-06",
                "user_birth_month": "03-06",
                "user_age": 29,
                "remark": "备注A",
                "e4760fb20168473f854ea6af64d3aa10": "准入证",
                "5a397f4f8738419ca072b8f68d0a0009": "2021-08-25T16:00:00.000Z",
                "3eb923fa7bea469596090fabccc57cfb": "职业资格证书编号BBb",
                "f297dcc358b542f284b06c9fd1151764": "职业资格证书颁发单位BBBb",
                "extra_info": {
                    "e4760fb20168473f854ea6af64d3aa10": "准入证",
                    "5a397f4f8738419ca072b8f68d0a0009": "2021-08-25T16:00:00.000Z",
                    "3eb923fa7bea469596090fabccc57cfb": "职业资格证书编号BBb",
                    "f297dcc358b542f284b06c9fd1151764": "职业资格证书颁发单位BBBb"
                },
                "user_avatar": "",
                "user_resume_type": "477"
            },
            "213": {
                "main_dept": ["dc85a1dd388d4d2d874ff511247c9aa2"],
                "supervisor": [],
                "work_number": "G202108231444A",
                "extra_info": {},
            },
            "314": {
                "extra_info": {}
            },
            "498": {
                "communication_phone": "18866660001",
                "extra_info": {}
            },
            "549": [],
            "1397": {
                "extra_info": {}
            },
            "1528": {
                "extra_info": {}
            },
            "1529": {
                "extra_info": {}
            }
        }
    },
    "a": {
        "source": "1284"
    },
    "v": {
        "session_id": session_id
    }
}

response_add = requests.post(url=add_url, data=json.dumps(add_data), headers=HEADERS).json()
print(response_add)
# '''删除'''
# es_url = "https://hrmapitest.dingyl.com/hrm/worker/info/es/query"
# es_data = {"n": {"query_string": {"worker_status": {"big_value": "", "query_type": 10,
#                                                     "small_value": ["73", "315", "426", "499", "550", "592", "624",
#                                                                     "1512", "1513", "1514", "1515", "1516", "1517",
#                                                                     "1518", "1519"], "value_format": ""}}},
#            "a": {"source": "1284"}, "v": {"session_id": session_id},
#            "f": {"indexpage": 1, "repaging": "1", "pagesize": 10}}
#
# response_es = requests.post(url=es_url, data=json.dumps(es_data), headers=HEADERS).json()
# # print(response_es)
# print(jsonpath.jsonpath(response_es, "$..worker_user_id")[0:2])
# delete_url = "https://hrmapitest.dingyl.com/hrm/base/user/info/delete"
#
# for user_id in jsonpath.jsonpath(response_es, "$..worker_user_id")[0:2]:
#     delete_data = {"n": {"work_user_id": user_id}, "a": {"source": "1284"}, "v": {"session_id": session_id}}
#     # response_delete = requests.post(url=delete_url, data=json.dumps(delete_data), headers=HEADERS).json()
#     # print(response_delete)
#
