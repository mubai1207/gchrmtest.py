import time
import random
import json

print(time.strftime('%Y-%m-%d'))

print(random.randint(1, 1))

import re

dit = {"message_conetet": "【医院】验证码：576224。5分钟"}
print(re.findall(r'：([0-9]{6,})。', dit["message_conetet"])[0])

headers = '''
accept: application/json, text/javascript, */*; q=0.01
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
content-length: 128
content-type: application/x-www-form-urlencoded
cookie: lockNav=unLocked; shiroJID=6e06a07c-fb2f-489e-951d-695207a43b96
origin: https://bill.xiaofubao.com
referer: https://bill.xiaofubao.com/index?page=/bill/thirdReport/daily
sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"
sec-ch-ua-mobile: ?0
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36
x-requested-with: XMLHttpRequest
'''

# 去除参数头尾的空格并按换行符分割
headers = headers.strip().split('\n')

# 使用字典生成式将参数切片重组，并去掉空格，处理带协议头中的://
headers = {x.split(':')[0].strip(): (''.join(x.split(':')[1:])).strip().replace('//', "://") for x in headers}
print(headers)
# 使用json模块将字典转化成json格式打印出来
print(json.dumps(headers, indent=1))
