#!/usr/bin/env python
# _*_ coding:utf-8 _*_


__author__ = 'RaoPQ'

import configparser
import jsonpath
import os, sys, json
import urllib3
from DemoHealthCloud.lib.readExcel import ReadExcel
from DemoHealthCloud.config import setting
from DemoHealthCloud.lib.log import Log
from DemoHealthCloud.lib.getToken import getToken

log = Log().getLog()
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
testData = ReadExcel(setting.SOURCE_FILE)  # 获取测试用例文件
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='utf-8')
headers = eval(cf.get('headers', 'HEADERS-Chrome'))
urllib3.disable_warnings()

module_dict = {"全民健康平台": "health_cloud",
               "居民健康档案": "people_record",
               "视图360": "medic_360",
               "移动医生": "dingtalk_doctor"}

"""发送请求"""


def send_requests(s, apiData):
    module_url, response_data = None, None
    module = apiData["module"]
    for key, var in module_dict.items():
        if key.find(module) != -1:
            module_url = cf.get(apiData["Access"], var)

    if module_url:
        url = module_url + apiData["url"]
    else:
        url = apiData["url"]
        log.info("未匹配到module内容，直接获取填写的url")
    par = apiData["params"]  # get请求params
    method = apiData["method"]
    h = headers
    if apiData["token"] in 'y':
        if getToken():
            h = getToken()
        else:
            log.error("toekn.json 中没有内容")

    if apiData["body"] == "":  # post请求body
        body_data = None
    else:
        body_data = eval(apiData["body"])
    if apiData["depend"]:  # 判断是否需要先执行其他关联用例
        depend = apiData["depend"].split(',')
        depend_data = depend[1:-1]  # 从关联用例需要获取的数据
        # depend_number = depend[0]  # 关联用例编码
        # depend_nature = depend[-1]  # 关联用例获取数据个数0是所有

        if len(depend) <= 2:
            depend_number = apiData["depend"]
            dict_data = testData.read_row(int(depend_number))
            response_depend = send_requests(s, dict_data)
            log.debug("执行成功")
        else:
            dict_data = testData.read_row(int(depend[0]))
            response_depend = send_requests(s, dict_data)
            if response_depend:
                if depend[-1].isdigit() and int(depend[-1]) != 0:
                    _num = int(depend[-1])
                    # for _data in depend_data:
                    #     _get_data = jsonpath.jsonpath(response_depend, "$..%s" % _data)[_num - 1]
                    #     for k, v in body_data.items():
                    #         if '$' in str(v):
                    #             v1 = v.split('$')[1]
                    #             if v1 == _data:
                    #                 body_data[k] = _get_data
                    _list = []
                    for _data in depend_data:
                        _list.append(jsonpath.jsonpath(response_depend, "$..%s" % _data)[_num - 1])
                    new_dic = dict(zip(depend_data, _list))
                    body_data = dict(eval(apiData["body"]), **new_dic)

                else:
                    if jsonpath.jsonpath(response_depend, "$..%s" % depend_data[0]):
                        for num, _str in enumerate(jsonpath.jsonpath(response_depend, "$..%s" % depend_data[0])):
                            # get_list = {}
                            # body_data = eval(apiData["body"])
                            # for _data in depend_data:
                            #     _get_data = jsonpath.jsonpath(response_depend, "$..%s" % _data)[num]
                            #     get_list = dict(get_list, **{_data: _get_data})
                            # for k, v in body_data.items():
                            #     if '$' in str(v):
                            #         v1 = v.split('$')[1]
                            #         if v1 in get_list.keys():
                            #             body_data[k] = get_list[v1]
                            _list = []
                            for _data in depend_data:
                                _list.append(jsonpath.jsonpath(response_depend, "$..%s" % _data)[num])
                            new_dic = dict(zip(depend_data, _list))
                            body_data = dict(eval(apiData["body"]), **new_dic)
                            log.debug("\n请求方式: {0}\n请求URL: {1}\n请求data: {2}".format(method, url, body_data))
                            log.info(
                                "第{0}次，请求{1}".format(num + 1, _requests(s, method, url, h, body=json.dumps(body_data))))

                    else:
                        log.info("返回内容中未找到对应的内容-->{0}".format(depend_data[0]))
                        return response_data

            else:
                log.error("关联接口执行出错")

    typ = apiData["type"]  # 判断请求体格式
    if typ == "data":
        body = body_data
    elif typ == "json":
        body = json.dumps(body_data, ensure_ascii=False)
    else:
        body = body_data

    return _requests(s, method, url, h, body=body, par=par)


def _requests(s, method, url, h, body=None, par=None):
    if method == 'post':
        log.debug("\n请求方式: {0}\n请求URL: {1}\n请求data: {2}".format(method, url, body))
        response_data = s.post(url=url, headers=h, data=body, verify=False)

    elif method == 'get':
        log.debug("\n请求方式: {0}\n请求URL: {1}\n请求params: {2}".format(method, url, par))
        response_data = s.get(url=url, headers=h, params=par, verify=False)
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
    import requests

    data = {'number': 2.0, 'module': '视图360_DE', 'ID': 'major', 'UseCase': 'major', 'Access': 'test',
            'url': 'http://47.97.43.115:8083/certification/login/authValid', 'method': 'post', 'params': '',
            'token': 'n',
            'body': '{"zgbm":"1002","txHash1":"","klx":"8","yljgdm":"47128802033052311A1001","txHash2":"","kh":"330523193508250038"}',
            'type': 'data', 'depend': '', 'run': 'y', 'result_code': 1.0, 'message': 'message=成功', 'result': '',
            ' testers': ''}

    print(send_requests(requests, data))
