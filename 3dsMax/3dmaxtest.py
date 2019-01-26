import os

import MaxPlus

maxFile=r"F:\Share\HSM\1分类\餐桌"
objfile = r'D:\aaaa'

fm = MaxPlus.FileManager


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
                _file.append(os.path.join(root, file))
    return _file





q = 1
for i in findSpecifiedFile(maxFile,suffix='.max'):

    print(i)
    fm.Open(i)
    fm.Export(os.path.join(objfile,'a%s.obj'% q),True)
    q+=1

