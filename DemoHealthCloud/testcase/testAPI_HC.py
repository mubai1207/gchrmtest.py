#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'RaoPQ'

import os, sys
import unittest, ddt
import shutil
import configparser
import urllib3
import warnings
import requests
from DemoHealthCloud.config import setting
from DemoHealthCloud.lib.readExcel import ReadExcel
from DemoHealthCloud.lib.writeExcel import WriteExcel
from DemoHealthCloud.lib.getJsonPath import getJson
from DemoHealthCloud.lib.log import Log
from DemoHealthCloud.lib.sendRequests import send_requests
from DemoHealthCloud.lib.login import Login

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
readExcel = ReadExcel(setting.SOURCE_FILE)  # 获取测试用例文件
testData = readExcel.read_data()
cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='UTF-8')
log = Log().getLog()

LoginName = cf.get("user", "USER_1")
PWD = cf.get('pwd', 'PWD_1')
urllib3.disable_warnings()


@ddt.ddt
class Demo_API(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # if not os.path.exists(setting.TARGET_FILE):  # 文件不存在，则拷贝模板文件至指定报告目录下
        shutil.copyfile(setting.SOURCE_FILE, setting.TARGET_FILE)  # 拷贝模板文件至指定报告目录下
        cls.login_PATH = testData[0]["Access"]
        cls.s = requests
        for _d in testData:
            if _d['ID'] == "login":
                if 'captcha' in eval(_d['body']):
                    cls.loginData = Login(login_PATH=cls.login_PATH, login_data=_d['body']).login()
                else:
                    log.info("登录不需要验证码")
                    pass

        cls.writeData = WriteExcel(setting.TARGET_FILE)
        cls.health_cloud = cf.get(cls.login_PATH, "health_cloud")

    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        pass

    def tearDown(self):
        pass

    @ddt.data(*testData)
    def test_Api(self, data):
        PASS_data, FAIL_data, NA_data = "PASS", "FAIL", "NA"
        rowNum = int(data['number'])
        case = "{0}_{1}_{2} ".format(data['module'], data['Case'], data['ID'])  # data['module']+data['ID']+data['Case']
        if data["run"].upper() in ['Y', 'YES']:  # 判断用例是否需要执行
            log.info("******* 正在执行用例 ->{0} *********".format(case))
            response_data = send_requests(self.s, data)
            if response_data:
                if ('n' in response_data and response_data.get('n')) or ('msg' in response_data):  # 判断返回是否为空
                    if 'msg' in response_data:
                        result_code = int((getJson(response_data, 'code')[0]))  # msg返回的状态码
                    else:
                        result_code = int((getJson(response_data, 'result')[0]))  # 返回的状态码
                    read_code = int(data["result_code"])  # 获取excel表格数据的状态码
                    if data["message"]:  # 判断excel表格message数据是否有值,有值则需要判断message数据
                        read_message, read_text = data["message"].split('=')  # 获取excel表格message数据
                        result_text = str(getJson(response_data, read_message)[0])
                        if read_code == result_code and read_text == result_text:  # 判断状态码和返回信息是否相等，相等则测试用例执行通过
                            log.info("用例-->{0},测试结果:---->{1}".format(case, PASS_data))
                            self.writeData.write_data(rowNum + 1, PASS_data)  # 写入执行的结果
                        if read_code != result_code or read_text != result_text:
                            log.error("用例-->{0},测试结果:---->{1}".format(case, FAIL_data))
                            self.writeData.write_data(rowNum + 1, FAIL_data)
                            if read_code != result_code:
                                log.error("result_code 预期结果--->{0}，实际结果是--->{1}".format(read_code, result_code))
                            if read_text != result_text:
                                log.error("result_text 预期结果--->{0}，实际结果是--->{1}".format(read_text, result_text))
                    else:  # message没有值则直接判断readData_code
                        if read_code == result_code:  # 判断状态码，相等则测试用例执行通过
                            log.info("用例-->{0},测试结果:---->{1}".format(case, PASS_data))
                            self.writeData.write_data(rowNum + 1, PASS_data)  # 写入执行的结果
                        elif read_code != result_code:
                            log.error("用例-->{0},测试结果:---->{1}".format(case, FAIL_data))
                            self.writeData.write_data(rowNum + 1, FAIL_data)
                            log.error("result_code 预期结果--->{0}，返回实际结果是--->{1}".format(read_code, result_code))
                        else:
                            log.debug("用例-->{0},测试结果:---->{1}".format(case, NA_data))
                            self.writeData.write_data(rowNum + 1, NA_data)
                elif 'n' in response_data:
                    log.error('用例-->{0},返回内容是空--->{1}'.format(case, response_data['n']))
                    self.writeData.write_data(rowNum + 1, "Error")
                else:
                    log.error('用例-->{0},返回内容出错了--->{1}'.format(case, response_data))
                    self.writeData.write_data(rowNum + 1, "Error")
            else:
                log.error("用例-->{0}接口没有返回信息--->{1}".format(case, response_data))
                self.writeData.write_data(rowNum + 1, "Error")
        else:  # 判不执行直接跳过
            log.warning('用例-->{0},不执行！'.format(case))
            self.writeData.write_data(rowNum + 1, "not run")


if __name__ == '__main__':
    unittest.main()
