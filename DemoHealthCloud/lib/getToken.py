# _*_ coding:utf-8 _*_
__author__ = 'RaoPQ'

import os, sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from DemoHealthCloud.config import setting


def getToken():
    with open(setting.TOKEN_FILE, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
        if list(json_data.values())[0]:
            return json_data
        else:
            return None
            # print("toekn.json 中没有内容")


if __name__ == '__main__':
    # headers = {
    #     "Content-Type": "11111", }
    # with open(setting.TOKEN_FILE, 'w', encoding='utf8')as fp:
    #     json.dump(headers, fp, ensure_ascii=False)

    print(getToken())
