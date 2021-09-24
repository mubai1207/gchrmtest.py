# _*_ coding:utf-8 _*_

import os
import re
import sys
import requests
import pytesseract
import time
import datetime
import json
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Cookie": "JSESSIONID=C7D55669C9628A69F328E2AE53CBD9F8"
}


def _get_picture():
    get_img_url = 'http://tjbb.wsjkw.zj.gov.cn/irpt/esmain/verifycode.do'
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
            if sum(color) < 880:
                c1 = image_data.getpixel((w - 1, h))
                c2 = image_data.getpixel((w + 1, h))
                c3 = image_data.getpixel((w, h - 1))
                c4 = image_data.getpixel((w, h + 1))
                rule = lambda item: sum(item) < 700
                if all(map(rule, (c1, c2, c3, c4))):
                    im_new.putpixel((w, h), color)
    im_new.save(r'./b.png')
    return im_new


'''图片转换成黑白模式'''


def _processing_image(image_data):
    image_obj = image_data  # Image.open(r'E:\\bb.png')
    img = image_obj.convert("L")  # 转灰度
    table = []
    threshold = 80
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
    rep = {'\\': '', ' ': '', '0': '', 'o': '', }
    p = re.compile(r'[—,‘_§{."$(#+&*¥~!@%:;/<>«»|)]')
    text = re.sub(p, '', text)
    for r in rep:
        text = text.replace(r, rep[r])
    text = text.strip()
    return text


if __name__ == '__main__':

    login_url = 'http://tjbb.wsjkw.zj.gov.cn/irpt/esmain/js/login.do'
    _loginData = ''
    while not _loginData:
        im = _get_picture()  # './a.png'#
        text = _get_captcha(Image.open(im))
        if len(text) == 4:
            print(text)
            login_Data = {
                "action": "login",
                "pw": "{f3f52617d64395fd421c8087a142d41b}",
                "pwdstrength": 3,
                "pwdlength": 14,
                "MAC": "",
                "imgtext": text,
                "__t__": str(int((time.time() * 1000)))
            }
            res_login = requests.post(url=login_url, data=json.dumps(login_Data), headers=headers)
            cookies = res_login.cookies
            if cookies:
                print("登录成功！")
                os.remove('./a.png')
                cookie = "JSESSIONID=" + requests.utils.dict_from_cookiejar(cookies)["JSESSIONID"]
                headers["Cookie"] = cookie
                break
# print(headers)

uu = 'http://tjbb.wsjkw.zj.gov.cn/irpt/i18n.do'
data = {
    "action": "getLang",
    "__t__": str(int((time.time() * 1000)))
}
r = requests.post(url=uu, data=data, headers=headers)
print(r.text)  # 返回对象，unicode类型（主要取文本）
