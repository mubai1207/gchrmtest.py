# _*_ coding:utf-8 _*_
import datetime
import os
import re
import sys
import requests
import pytesseract
import time
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
}


def _get_picture():
    get_img_url = "http://47.97.43.115:8082/aj_healthcloud/login/captcha?timestamp=" + str(int((time.time() * 1000)))
    timestamp = datetime.datetime.now().strftime("%a %b %d %Y %H:%M:%S GMT 0800 (中国标准时间)")
    res_img = requests.get(url=get_img_url, headers=headers, params=timestamp).content
    file_path = './a.png'
    with open(file_path, 'wb') as f:
        f.write(res_img)
    return file_path


'''改变图片的色系'''


def _change_img(image_data):
    width, height = image_data.size
    white = (255, 255, 255)
    im_new = Image.new(image_data.mode, image_data.size, white)
    for w in range(1, width - 1):
        for h in range(1, height - 1):
            color = image_data.getpixel((w, h))
            if sum(color) < 360:
                c1 = image_data.getpixel((w - 1, h))
                c2 = image_data.getpixel((w + 1, h))
                c3 = image_data.getpixel((w, h - 1))
                c4 = image_data.getpixel((w, h + 1))
                rule = lambda item: sum(item) < 610
                if all(map(rule, (c1, c2, c3, c4))):
                    im_new.putpixel((w, h), color)
    im_new.save(r'./b.png')
    return im_new


'''图片转换成黑白模式'''


def _processing_image(image_data):
    image_obj = image_data  # Image.open(r'E:\\bb.png')
    img = image_obj.convert("L")  # 转灰度
    table = []
    threshold = 120
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
        # 参照这个表进行二值化
    img = img.point(table, '1')
    img.save(r'./c.png')
    return img


'''去除图片干扰点'''


def _delete_spot(images):
    # images = self._processing_image(image_data)
    data = images.getdata()
    w, h = images.size
    black_point = 0
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            mid_pixel = data[w * y + x]  # 中央像素点像素值
            if mid_pixel < 200:  # 找出上下左右四个方向像素点像素值
                top_pixel = data[w * (y - 1) + x]
                left_pixel = data[w * y + (x - 1)]
                down_pixel = data[w * (y + 1) + x]
                right_pixel = data[w * y + (x + 1)]
                # 判断上下左右的黑色像素点总个数
                if top_pixel < 10:
                    black_point += 1
                if left_pixel < 10:
                    black_point += 1
                if down_pixel < 10:
                    black_point += 1
                if right_pixel < 10:
                    black_point += 1
                if black_point < 1:
                    images.putpixel((x, y), 255)
                black_point = 0
    # images.show()
    images.save(r'./d.png')
    return images


'''识别图片内容'''


def _get_captcha(image_data):
    im = _change_img(image_data)
    im = _processing_image(im)  # Image.open(r'E:\\cc.png')
    # im = _delete_spot(im)
    text = pytesseract.image_to_string(im)
    rep = {'\\': '', ' ': ''}
    p = re.compile(r'[—,‘_§{."$(#+&*¥~!@%:;/<>«»|)]')
    text = re.sub(p, '', text)
    for r in rep:
        text = text.replace(r, rep[r])
    text = text.strip()
    return text


if __name__ == '__main__':
    # im = _get_picture()#"./a.png"  #
    # captcha = _get_captcha(Image.open(im))
    # print(captcha)
    #     login_url = "http://47.97.43.115:8082/aj_healthcloud/login/verify"
    #     while True:
    #         captcha = _get_captcha(Image.open(_get_picture()))
    #         if len(captcha) == 4:
    #             login_data = {
    #                 "usercode": "platAdmin",
    #                 "password": "admin123",
    #                 "captcha": captcha
    #             }
    #             res_login = requests.post(url=login_url, data=json.dumps(login_data), headers=headers).json()
    #             if res_login and res_login['n']:
    #                 os.remove('./a.png')
    #                 login_token = res_login['n']["token"]
    #                 headers["X-Token"] = login_token
    #                 break
    #
    # print(headers)

    # print(r.text)  # 返回对象，unicode类型（主要取文本）
    # print(r.content)  # 返回对象，bytes类型（二进制的数据，取图片和文件等，中文显示为字符）
    # print(r.json())  # 返回对象，json类型
    # print(r.status_code)  # 响应状态码
    # print(r.reason)  # 状态原因
    # print(r.cookies)  # 返回cookies
    # print(r.encoding)  # 返回对象，bytes类型（二进制的数据，取图片和文件等，中文显示为字符）
    # print(r.request.headers)  # 返回请求消息的报头
    # print(r.url)  # 最终的url
    # print(r.headers)  # 以字典对象存储服务器响应头，若键不存在则返回None
    # print(r.history)  #
    # print(r.raw)  # 返回原始响应体
    # print(r.raise_for_status())  # 失败请求（非200）抛出异常
    login_data = {"usercode": "platAdmin", "password": "admin123", "captcha": ""}
    login_data.values()
