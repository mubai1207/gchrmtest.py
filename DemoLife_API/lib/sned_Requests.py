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

log = Log()
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
testData = ReadExcel(setting.SOURCE_FILE, "健康云")  # 获取测试用例文件
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='UTF-8')
headers = eval(cf.get('headers', 'HEADERS-Chrome'))


class SendRequests:
    """发送请求"""

    def sendRequests(self, s, apiData):

        try:
            method = apiData["method"]
            url = apiData["url"]
            if apiData["params"] == "":  # get请求params
                par = None
            else:
                par = eval(apiData["params"])
            if apiData["headers"] == "":
                h = headers
            else:
                h = eval(apiData["headers"])

            if apiData["body"] == "":  # post请求body
                body_data = None
            else:
                body_data = eval(apiData["body"])
                if len(apiData["depend"]) > 0:  # 判断是否需要先执行其他关联用例
                    depend_number = apiData["depend"].split(',')[0]
                    depend_data = apiData["depend"].split(',')[1:]
                    if depend_data is None:
                        depend_number = apiData["depend"]
                        dict_data = testData.read_nrow(int(depend_number))
                        response_depend = SendRequests.sendRequests(self, s, dict_data)[0]
                    else:
                        dict_data = testData.read_nrow(int(depend_number))
                        response_depend = SendRequests.sendRequests(self, s, dict_data)[0]
                        values = []
                        for depend in depend_data:
                            values.append(jsonpath.jsonpath(response_depend.json(), "$..%s" % depend)[0])
                        new_data = dict(zip(depend_data, values))
                        body_data = dict(body_data, **new_data)

                # if apiData["token"].upper() in ['Y', 'YES']:  # 判断是否需要token
                #     token = GetToken().get_token()  # 获取文件中写入的token
                #     body_data = dict(body_data, **token)  # 合并token与excel文件中的请求

            type = apiData["type"]  # 判断请求体格式

            if type == "data":
                body = body_data
            elif type == "json":
                body = json.dumps(body_data)
            else:
                body = body_data

            # 执行请求，返回请求结果
            if method == 'post':
                re = s.post(url=url, headers=h, data=json.dumps(body), verify=False)
            elif method == 'get':
                re = s.get(url=url, headers=h, params=json.dumps(par), verify=False)
            else:
                return "method error"
            return re, body

        except Exception as e:
            print(e)
