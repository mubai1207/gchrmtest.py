# _*_ coding:utf-8 _*_
import os
import sys
import pytest
import allure

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def test_answer(cmdopt):
    if cmdopt == "type1":
        print("first")
    elif cmdopt == "type2":
        print("second")
    assert 0  # to see what was printed


if __name__ == "__main__":
    pytest.main(["-s", "test_contetest.py"])
