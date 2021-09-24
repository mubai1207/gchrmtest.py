# _*_ coding:utf-8 _*_
import os
import sys
import pytest  # 引入pytest包
import allure

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestClass:
    def test_one(self):
        x = "this"
        assert 'h' in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')

    def test_three(self):
        a = "hello"
        b = "hello world"
        assert a in b


if __name__ == '__main__':
    # pytest.main(['-s', '-q'])
    pytest.main(['-q', 'test_class.py'])
