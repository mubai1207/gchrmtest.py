import re
from os.path import splitext

import pytesseract
from PIL import Image


def del_noise(im):
    width, height = im.size
    white = (255, 255, 255)
    im_new = Image.new(im.mode, im.size, white)
    for w in range(1, width - 1):
        for h in range(1, height - 1):
            color = im.getpixel((w, h))
            if sum(color) < 600:
                c1 = im.getpixel((w - 1, h))
                c2 = im.getpixel((w + 1, h))
                c3 = im.getpixel((w, h - 1))
                c4 = im.getpixel((w, h + 1))
                rule = lambda item: sum(item) < 660
                if all(map(rule, (c1, c2, c3, c4))):
                    im_new.putpixel((w, h), color)
    return im_new


def deal_code_image(file_name):
    # image = Image.open(file_name)
    # # image.show() #查看处理前的图片
    # # 处理图片去除干扰
    # # 将图片转化为灰度图像
    # image = image.convert('L')
    #
    # threshold = 120  # 设置临界值，临界值可调试
    # table = []
    # for i in range(256):
    #     if i < threshold:
    #         table.append(0)
    #     else:
    #         table.append(1)
    #
    # image = image.point(table, '1')
    # image.save(r'./b.png')
    image_obj = Image.open(file_name)  # Image.open(r'E:\\bb.png')
    img = image_obj.convert("L")  # 转灰度
    pix_data = img.load()
    w, h = img.size
    threshold = 120
    for y in range(h):
        for x in range(w):
            if pix_data[x, y] < threshold:
                pix_data[x, y] = 0
            else:
                pix_data[x, y] = 250
    img.save(r'./b.png')
    # return img

    res = pytesseract.image_to_string(img)

    rep = {'\\': '', '-': '', ' ': '', }
    p = re.compile(r'[—,_$"()#+&*¥~!@%:;/<>|]')
    res = re.sub(p, '', res)
    for r in rep:
        text = res.replace(r, rep[r])
    res = res.strip()
    # res = res.replace(" ", "")  # 去除结果中的空格
    print(res)
    return res


if __name__ == '__main__':
    fn = r'./a.png'
    im = Image.open(fn)
    im = del_noise(im)
    im.save('_new'.join(splitext(fn)))
    deal_code_image(r'./a_new.png')
