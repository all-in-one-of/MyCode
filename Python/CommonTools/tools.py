# coding=utf-8
import json
import math
import os
import shutil
import datetime
import time
import numpy
import cv2
import name
from win32gui import *
import win32gui
import win32con
from time import sleep
from pykeyboard import PyKeyboard


# 529478

def get_all_hwnd(hwnd,mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})




def foo(hwnd, mouse):
    titles = set()

    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        # 判断是不是窗口、是不是可用的、是不是可见的
        a = win32gui.GetWindowText(hwnd)
        if a and 'Program Manager' not in a and '管理员' not in a:
            print(a)
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    titles.add(GetWindowText(hwnd))


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


def copyfile(files, path=None, nummber=1):
    """
    复制文件
    :param files: 文件列表
    :param path: 目标文件夹
    :param nummber: 复制次数
    :return:
    """
    if type(files) is list and path:
        for file in files:
            shutil.copy(file, path)
    elif type(files) is str and path:
        shutil.copy(files, path)
    elif path is None:
        for i in range(nummber):
            for file in files:
                suffix = file.split('.')[1]
                newFile = file.split('.')[0] + '_%s.' % i + suffix
                shutil.copyfile(file, newFile)


def createDirectory(directory):
    '''
    创建路径，如果文件夹不存在，就创建
    :param directory (str): 创建文件夹
    :return:
    '''
    if not os.path.exists(directory):
        os.mkdir(directory)


def readJson(path):
    """
    读取json
    :param path: json文件
    :return: 字典
    """
    with open(path, 'r') as f:
        info = json.load(f)  # 导入json文件
        b = json.dumps(info, encoding="utf-8", ensure_ascii=False)  # 转码成字符串
        c = eval(b)  # 转回字典
    return c  # 返回字典


def changeTime(allTime):
    day = 24 * 60 * 60
    hour = 60 * 60
    min = 60
    if allTime < 60:
        return "%d sec" % math.ceil(allTime)
    elif allTime > day:
        days = divmod(allTime, day)
        return "%d days, %s" % (int(days[0]), changeTime(days[1]))
    elif allTime > hour:
        hours = divmod(allTime, hour)
        return '%d hours, %s' % (int(hours[0]), changeTime(hours[1]))
    else:
        mins = divmod(allTime, min)
        return "%d mins, %d sec" % (int(mins[0]), math.ceil(mins[1]))


def loadDatadet(infile):
    with open(infile, 'r', encoding='utf-8') as f:
        sourceInLine = f.readlines()
        dataset = []
        for line in sourceInLine:
            temp1 = line.strip('\n')
            temp2 = temp1.split('\t')
            dataset.append(temp2)
        return dataset


