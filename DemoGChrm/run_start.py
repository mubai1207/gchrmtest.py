#!/usr/bin/env python
# _*_ coding:utf-8 _*_


__author__ = 'RaoPQ'

"""
运行测试脚本
"""
import os, sys
from DemoGChrm.config import setting
import unittest, time
from DemoGChrm.testcase import test_Add_YRXQ
from DemoGChrm.testcase import test_Add_GRJL
from DemoGChrm.testcase import test_GWBM
from DemoGChrm.testcase import test_Check_JLSH
from DemoGChrm.testcase import test_Check_MSGL
from DemoGChrm.testcase import test_Add_ZZRY
from lib.newReport import new_report
from DemoGChrm.package.HTMLTestRunner import HTMLTestRunner

sys.path.append(os.path.dirname(__file__))


def run_case(result_path=setting.TEST_CASE):
    # test_data.init_data()# 初始化接口测试数据（调用数据库执行数据库操作）
    # now = time.strftime("%Y-%m-%d %H_%M_%S")  # 获取当前系统时间
    # filename = result_path + '/' + now + 'result.html'  # 定义报告名称
    # fp = open(filename, 'wb')
    # runner = HTMLTestRunner(stream=fp, title='接口自动化测试报告', description='环境：windows 10 浏览器：chrome', tester='RaoPQ')
    # runner.run(all_case)  # 执行所有的测试用例
    # fp.close()
    #
    # report = new_report(setting.TEST_REPORT)  # 调用模块生成最新的报告
    # discover = unittest.defaultTestLoader.discover(result_path, pattern="test*.py")
    # print(discover)
    # suite = unittest.TestSuite()
    # suite.addTest(discover)
    # return suite
    result_path = setting.TEST_REPORT
    suite = unittest.TestSuite()
    # suite.addTest(test_Add_YRXQ.MyTestCase('test_run', 'test', 'GC0200074603961341'))  # 添加用人需求
    # suite.addTest(test_Add_GRJL.MyTestCase('test_run', 'test', '13234166661'))  # 个人简历填写
    # suite.addTest(test_GWBM.MyTestCase('test_run', 'test', '13234166661'))  # 招聘岗位报名
    # suite.addTest(test_JLSH.MyTestCase('test_run', 'test', '13234166661'))  # 简历审核
    # suite.addTest(test_MSGL.MyTestCase('test_run', 'test', '13234166661'))  # 面试管理
    suite.addTest(test_Add_ZZRY.MyTestCase('test_run', 'test', 'GC0200074603961341'))  # 在职人员

    now = time.strftime("%Y-%m-%d %H_%M_%S")  # 获取当前系统时间
    filename = result_path + '/' + now + '_result.html'  # 定义报告名称
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp, title='接口自动化测试报告', description='环境：windows 10 浏览器：chrome', tester='RaoPQ')
    # runner.run(all_case)  # 执行所有的测试用例
    # runner = unittest.TextTestRunner()
    runner.run(suite)
    fp.close()


if __name__ == "__main__":
    run_case()
