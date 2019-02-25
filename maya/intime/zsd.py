# coding=utf-8
# from Qt import QtWidgets,QtCore,QtGui
from PySide2 import QtWidgets, QtCore, QtGui
import pymel.core as pm
from functools import partial
import os
import json
import time
from maya import OpenMayaUI as omui
import logging

# 初始化logging系统
logging.basicConfig()
# 设置名称 可以针对当前工具进行记录
logger = logging.getLogger('LightingManager')
# 设置信息反馈的模式
logger.setLevel(logging.DEBUG)

import Qt

# 识别当前的使用的Qt库 从而导入正确的库
if Qt.__binding__.startswith('PyQt'):
    logger.debug('Using sip')
    from sip import wrapinstance as wrapInstance
    from Qt.QtCore import pyqtSignal as Signal
elif Qt.__binding__ == 'PySide':
    logger.debug('Using shiboken')
    from shiboken import wrapInstance
    from Qt.QtCore import Signal
else:
    logger.debug('Using shiboken2')
    from shiboken2 import wrapInstance
    from Qt.QtCore import Signal


# 获取Maya的主窗口 用于 dock 窗口
def getMayaMainWindow():
    # 通过OpenMayaUI API 获取Maya主窗口
    win = omui.MQtUtil_mainWindow()
    # 将窗口转换成Python可以识别的东西 这里是将它转换为QMainWindow
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    return ptr


def getDock(name='LightingManagerDock'):
    # 首先删除重名的窗口
    deleteDock(name)
    # 生成可以dock的Maya窗口
    # dockToMainWindow 将窗口dock进右侧的窗口栏中
    # label 设置标签名称
    ctrl = pm.workspaceControl(name, dockToMainWindow=('right', 1), label="Lighting Manager")
    # 通过OpenMayaUI API 获取窗口相关的 Qt 信息
    qtCtrl = omui.MQtUtil_findControl(ctrl)
    # 将 qtCtrl 转换为Python可以识别的形式
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)
    return ptr


def deleteDock(name='LightingManagerDock'):
    # 查询窗口是否存在
    if pm.workspaceControl(name, query=True, exists=True):
        # 存在即删除
        pm.deleteUI(name)


