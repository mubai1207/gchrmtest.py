# # coding:utf-8
# import pytest
#
# '''
# conftest.py配置需要注意以下点：
# conftest.py配置脚本名称是固定的，不能改名称
# conftest.py与运行的用例要在同一个pakage下，并且有init.py文件
# 不需要import导入 conftest.py，pytest用例会自动查找
# '''
#
# # @pytest.fixture()
# # def login():
# #     print("输入账号，密码先登录")
#
#
# from selenium import webdriver
# import pytest
#
# driver = None
#
#
# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item):
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, 'extra', [])
#
#     if report.when == 'call' or report.when == "setup":
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             file_name = report.nodeid.replace("::", "_") + ".png"
#             screen_img = _capture_screenshot()
#             if file_name:
#                 html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
#                        'onclick="window.open(this.src)" align="right"/></div>' % screen_img
#                 extra.append(pytest_html.extras.html(html))
#         report.extra = extra
#
#
# def _capture_screenshot():
#     return driver.get_screenshot_as_base64()
#
#
# @pytest.fixture(scope='session', autouse=True)
# def browser():
#     global driver
#     if driver is None:
#         driver = webdriver.Chrome(r"C:\Users\goocan\Desktop\pythonProject\DemoTest\chromedriver.exe")
#     return driver
