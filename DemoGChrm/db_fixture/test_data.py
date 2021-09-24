#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'RaoPQ'

import sys, time, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from DemoGChrm.lib.mysql_db import DB

# 定义过去时间
past_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - 100000))
# 定义将来时间
future_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 10000))

# 创建测试数据
datas = {
}


# 测试数据插入表
def init_data():
    DB().init_data(datas)
