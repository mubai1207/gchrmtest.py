#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

# 配置文件
TEST_CONFIG = os.path.join(BASE_DIR, "database", "config.ini")

LOG_DIR = os.path.join(BASE_DIR, "logs")

# SOURCE_FILE = os.path.join(BASE_DIR, "database", "DemoAPITestCase.xlsx")
# # excel测试用例结果文件
# TARGET_FILE = os.path.join(BASE_DIR, "report", "excelReport", "DemoAPITestCaseReport.xlsx")
# # 测试用例报告
# TEST_REPORT = os.path.join(BASE_DIR, "report")
# # 测试用例程序文件
# TEST_CASE = os.path.join(BASE_DIR, "testcase")
# # token文件
# TOKEN_FILE = os.path.join(BASE_DIR, "database", "session.json")
