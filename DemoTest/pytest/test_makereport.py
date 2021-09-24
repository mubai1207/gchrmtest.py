from selenium import webdriver
import time
import pytest


def test_yoyo_01(browser: webdriver.Firefox):
    browser.get("https://www.cnblogs.com/yoyoketang/")
    time.sleep(2)
    t = browser.title
    assert t == "上海-悠悠"


def test_yoyo_01(browser: webdriver.Firefox):
    browser.get("https://www.cnblogs.com/yoyoketang/")
    time.sleep(2)
    t = browser.title
    assert "上海-悠悠" in t


if __name__ == "__main__":
    # pytest.main(["-s", "test_fixture.py"])
    pytest.main(["-s", "test_fixture.py",'--html=./report/report.html'])
