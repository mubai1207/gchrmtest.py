# _*_ coding:utf-8 _*_
import configparser
import json
import os
import re
import sys
import requests
import pytesseract
import time
from PIL import Image
from DemoHealthCloud.lib.log import Log
from DemoHealthCloud.config import setting

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

log = Log().getLog()

cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='UTF-8')

headers = eval(cf.get('headers', 'HEADERS-Chrome'))


class Login:

    def __init__(self, login_PATH, login_data=None):
        values = list(eval(login_data).values())  # {"usercode": "platAdmin", "password": "admin123", "captcha": ""}
        log.debug("登录环境--->{0}".format(login_PATH))
        self.ss = requests
        self.login_name = values[0]
        self.pwd = values[1]
        self.headers = headers
        self.health_cloud = cf.get(login_PATH, "health_cloud")

    '''获取图片'''

    def _get_picture(self):
        img_url = self.health_cloud + "/aj_healthcloud/login/captcha?timestamp=" + str(int((time.time() * 1000)))
        res_img = self.ss.get(url=img_url, headers=self.headers).content
        file_path = './a.png'
        with open(file_path, 'wb') as f:
            f.write(res_img)
        log.debug("成功获取验证码图片")
        return file_path

    '''改变图片的色系'''

    def _change_img(self, image_data):
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
        # im_new.save(r'./b.png')
        log.debug("改变图片的色系")
        return im_new

    '''图片转换成黑白模式'''

    def _processing_image(self, image_data):
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
        # img.save(r'./c.png')
        log.debug("图片转换成黑白模式")
        return img

    '''去除图片干扰点'''

    def _delete_spot(self, images):
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
        # images.save(r'./d.png')
        return images

    '''识别图片内容'''

    def _get_captcha(self, image_data):
        im = self._change_img(image_data)
        im = self._processing_image(im)  # Image.open(r'E:\\cc.png')
        # im = self._delete_spot(im)
        text = pytesseract.image_to_string(im)
        rep = {'\\': '', ' ': '', '0': 'o', }
        p = re.compile(r'[—,‘_§{."$(#+&*¥~!@%:;/<>«»|)]')
        text = re.sub(p, '', text)
        for r in rep:
            text = text.replace(r, rep[r])
        text = text.strip()
        log.debug("识别图片内容->{0}".format(text))
        return text

    def login(self):
        login_url = self.health_cloud + "/aj_healthcloud/login/verify"
        reponse_login = None
        _loginData = ''
        while not _loginData:
            captcha = self._get_captcha(Image.open(self._get_picture()))
            if len(captcha) == 4:
                login_data = {
                    "usercode": self.login_name,
                    "password": self.pwd,
                    "captcha": captcha
                }
                reponse_login = self.ss.post(url=login_url, data=json.dumps(login_data), headers=self.headers)
                res_login = reponse_login.json()
                if res_login and res_login['n']:
                    log.info('登录成功了，返回的登录信息->{0}'.format(res_login))
                    os.remove('./a.png')
                    login_token = res_login['n']["token"]
                    log.info('返回登录信息token')
                    self.headers["X-Token"] = login_token
                    with open(setting.TOKEN_FILE, 'w', encoding='utf8')as fp:
                        json.dump(self.headers, fp, ensure_ascii=False)
                    break
        return reponse_login


def login_main(login_name, pwd, path):
    return Login(login_PATH=path).login()


if __name__ == '__main__':
    login_ = login_main("platAdmin", 'admin123', path='test')
    print(login_.headers)
    print(login_.request.headers)
