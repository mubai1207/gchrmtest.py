# _*_ coding:utf-8 _*_
import os
import sys
import pytest
import allure

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

'''
pytest.mark.skip可以标记无法在某些平台上运行的测试功能，或者您希望失败的测试功能

skip意味着只有在满足某些条件时才希望测试通过，否则pytest应该跳过运行测试。
xfail意味着您希望测试由于某种原因而失败
'''
