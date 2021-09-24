# _*_ coding:utf-8 _*_

import time, datetime


class getTime:
    now_time = datetime.datetime.now()
    t = time.time()

    def get_Daytime(self, days=0):
        """
        :param days: 需要获取的天数，正数往后、负数往前
        :return: 返回天数
        """
        return (self.now_time + datetime.timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")  # 获取后一天

    def get_Hourstime(self, hours=0):
        """
        :param hours: 需要获取的小时，正数往后、负数往前
        :return: 返回时间
        """
        return (self.now_time + datetime.timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")  # 获取前一小时

    def get_Time(self):
        """
        :return: 毫秒级时间戳
        """
        return int(round(self.t * 1000))

    def get_last_Years(self, year, lastyear):
        times = datetime.datetime.strptime(str(year), "%Y-%m-%d")
        last_year = "%s-%s" % (times.year + lastyear, year.split("-")[1])
        return last_year


if __name__ == '__main__':
    print(getTime().get_Daytime(30))

