# _*_ coding:utf-8 _*_

import datetime
from DemoGChrm.lib.getTime import *


def getCert(cert_number):
    year = cert_number[6:10]
    month = cert_number[10:12]
    day = cert_number[12:14]
    sex = cert_number[16:17]
    sex = int(sex)
    if sex % 2:
        sex_value = 32
    else:
        sex_value = 280

    birth_d = datetime.datetime.strptime(cert_number[6:14], "%Y%m%d")
    today_d = datetime.datetime.now()
    birth_t = birth_d.replace(year=today_d.year)
    if today_d > birth_t:
        age = today_d.year - birth_d.year
    else:
        age = today_d.year - birth_d.year - 1

    birth_time = "%s-%s-%s" % (year, month, day)
    birth_month = "%s-%s" % (month, day)
    return birth_month, birth_time, sex_value, age


if __name__ == '__main__':
    l = getCert(str(632323190605262960))
    print(getTime().get_last_Years(l[1], 20))
