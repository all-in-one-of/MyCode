#!/usr/bin/env python
# coding=utf-8
# Author = 'HYC'
# Time   = '2019/4/3 23:49'
import assetFunctions
reload(assetFunctions)
from assetFunctions import *
import os
female = os.path.join(os.path.expanduser('~/Desktop'), 'female.fbx')

t1 = r"C:\Users\HYC\Desktop\-a2.jpg"

def run():
    a1 = buildImportTask(t1,'/game/images')
    a2 = buildImportTask(female,'/game/fbx')
    executeImportTask([a1,a2])

if __name__ == '__main__':
    run()