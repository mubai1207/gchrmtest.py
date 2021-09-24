#!/usr/bin/env python
# _*_ coding:utf-8 _*_


__author__ = 'RaoPQ'

"""
运行测试脚本
"""
import shutil
import os, sys
from DemoHealthCloud.config import setting
import unittest, time
from lib.sendEmail import send_mail
from lib.newReport import new_report
from DemoHealthCloud.package.HTMLTestRunner import HTMLTestRunner

# from HTMLTestRunner import HTMLTestRunner

sys.path.append(os.path.dirname(__file__))


def add_case(test_path=setting.TEST_CASE):
    """加载所有的测试用例"""

    discover = unittest.defaultTestLoader.discover(test_path, pattern='test*.py')
    return discover


def run_case(all_case, result_path=setting.TEST_REPORT):
    # test_data.init_data()# 初始化接口测试数据（调用数据库执行数据库操作）

    now = time.strftime("%Y-%m-%d %H_%M_%S")  # 获取当前系统时间
    filename = result_path + '/' + now + 'result.html'  # 定义报告名称
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp, title='接口自动化测试报告', description='环境：windows 10 浏览器：chrome', tester='RaoPQ')
    runner.run(all_case)  # 执行所有的测试用例
    fp.close()

    report = new_report(setting.TEST_REPORT)  # 调用模块生成最新的报告
    # send_mail(report)  # 调用发送邮件模块


if __name__ == "__main__":
    # shutil.copyfile(setting.SOURCE_FILE, setting.TARGET_FILE)
    cases = add_case()
    run_case(cases)
