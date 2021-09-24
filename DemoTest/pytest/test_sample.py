# _*_ coding:utf-8 _*_
import os
import sys
import pytest  # 引入pytest包
import allure

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
'''

（1）‘-s’：关闭捕捉，输出打印信息。
（2）‘-v’:用于增加测试用例的冗长。
（3）‘-k’ ：运行包含某个字符串的测试用例。如：pytest -k add XX.py 表示运行XX.py中包含add的测试用例。
（4）‘q’:减少测试的运行冗长。
（5）‘-x’:出现一条测试用例失败就退出测试。在调试阶段非常有用，当测试用例失败时，应该先调试通过，而不是继续执行测试用例。


pytest用例规则:
文件名以test_*.py文件和*_test.py
测试文件以test_开头（以_test结尾也可以）
测试类以Test开头，并且不能带有 init 方法
测试函数以test_开头
断言使用assert


执行用例规则:
1.执行某个目录下所有的用例--------pytest 文件名/
2.执行某一个py文件下用例-----------pytest 脚本名称.py
3.-k 按关键字匹配-----------pytest -k “MyClass and not method”
4.按节点运行
    运行.py模块里面的某个函数-------pytest test_mod.py::test_func
    运行.py模块里面,测试类里面的某个方法---------pytest test_mod.py::TestClass::test_method
5.标记表达式-------pytest -m slow(将运行用@ pytest.mark.slow装饰器修饰的所有测试。)
6.从包里面运行------pytest —pyargs pkg.testing(这将导入pkg.testing并使用其文件系统位置来查找和运行测试。)
7.-x 遇到错误时停止测试-----pytest -x test_class.py
8.—maxfail=num-----pytest —maxfail=1（当用例错误个数达到指定数量时，停止测试）



用例运行级别:
模块级（setup_module/teardown_module）开始于模块始末，全局的
函数级（setup_function/teardown_function）只对函数用例生效（不在类中）
类级（setup_class/teardown_class）只在类中前后运行一次(在类中)
方法级（setup_method/teardown_method）开始于方法始末（在类中）
类里面的（setup/teardown）运行在调用方法的前后
'''


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 5


if __name__ == '__main__':
    pytest.main(['-s', '-q'])
