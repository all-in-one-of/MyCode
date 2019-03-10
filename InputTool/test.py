# -*- encoding: utf-8 -*-
"""
@File    : test.py
@Time    : 2019/3/6 19:35
@Author  : Intime
@Software: PyCharm
"""
import time
import datetime
import os
from usual import changeTime
startTime = time.time()
print(datetime.datetime.now())

os.system(r'SimplygonBatch --Input F:\Share\simplygon\inputDir --Output F:\Share\simplygon\outputDir --Spl F:\Share\simplygon\splDir --Temp F:\Share\simplygon\temp --Verbose --OutputFileFormat .fbx')
endTime = time.time()
print('用时',changeTime(endTime-startTime))
print(datetime.datetime.now())
