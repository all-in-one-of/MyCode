# -*- encoding: utf-8 -*-
"""
@File    : readExcel.py
@Time    : 2019/4/3 10:41
@Author  : Intime
@Software: PyCharm
"""
from openpyxl import load_workbook
from IntimeTool.usual import *

wb = load_workbook(r"F:\Share\原始模型\高居明作\高居明作 信息完成.xlsx")

ws = wb['Sheet1']
# c = ws.cell(row=x, column=y)

a = []
b = []
c = []
for i in ws.values:
    if i[-1] is 1:
        a.append(i)
    elif i[-1] is 2:
        b.append(i)
    else:
        c.append(i)

d = {}
d['Done']=a
d['Undone']=b
d['Wait']=c

writeJson(r'F:\Share\原始模型\高居明作\gjmz.json',d)