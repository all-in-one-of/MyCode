#!/usr/bin/env python
# coding=utf-8
# Author = 'HYC'
# Time   = '2019/4/6 17:31'

import os
import bpy

def findSpecifiedFile(path, suffix=''):
    _file = []
    for root, dirs, fils in os.walk(path):
        for file in fils:
            if file.endswith(suffix):
                _file.append(os.path.join(root, file))
    return _file

def install(plugins):

    for plugin in plugins:
        try:
            bpy.ops.preferences.addon_install(filepath=plugin)
        except:
            print(os.path.basename(plugin))


dir = r'C:\Users\HYC\Downloads\aaa'
install(findSpecifiedFile(dir,'zip'))