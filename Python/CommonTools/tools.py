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

path = r'C:\Users\Intime\Documents\MyCode'
tpath = r'F:\Share\HSM\1分类\餐桌\简明式餐椅'

def findSpecifiedFile(path, suffix=''):
    '''
    查找指定文件
    :param path: 根目录
    :param suffix: 格式，默认是空
    :return: 文件地址列表
    '''
    _file = []
    path = path.decode('utf-8')
    for root, dirs, fils in os.walk(path):
        for file in fils:
            if file.endswith(suffix):
                _file.append(os.path.join(root,file))
    return _file

def copyfile(files,path=None,nummber=1):
    if path:
        for file in files:
            shutil.copy(file,path)
    if path is None:
        for i in range(nummber):
            for file in files:
                suffix=file.split('.')[1]
                newFile=file.split('.')[0]+'_%s.' %i +suffix
                print newFile
                shutil.copyfile(file,newFile)

a = findSpecifiedFile(tpath,'.max')
print a[0]