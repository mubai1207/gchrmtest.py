# _*_ coding:utf-8 _*_
import logging
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from DemoLife_API.config import setting
import colorlog

# 日志存放文件夹，如不存在，则自动创建一个logs目录
if not os.path.exists(setting.LOG_DIR):
    os.mkdir(setting.LOG_DIR)

log_colors_config = {
    'DEBUG': 'white',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
}


class Log(object):
    """封装后的logging"""

    def __init__(self, logger=None):
        """
            指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        """

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        self.log_name = os.path.join(setting.LOG_DIR, '%s.log' % time.strftime('%Y-%m-%d %H_%M_%S'))
        self.logger.handlers = []  # 因为多出调用logger会生成多个handlers（重复输出log）,所以每次调用清空handler
        fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')
        fh.setLevel(logging.INFO)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s]-[%(filename)s|%(funcName)s]-[line|%(lineno)d]-%(levelname)-8s: %(message)s')
        formatter_colorlog = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]: %(message)s',
            log_colors=log_colors_config)
        fh.setFormatter(formatter)
        ch.setFormatter(formatter_colorlog)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        fh.close()
        ch.close()

    def getLog(self):
        return self.logger
