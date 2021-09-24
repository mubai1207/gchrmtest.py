# _*_ coding:utf-8 _*_
import base64
import sys

card_num = sys.argv[1]  # 返回一个列表形式


def get_card(card_num):
    data = {'yljgdm': '47128802033052311A1001', 'zgbm': '1002', 'klx': '8', 'kh': card_num}
    get_card_num = str(base64.b64encode(str(data).encode("utf-8")), "utf-8")
    return get_card_num


if __name__ == '__main__':
    print(get_card(card_num))
