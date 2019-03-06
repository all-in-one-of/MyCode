# -*- encoding: utf-8 -*-
"""
@File    : test.py
@Time    : 2019/3/6 19:35
@Author  : Intime
@Software: PyCharm
"""
import time
import json

from usual import *
a = readJson(r"F:\Share\goods\yingtaikeji\00000000\00000000.json")
t1 = a['inputTime']

t2 = time.time()

print(changeTime(t2-t1))