class LightManager(QtWidgets.QWidget):
    # 用来显示下拉菜单
    lightTypes = {
        "Point Light": pm.pointLight,
        "Spot Light": pm.spotLight,
        "Direction Light": pm.directionalLight,
        # partial 类似于 lambda 函数
        # 可以将 partial 转换为函数的形式
        # def createAreaLight(self):
        #     pm.shadingNode('areaLight', asLight=True)
        # partial 和 lambda 的区别在于 lambda 的运行传入参数 partial是创建传入
        "Area Light": partial(pm.shadingNode, 'areaLight', asLight=True),
        "Volume Light": partial(pm.shadingNode, 'volumeLight', asLight=True),
    }

    def __init__(self, dock=True):
        # parent = getMayaMainWindow()
        # 如果设置 dock 窗口 执行 getdock 函数
        if dock:
            parent = getDock()
        else:
            # 删除dock窗口
            deleteDock()

            try:
                # 删除窗口 如果窗口本身不存在 用try可以让代码不会停止运行并报错
                pm.deleteUI('lightingManager')

            except:
                logger.debug('No previous UI exists')

            # 获取Maya主窗口 并将窗口负载在Qt窗口上
            parent = QtWidgets.QDialog(parent=getMayaMainWindow())
            # 设置名称 可以在后面找到它
            parent.setObjectName('lightingManager')
            parent.setWindowTitle('Lighting Manager')
            layout = QtWidgets.QVBoxLayout(parent)

        # 执行父对象，并且设置parent
        super(LightManager, self).__init__(parent=parent)
        self.buildUI()
        self.populate()

        # 将自己添加到父对象中
        self.parent().layout().addWidget(self)

        # 如果没有dock窗口 则显示窗口
        if not dock:
            parent.show()

    def populate(self):
        # count() 获取 scrollLayout 的 item 个数
        while self.scrollLayout.count():
            # 获取 scrollLayout 第一个元素
            widget = self.scrollLayout.takeAt(0).widget()
            if widget:
                # 隐藏元素
                widget.setVisible(False)
                # 删除元素
                widget.deleteLater()

        # 循环场景中所有的灯光元素
        for light in pm.ls(type=["areaLight", "spotLight", "pointLight", "directionalLight", "volumeLight"]):
            # 添加相关的灯光
            self.addLight(light)

    def buildUI(self):
        # 创建 QGridLayout 可以快速将元素添加到网格位置中
        layout = QtWidgets.QGridLayout(self)

        # QComboBox 为下拉菜单
        self.lightTypeCB = QtWidgets.QComboBox()
        # 将 lightTypes 的元素添加到 QComboBox 中
        for lightType in sorted(self.lightTypes):
            self.lightTypeCB.addItem(lightType)

        # 添加到(0,0)的位置 占用1行2列
        layout.addWidget(self.lightTypeCB, 0, 0, 1, 2)

        # 创建按钮
        createBtn = QtWidgets.QPushButton('Create')
        createBtn.clicked.connect(self.createLight)
        layout.addWidget(createBtn, 0, 2)

        # 滚动用的组件
        scrollWidget = QtWidgets.QWidget()
        # 设置滚动组件固定大小
        scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        # 横向排布
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)

        # 滚动区域
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        layout.addWidget(scrollArea, 1, 0, 1, 3)

        # 保存按钮
        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.saveLights)
        layout.addWidget(saveBtn, 2, 0)

        # 导入按钮
        importBtn = QtWidgets.QPushButton('Import')
        importBtn.clicked.connect(self.importLights)
        layout.addWidget(importBtn, 2, 1)

        # 刷新按钮
        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)
        layout.addWidget(refreshBtn, 2, 2)

    def saveLights(self):
        # 将数据保存为 json

        properties = {}

        # 寻找 LightWidget 类的对象
        for lightWidget in self.findChildren(LightWidget):
            # 获取灯光的Transform节点
            light = lightWidget.light
            transform = light.getTransform()

            # 将相关的数据存入 properties 变量中
            properties[str(transform)] = {
                'translate': list(transform.translate.get()),
                'rotate': list(transform.rotate.get()),
                'lightType': pm.objectType(light),
                'intensity': light.intensity.get(),
                'color': light.color.get()
            }

        # 获取数据的存储路径
        directory = self.getDirectory()

        # 设置存储文件的名称
        lightFile = os.path.join(directory, 'lightFile_%s.json' % time.strftime('%m%d'))

        # 写入数据
        with open(lightFile, 'w') as f:
            json.dump(properties, f, indent=4)

        logger.info('Saving file to %s' % lightFile)

    def getDirectory(self):
        # 获取文件保存路径
        directory = os.path.join(pm.internalVar(userAppDir=True), 'lightManager')
        if not os.path.exists(directory):
            os.mkdir(directory)
        return directory

    # json数据的保存格式
    # {
    #     "pointLight1": {
    #         "color": [
    #             1.0,
    #             1.0,
    #             1.0
    #         ],
    #         "intensity": 1.0,
    #         "translate": [
    #             0.0,
    #             7.269212547848552,
    #             0.0
    #         ],
    #         "rotate": [
    #             0.0,
    #             0.0,
    #             0.0
    #         ],
    #         "lightType": "pointLight"
    #     },
    #     "pointLight3": {
    #         "color": [
    #             0.03610000014305115,
    #             0.580299973487854,
    #             0.0
    #         ],
    #         "intensity": 470.0,
    #         "translate": [
    #             10.703503890939462,
    #             17.997132841447666,
    #             0.0
    #         ],
    #         "rotate": [
    #             0.0,
    #             0.0,
    #             0.0
    #         ],
    #         "lightType": "pointLight"
    #     }
    # }
    def importLights(self):
        # 读取 json 数据

        # 获取存储路径
        directory = self.getDirectory()
        # 打开一个获取文件的 file browser 窗口 获取相关的json文件
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "light Browser", directory)

        # 读取 json 数据
        with open(fileName[0], 'r') as f:
            properties = json.load(f)

        # 根据 json 数据处理 生成相关的灯光和属性
        for light, info in properties.items():
            # 获取灯光类型
            lightType = info.get('lightType')
            # 循环遍历灯光类型
            for lt in self.lightTypes:
                # lightTypes 中的类型 需要提取出前半部分与Light结合 进行匹配
                if ('%sLight' % lt.split()[0].lower()) == lightType:
                    break
            else:
                # for 循环 也有else语句 当循环没有被 break 时执行
                logger.info('Cannot find a corresponding light type for %s (%s)' % (light, lightType))
                continue

            # 创建当前lt类型的灯光
            light = self.createLight(lightType=lt)

            # 设置 json 的数据到具体对象中
            light.intensity.set(info.get('intensity'))

            light.color.set(info.get('color'))

            transform = light.getTransform()
            transform.translate.set(info.get('translate'))
            transform.rotate.set(info.get('rotate'))

        # 刷新
        self.populate()

    def createLight(self, lightType=None, add=True):
        # 创建灯光 如果没有类型参数传入 就属于点击创建按钮的情况 获取下拉菜单的类型
        if not lightType:
            lightType = self.lightTypeCB.currentText()

        # 去到 lightTypes 的字典中 找到相关的函数进行调用
        func = self.lightTypes[lightType]

        # 返回灯光的 pymel 对象
        light = func()

        # 添加灯光到滚动区域中
        if add:
            self.addLight(light)

        return light

    def addLight(self, light):
        # 添加滚动区域的组件
        widget = LightWidget(light)
        self.scrollLayout.addWidget(widget)
        # 链接组件的 onSolo Signal 触发 onSolo 方法
        widget.onSolo.connect(self.onSolo)

    def onSolo(self, value):
        # 找到 LightWidget 类的对象
        lightWidgets = self.findChildren(LightWidget)

        # 遍历所有的组件
        for widget in lightWidgets:
            # signal 的数据会通过 sender() 返回
            # 如果返回是 True 则是不需要 disable 的对象
            if widget != self.sender():
                widget.disableLight(value)


