# _*_ coding:utf-8 _*_
import os
import sys
import pytest
import allure

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

'''
setup_function/teardown_function  每个用例开始和结束调用一次
setup_module是所有用例开始前只执行一次，teardown_module是所有用例结束后只执行一次
setup_function/teardown_function和setup_module/teardown_module这四种方法是可以任意组合的，用一个和多个都可以

setup/teardown和unittest里面的setup/teardown是一样的功能
setup_class和teardown_class等价于unittest里面的setupClass和teardownClass
这里setup_method和teardown_method的功能和setup/teardown功能是一样的，一般二者用其中一个即可
setup_module/teardown_module的优先级是最大的，然后函数里面用到的setup_function/teardown_function与类里面的setup_class/teardown_class互不干涉



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
    print("teardown_function：每个用例结束后都会执行")


def test_one():
    print("正在执行----test_one")
    x = "this"
    assert 'h' in x


def test_two():
    print("正在执行----test_two")
    x = "hello"
    # assert hasattr(x, 'check')


def test_three():
    print("正在执行----test_three")
    a = "hello"
    b = "hello world"
    assert a in b


if __name__ == "__main__":
    pytest.main(["-s", "test_fixt.py"])  # -s参数是为了显示用例的打印信息。 -q参数只显示结果，不显示过程
