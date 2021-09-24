#!/usr/bin/env python
# _*_ coding:utf-8 _*_


__author__ = 'RaoPQ'

import configparser
import os, sys, json
import urllib3
import requests
from DemoGChrm.lib.readExcel import ReadExcel
from DemoGChrm.config import setting
from DemoGChrm.lib.log import Log
from DemoGChrm.lib.getSession import getSession

log = Log().getLog()
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
testData = ReadExcel(setting.SOURCE_FILE)  # 获取测试用例文件
cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='utf-8')
headers = eval(cf.get('headers', 'HEADERS-Chrome'))
urllib3.disable_warnings()

"""发送请求"""


# def send_requests(s, apiData):
#     login_PATH = cf.get(apiData["Access"], "hrmapi")
#     url = login_PATH + apiData["url"]
#     par = apiData["params"]  # get请求params
#     method = apiData["method"]
#     h = headers
#
#     if apiData["body"] == "":  # post请求body
#         body_data = None
#     else:
#         body_data = eval(apiData["body"])
#
#     if apiData["token"] in 'y':
#         if getSession():
#             body_data['v'] = getSession()
#         else:
#             log.error("Session.json 中没有内容")
#     if apiData["depend"]:  # 判断是否需要先执行其他关联用例
#         depend = apiData["depend"].split(',')
#         depend_data = depend[1:-1]  # 从关联用例需要获取的数据
#         # depend_number = depend[0]  # 关联用例编码
#         # depend_nature = depend[-1]  # 关联用例获取数据个数0是所有
#         if len(depend) <= 2:
#             depend_number = apiData["depend"]
#             dict_data = testData.read_row(int(depend_number))
#             response_depend = send_requests(s, dict_data)
#             log.debug("执行成功")
#         else:
#             dict_data = testData.read_row(int(depend[0]))
#             response_depend = send_requests(s, dict_data)
#             if response_depend:
#                 if depend[-1].isdigit() and int(depend[-1]) != 0:
#                     _num = int(depend[-1])
#                     _list = []
#                     for _data in depend_data:
#                         _list.append(jsonpath.jsonpath(response_depend, "$..%s" % _data)[_num - 1])
#                     new_dic = dict(zip(depend_data, _list))
#                     body_data = dict(eval(apiData["body"]), **new_dic)
#
#                 else:
#                     if jsonpath.jsonpath(response_depend, "$..%s" % depend_data[0]):
#                         for num, _str in enumerate(jsonpath.jsonpath(response_depend, "$..%s" % depend_data[0])):
#                             _list = []
#                             for _data in depend_data:
#                                 _list.append(jsonpath.jsonpath(response_depend, "$..%s" % _data)[num])
#                             new_dic = dict(zip(depend_data, _list))
#                             body_data = dict(eval(apiData["body"]), **new_dic)
#                             log.debug("\n请求方式: {0}\n请求URL: {1}\n请求data: {2}".format(method, url, body_data))
#                             log.info(
#                                 "第{0}次，请求{1}".format(num + 1, _requests(s, method, url, h, body=json.dumps(body_data))))
#                     else:
#                         log.info("返回内容中未找到对应的内容-->{0}".format(depend_data[0]))
#
#             else:
#                 log.error("关联接口执行出错")
#
#     typ = apiData["type"]  # 判断请求体格式
#     if typ == "data":
#         body = body_data
#     elif typ == "json":
#         body = json.dumps(body_data, ensure_ascii=False)
#     else:
#         body = body_data
#
#     return _requests(s, method, url, h, body=body, par=par)


def send_requests(method, url, data=None, par=None):

    if method == 'post':
        log.debug("\n请求方式: {0}\n请求URL: {1}\n请求data: {2}".format(method, url, data))
        requests.packages.urllib3.disable_warnings()
        response_data = requests.post(url=url, headers=headers, data=data, verify=False)

    elif method == 'get':
        log.debug("\n请求方式: {0}\n请求URL: {1}\n请求params: {2}".format(method, url, par))
        requests.packages.urllib3.disable_warnings()
        response_data = requests.get(url=url, headers=headers, params=par, verify=False)
    else:
        log.error("请求方法有误--->{0}".format(method))
        return None
    if response_data.status_code != 200:
        log.error("接口出错了--->{0}".format(response_data))
        return None
    else:
        log.debug("返回内容--->{0}".format(response_data.json()))
        response_data.encoding = 'utf-8'
        return response_data.json()  # json.dumps(response_data.json(), sort_keys=True, separators=(',', ':'), indent=4, ensure_ascii=False)


# except Exception as e:
#     log.error("请求出错--->{0}".format(e))


if __name__ == '__main__':
    pass
    # import jsonpath
    #
    # data = {'number': 2.0, 'module': '用人需求_添加用人需求', 'ID': 'comboBox', 'Case': '需求岗位选择', 'Access': 'pro',
    #         'url': ' https://hrmapi.dingyl.com/hrm/dictionary/system/comboBox', 'method': 'post', 'params': '',
    #         'token': 'y',
    #         'body': '{"a":{"source":"1284"},"n":{"dictionary_group":"ZPGW"},"v":"session_id"}',
    #         'type': 'json', 'depend': '', 'run': 'y', 'result_code': 1.0, 'message': 'message=成功', 'result': '',
    #         ' testers': ''}
    # res = send_requests(requests, data)
    # print(jsonpath.jsonpath(res, "$..value"))