class LightWidget(QtWidgets.QWidget):
    # 灯光组件 放置在滚动区域中

    # 注册 onSolo 信号
    onSolo = QtCore.Signal(bool)

    def __init__(self, light):
        super(LightWidget, self).__init__()
        # 如果灯光是字符串 可以将它转换为 pymel 的对象
        if isinstance(light, basestring):
            logger.debug('Converting node to a PyNode')
            light = pm.PyNode(light)

        # 如果获取的是 Transform 节点 就转而获取它的形状节点
        if isinstance(light, pm.nodetypes.Transform):
            light = light.getShape()

        # 存储 shape 节点
        self.light = light
        self.buildUI()

    def buildUI(self):
        # 创建 grid 布局
        layout = QtWidgets.QGridLayout(self)

        # 创建 复选框 用来设置可视化属性
        self.name = QtWidgets.QCheckBox(str(self.light.getTransform()))
        self.name.setChecked(self.light.visibility.get())
        self.name.toggled.connect(lambda val: self.light.getTransform().visibility.set(val))
        layout.addWidget(self.name, 0, 0)

        # 隔离显示按钮
        soloBtn = QtWidgets.QPushButton('Solo')
        soloBtn.setCheckable(True)
        soloBtn.toggled.connect(lambda val: self.onSolo.emit(val))
        layout.addWidget(soloBtn, 0, 1)

        # 删除按钮
        deleteBtn = QtWidgets.QPushButton('X')
        deleteBtn.clicked.connect(self.deleteLight)
        deleteBtn.setMaximumWidth(10)
        layout.addWidget(deleteBtn, 0, 2)

        # 强度滑竿
        intensity = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        intensity.setMinimum(1)
        intensity.setMaximum(1000)
        intensity.setValue(self.light.intensity.get())
        intensity.valueChanged.connect(lambda val: self.light.intensity.set(val))
        layout.addWidget(intensity, 1, 0, 1, 2)

        # 颜色按钮
        self.colorBtn = QtWidgets.QPushButton()
        self.colorBtn.setMaximumWidth(20)
        self.colorBtn.setMaximumHeight(20)
        self.setButtonColor()
        self.colorBtn.clicked.connect(self.setColor)
        layout.addWidget(self.colorBtn, 1, 2)

    def setButtonColor(self, color=None):
        # 设置按钮颜色

        # 如果没有传入颜色参数 就获取灯光的颜色
        if not color:
            color = self.light.color.get()

        # 类似于 lambda 函数 可转换为
        # if not len(color) == 3:
        #       raise Exception("You must provide a list of 3 colors")
        # 可以用来检测输入是否正确
        assert len(color) == 3, "You must provide a list of 3 colors"

        # 获取相关的颜色数值到 r,g,b 变量中
        r, g, b = [c * 255 for c in color]

        # 给按钮设置CSS样式
        self.colorBtn.setStyleSheet('background-color:rgba(%s,%s,%s,1)' % (r, g, b))

    def setColor(self):
        # 点击颜色按钮设置颜色

        # 获取灯光的颜色
        lightColor = self.light.color.get()
        # 打开 Maya 的颜色编辑器
        color = pm.colorEditor(rgbValue=lightColor)

        # Maya 返回了字符串
        # 我们需要手动将其转换为可用的变量
        r, g, b, a = [float(c) for c in color.split()]

        # 保存新的颜色值
        color = (r, g, b)

        # 设置新的颜色值
        self.light.color.set(color)
        self.setButtonColor(color)

    def disableLight(self, value):
        # self.name 为复选框
        # 设置复选框的状态
        self.name.setChecked(not bool(value))

    def deleteLight(self):
        # 删除灯光组件
        self.setParent(None)
        self.setVisible(False)
        self.deleteLater()

        # 删除灯光
        pm.delete(self.light.getTransform())