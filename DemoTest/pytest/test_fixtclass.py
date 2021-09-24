# _*_ coding:utf-8 _*_
import os
import sys
import pytest
import allure

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

'''
setup/teardown和unittest里面的setup/teardown是一样的功能
setup_class和teardown_class等价于unittest里面的setupClass和teardownClass
这里setup_method和teardown_method的功能和setup/teardown功能是一样的，一般二者用其中一个即可
'''


def setup_module():
    print("setup_module：整个.py模块只执行一次")
    print("比如：所有用例开始前只打开一次浏览器")


def teardown_module():
    print("teardown_module：整个.py模块只执行一次")
    print("比如：所有用例结束只最后关闭浏览器")


def setup_function():
    print("setup_function：每个用例开始前都会执行")


def teardown_function():
    print("teardown_function：每个用例结束前都会执行")


def test_one():
    print("正在执行----test_one")
    x = "this"
    assert 'h' in x


def test_two():
    print("正在执行----test_two")
    x = "hello"
    # assert hasattr(x, 'check')


class TestCase():

    def setup_class(self):
        print("setup_class：所有用例执行之前")

    def teardown_class(self):
        print("teardown_class：所有用例执行之前")

    def test_three(self):
        print("正在执行----test_three")
        x = "this"
        assert 'h' in x

    def test_four(self):
        print("正在执行----test_four")
        x = "hello"
        # assert hasattr(x, 'check')


if __name__ == "__main__":
    pytest.main(["-s", "test_fixtclass.py"])
