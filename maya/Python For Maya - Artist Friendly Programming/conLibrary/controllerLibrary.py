# coding=utf-8
from maya import cmds
import os
import json
import pprint

USERAPPDIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USERAPPDIR, 'controllerLibrary')


def createDirectory(directory=DIRECTORY):
    '''
    创建路径，如果文件夹不存在，就创建
    :param directory (str): 创建文件夹
    :return:
    '''
    if not os.path.exists(directory):
        os.mkdir(directory)


class ControllerLibrary(dict):

    def save(self, name, directory=DIRECTORY, screenshot=True, **info):

        createDirectory(directory)
        path = os.path.join(directory, '%s.ma' % name)
        infoFile = os.path.join(directory, '%s.json' % name)  # 默认路径下添加json文件路径
        info['name'] = name
        info['path'] = path
        cmds.file(rename=path)  # 重命名

        if cmds.ls(selection=True):
            cmds.file(force=True, type='mayaAscii', exportSelected=True)  # 保存选中的

        else:
            cmds.file(save=True, type='mayaAscii', force=True)  # 保存全部
        if screenshot:
            info['screenshot'] = self.saveScreenshot(name, directory=directory)
        with open(infoFile, 'w') as f:
            # 将相关的信息存入json文件中，用于后面读取
            # with as语法通常用于打开文件 它可以在执行scope代码前打开相关的文件 并在执行后关闭文件
            # info存储相关的dictionary f是filestream indent是缩进字符
            json.dump(info, f, indent=4)

        self[name] = info

    def find(self, directory=DIRECTORY):
        self.clear()
        if not os.path.exists(directory):
            return

        files = os.listdir(directory)
        # 遍历files如果结尾是.ma则存入mayaFiles 列表
        mayaFiles = [f for f in files if f.endswith('.ma')]
        for ma in mayaFiles:
            name, ext = os.path.splitext(ma)
            path = os.path.join(directory, ma)
            infoFIle = '%s.json' % name
            if infoFIle in files:
                infoFIle = os.path.join(directory, infoFIle)
                with open(infoFIle, 'r') as f:
                    info = json.load(f)
            else:
                info = {}
            screenshot = '%s.jpg' % name
            if screenshot in files:
                info['screenshot'] = os.path.join(directory, screenshot)
            info['name'] = name
            info['path'] = path
            self[name] = info

    def load(self, name):
        path = self[name]['path']
        # cmds.file(path, i=True, usingNamespaces=False)

        cmds.file(new=True, force=True)
        cmds.file(path, o=True, force=True)

    def saveScreenshot(self, name, directory=DIRECTORY):
        # 图片保存路径

        path = os.path.join(directory, '%s.jpg' % name)

        cmds.viewFit(f=10.0)  # 聚焦物体
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)  # 设置默认渲染器图片格式 8位jpg
        # 使用playblast 的方式保存截图
        cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=200, height=200,
                       showOrnaments=False, startTime=1, endTime=1, viewer=False)

        return path