if __name__ == '__main__':
    num = 0
    mun = 0
    path = r'F:\Share\2018\rdx'

    tex = {}
    for n in os.listdir(path):
        gg = ['收藏级', '优等级', '实用级', '一等级']
        info = {}
        version_info = {}

        model = {}
        mesh = {}
        md = {}
        num = 0
        mun = 0
        directory = os.path.join(path, n)

        if os.path.isdir(directory):
            json_file = os.path.join(directory, '%s.json' % n)

            tex['baseColor'] = os.path.join(directory, [i for i in os.listdir(directory) if
                                                        i.endswith('Diffuse.png') or i.endswith('_b.png')][0])
            tex['normals'] = os.path.join(directory, [i for i in os.listdir(directory) if
                                                      i.endswith('Normals.png') or i.endswith('_n.png')][0])
            tex['ambientOcclusion'] = os.path.join(directory, [i for i in os.listdir(directory) if
                                                               i.endswith('AmbientOcclusion.png') or i.endswith(
                                                                   '_ao.png')][0])
            tex['shadow'] = os.path.join(directory, [i for i in os.listdir(directory) if i.endswith('_s.png')][0])

            tex['metallic'] = os.path.join(directory,
                                           [i for i in os.listdir(directory) if i.endswith('_m.png')][0]) if [i for i in
                                                                                                              os.listdir(
                                                                                                                  directory)
                                                                                                              if
                                                                                                              i.endswith(
                                                                                                                  '_m.png')] else ''
            tex['roughness'] = os.path.join(directory,
                                            [i for i in os.listdir(directory) if i.endswith('_r.png')][0]) if [i for i
                                                                                                               in
                                                                                                               os.listdir(
                                                                                                                   directory)
                                                                                                               if
                                                                                                               i.endswith(
                                                                                                                   '_r.png')] else ''
            tex['emissive'] = os.path.join(directory,
                                           [i for i in os.listdir(directory) if i.endswith('_e.png')][0]) if [i for i in
                                                                                                              os.listdir(
                                                                                                                  directory)
                                                                                                              if
                                                                                                              i.endswith(
                                                                                                                  '_e.png')] else ''

            mesh['maya文件地址'] = ''
            mesh['fbx文件地址'] = os.path.join(directory, [i for i in os.listdir(directory) if i.endswith('.fbx')][0])
            mesh['价格'] = 0
            mesh['sku'] = ''
            mesh['渲染图片地址'] = os.path.join(directory, [i for i in os.listdir(directory) if i.endswith('.jpg')][0])
            mesh['贴图地址'] = tex


            # version_info['MD5码'] = ''
            # version_info['提交时间'] = ''
            # version_info['note'] = ''
            md['提交时间'] = ''
            md['note'] = ''
            md['材质包地址'] = ''
            md['MD5码'] = ''

            for i in [i for i in os.listdir(directory) if i.endswith('manifest') and i.startswith('m') is False]:
                version_info['模型'] = mesh
                md[gg[num]] = version_info
                md[gg[num]]['模型包地址'] = i
                md.update(md)
                num += 1




            model['finally'] = md

            info['sku'] = n
            info['商品名称'] = name.name[n]
            info['副标题'] = ''
            info['价格'] = 0
            info['所属商家'] = '荣鼎轩红木'
            info['所属品牌'] = '荣鼎轩'
            info['所属分类'] = '客厅'
            info['所属系列'] = ''
            info['商品图片地址'] = os.path.join(directory, '%s.jpg' % n)
            info['所属套装'] = ''
            info['商品长宽高'] = ''
            info['3dMax地址'] = ''
            info['是否有金属配件'] = ''
            info['是否有发光配件'] = ''
            info['备注'] = ''
            info['制作类型'] = '普通类型'
            info['对接人'] = '王'
            info['制作人'] = '何'
            info['审核人'] = '韩'
            info['录入时间'] = ''
            info['开始制作时间'] = ''
            info['参考图地址'] = ''
            info['obj文件地址'] = ''
            info['规格'] = model

            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(info, f, indent=2, ensure_ascii=False)

            # with open(json_file, 'r+', encoding='utf-8') as f:
            #     j = 0
            #     info = json.load(f)
            #     for i in gg:
            #
            #         info['规格']['finally'][i]['模型']['模型包地址'] = os.path.join(directory,
            #                                                                [i for i in os.listdir(directory) if
            #                                                                 i.endswith('.manifest') and i.startswith(
            #                                                                     'm') is False][j].split('.')[0])
            #         info['规格']['finally'][i]['模型']['sku'] = \
            #         [i for i in os.listdir(directory) if i.endswith('.manifest') and i.startswith('m') is False][
            #             j].split('.')[0]
            #         info['规格']['finally']['MD5码'] = loadDatadet(
            #             r"F:\Share\2018\rdx\%s\%s.manifest" % (info['sku'], info['规格']['finally'][i]['模型']['sku']))[5][
            #             0].split(' ')[5]
            #         info['规格']['finally']['材质包地址'] = os.path.join(directory, [i for i in os.listdir(directory) if
            #                                                                      i.startswith('m') and i.endswith(
            #                                                                          '.manifest') is False][0])
            #         j += 1
            #
            # with open(json_file, 'w', encoding='utf-8') as f:
            #     json.dump(info, f, indent=2, ensure_ascii=False)
            print(n)
            break
        else:
            print('lala---------%s' % n)


# if __name__ == '__main__':
#     kk = PyKeyboard()
#
#     while True:
#         hwnd_title = {}
#
#         win32gui.EnumWindows(get_all_hwnd, 0)
#
#         for h, t in hwnd_title.items():
#             if t == "缺少外部文件":
#                 win32gui.PostMessage(h, win32con.WM_CLOSE, 0, 0)
#                 print(t)
#             elif t == "文件加载: Gamma 和 LUT 设置不匹配":
#                 win32gui.SetForegroundWindow(h)
#                 # win32gui.PostMessage(h, win32con.WM_CLOSE, 0, 0)
#                 kk.tap_key(kk.enter_key)
#                 time.sleep(1)
#
#             elif t == "文件加载: 单位不匹配":
#                 # win32gui.PostMessage(h, win32con.WM_CLOSE, 0, 0)
#                 win32gui.SetForegroundWindow(h)
#                 kk.tap_key(kk.enter_key)
#                 time.sleep(1)
#
#             elif t == "V-Ray 警告":
#                 win32gui.SetForegroundWindow(h)
#                 kk.tap_key(kk.enter_key)
#                 time.sleep(1)
#
#                 # win32gui.PostMessage(h, win32con.WM_CLOSE, 0, 0)
#
#             print(h, t)
#
#         time.sleep(1)
