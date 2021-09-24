#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'RaoPQ'

import xlrd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class ReadExcel:
    """读取excel文件数据"""

    def __init__(self, file_name, sheet_name=None):
        self.data = xlrd.open_workbook(filename=file_name)
        if sheet_name is None:
            self.table = self.data.sheets()[0]
        else:
            self.table = self.data.sheet_by_name(sheet_name)

        self.n_rows = self.table.nrows  # 获取总行数
        self.n_cols = self.table.ncols  # 获取总列数

    def read_data(self):
        if self.n_rows > 1:
            # 获取第一行的内容，列表格式
            keys = self.table.row_values(0)
            listApiData = []
            # 获取每一行的内容，列表格式
            for col in range(1, self.n_rows):
                values = self.table.row_values(col)
                # keys，values组合转换为字典
                api_dict = dict(zip(keys, values))
                listApiData.append(api_dict)

            return listApiData
        else:
            print("表格是空数据!")
            return None

    def read_row(self, row):
        if self.n_rows > 1:
            keys = self.table.row_values(0)  # 获取第一行的内容，列表格式
            values = self.table.row_values(row)
            api_dict = dict(zip(keys, values))  # keys，values组合转换为字典
            return api_dict
        else:
            print("表格是空数据!")
            return None


# class ReadExcel_T:
#     """读取excel文件数据"""
#
#     def __init__(self, file_name, sheet_name="Sheet1"):
#         self.data = openpyxl.load_workbook(file_name)
#         self.sheet = self.data[sheet_name]
#
#         '''最大列数、行数'''
#         # self.sheet.max_column  # 最大列数
#         # self.sheet.max_row  # 最大行数
#
#         '''读取每行数据'''
#         # for row in self.sheet.iter_rows():
#         #     row_data = [cell.value for cell in row]
#         #     print(row_data)
#
#         '''读取所有数据'''
#         # print(list(self.sheet.values))  # sheet.values 生成器
#
#         '''读取单元格数据'''
#         # print(self.sheet['A1'].value)
#         # print(self.sheet.cell(1, 1).value)  # 索引从1开始
#
#     def read_data(self):
#         if self.sheet.max_row > 1:
#             keys = list(self.sheet.values)[0]  # 获取第一行的内容
#             listApiData = []
#             # 获取每一行的内容，列表格式
#
#             for row in self.sheet.iter_rows(min_row=2):
#                 values = []
#                 for cell in row:
#                     if cell.value is None:
#                         cell.value = ''
#                     values.append(cell.value)
#                 # values = [cell.value for cell in row if cell.value is None ]
#                 # print('^^^^',values)
#                 api_dict = dict(zip(keys, values))  # keys，values组合转换为字典
#                 listApiData.append(api_dict)
#             return listApiData
#         else:
#             print("表格是空数据!")
#             return None
#
#     def read_row(self, row):
#         if self.sheet.max_row > row:
#             keys = list(self.sheet.values)[0]  # 获取第一行的内容，列表格式
#             values = list(self.sheet.values)[row + 1]
#             api_dict = dict(zip(keys, values))  # keys，values组合转换为字典
#             return api_dict
#         else:
#             print("超过最大行!")
#             return None


if __name__ == '__main__':
    re = ReadExcel(r'C:\Users\goocan\Desktop\pythonProject\DemoHealthCloud\database\DemoAPITestCase.xlsx', "健康云")
    # print(re.read_row(7))
    # for k,v in re.read_row(7).items():
    #     print(v)
    for _d in re.read_data():
        if _d['ID'] == "login":
            if 'captcha' in eval(_d['body']):
                print('captcha' in eval(_d['body']))
    # print(re.read_data()[0]["ID"] == "login")
