import os
import MaxPlus
import thread

maxFileDirectory = r"F:\Share\原始模型\融鼎轩"
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


def exportObj():
    for i in findSpecifiedFile(maxFileDirectory, suffix='.max'):
        print(i)
        fm.Open(i)
        fm.Export(os.path.join(objfile, os.path.basename(i).replace('max', 'obj')), True)


exportObj()