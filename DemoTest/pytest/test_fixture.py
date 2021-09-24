# _*_ coding:utf-8 _*_
import os
import sys
import pytest
import allure

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

'''
firture相对于setup和teardown来说应该有以下几点优势
命名方式灵活，不局限于setup和teardown这几个命名
conftest.py 配置里可以实现数据共享，不需要import就能自动找到一些配置
scope=”module” 可以实现多个.py跨文件共享前置
scope=”session” 以实现多个.py跨文件使用一个session来完成多个用例
fixture(scope="function", params=None, autouse=False, ids=None, name=None):
:arg scope: scope 有四个级别参数 "function" (默认), "class", "module" or "session".
:arg params: 一个可选的参数列表，它将导致多个参数调用fixture功能和所有测试使用它
:arg autouse:  如果为True，则为所有测试激活fixture func 可以看到它。 如果为False（默认值）则显式需要参考来激活fixture
:arg ids: 每个字符串id的列表，每个字符串对应于params 这样他们就是测试ID的一部分。 如果没有提供ID它们将从params自动生成
:arg name:   fixture的名称。 这默认为装饰函数的名称。 如果fixture在定义它的同一模块中使用，夹具的功能名称将被请求夹具的功能arg遮蔽; 解决这个问题的一种方法是将装饰函数命名
                   “fixture_ <fixturename>”然后使用”@ pytest.fixture（name ='<fixturename>'）“”。
Fixtures可以选择使用yield语句为测试函数提供它们的值，而不是return。 在这种情况下，yield语句之后的代码块作为拆卸代码执行，而不管测试结果如何。fixture功能必须只产生一次

'''

'''
fixture参数传入（scope=”function”）
如果@pytest.fixture()里面没有参数，那么默认scope=”function”，也就是此时的级别的function，针对函数有效


'''

# @pytest.fixture()  # 不带参数时默认scope="function"
# def login():
#     print("输入账号，密码先登录")
#
#
# def test_s1(login):
#     print("用例1：登录之后其它动作111")
#
#
# def test_s2():  # 不传login
#     print("用例2：不需要登录，操作222")
#
#
# def test_s3(login):
#     print("用例3：登录之后其它动作333")


'''
fixture参数传入（scope=”module”）
fixture参数scope=”module”，module作用是整个.py文件都会生效，用例调用时，参数写上函数名称就行

yield
1.如果其中一个用例出现异常，不影响yield后面的teardown执行,运行结果互不影响，并且在用例全部执行完之后，会呼唤teardown的内容
2.如果在setup就异常了，那么是不会去执行yield后面的teardown内容了
3.yield也可以配合with语句使用，
yield和addfinalizer方法都是在测试完成后呼叫相应的代码
'''


# 三个地方都调用了open函数，但是它只会在第一个用例前执行一次
@pytest.fixture(scope="module")  # 在用例前加前置条件，相当于setup
def open():
    print("打开浏览器，并且打开百度首页")
    yield
    print("执行teardown!")
    print("最后关闭浏览器")


def test_s00():
    print("用例0：搜索python-0")


def test_s11(open):
    print("用例1：搜索python-1")


def test_s22(open):  # 不传login
    print("用例2：搜索python-2")


def test_s33(open):
    print("用例3：搜索python-3")


def test_s44():  # 不传open
    print("用例4：搜索python-4")


if __name__ == "__main__":
    # pytest.main(["-s", "test_fixture.py"])
    pytest.main(["-s", "test_fixture.py"])