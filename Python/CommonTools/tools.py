# coding=utf-8
import os
import shutil

# def findSpecifiedFile(path, suffix=''):
#     _a = []
#     for fileName in os.listdir(path):
#         pathName = os.path.join(path, fileName)
#         if os.path.isfile(pathName):
#             if pathName.endswith(suffix):
#                 _a.append(pathName)
#         else:
#            _a.extend(findSpecifiedFile(pathName,suffix))
#     return _a

path = r'C:\Users\HYC\Documents\MyCode'


def findSpecifiedFile(path, surffix=''):
    _file = []
    for root, dirs, fils in os.walk(path):
        for file in fils:
            if file.endswith(surffix):
                _file.append(file)
    return _file

def copyfile(files,path,nummber=1)
    for file in files:
        shutil.copyfile()