# _*_ coding:utf-8 _*_
import os
import sys
import pytest
import allure

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

'''
pytest.mark.parametrize装饰器可以实现测试用例参数化。

marks=pytest.mark.xfail 标记为失败的用例就不运行了，直接跳过显示xfailed

'''

# @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), pytest.param("6 * 9", 42, marks=pytest.mark.xfail), ])
# def test_eval(test_input, expected):
#     print("-------开始用例------")
#     assert eval(test_input) == expected
#
#
# ''' 1.若要获得多个参数化参数的所有组合，可以堆叠参数化装饰器'''
#
#
# @pytest.mark.parametrize("x", [0, 1])
# @pytest.mark.parametrize("y", [2, 3])
# def test_foo(x, y):
#     print("测试数据组合：x->%s, y->%s" % (x, y))


# 测试登录数据
# 测试账号数据
test_user = ["admin1", "admin2"]
test_psw = ["11111", "22222"]


@pytest.fixture(scope="module")
def input_user(request):
    user = request.param
    print("登录账户：%s" % user)
    return user


@pytest.fixture(scope="module")
def input_psw(request):
    psw = request.param
    print("登录密码：%s" % psw)
    return psw


@pytest.mark.parametrize("input_user", test_user, indirect=True)
@pytest.mark.parametrize("input_psw", test_psw, indirect=True)
def test_login(input_user, input_psw):
    '''登录用例'''
    a = input_user
    b = input_psw
    print("测试数据a-> %s， b-> %s" % (a, b))
    assert b


if __name__ == "__main__":
    pytest.main(["-s", "test_parametrizing.py"])
