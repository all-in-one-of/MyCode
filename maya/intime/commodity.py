# coding=utf-8
from PySide2 import QtWidgets, QtCore, QtGui
import pymel.core as pm
from functools import partial
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui
from maya import cmds
import customMaya
# from intimeCommodity import *

import logging

# 初始化logging系统
logging.basicConfig()
# 设置名称 可以针对当前工具进行记录
logger = logging.getLogger('LightingManager')
# 设置信息反馈的模式
logger.setLevel(logging.DEBUG)

DOCKNAME = u'产品库'

RDX = r'F:\Share\2018\rdx'


def getDock(name=DOCKNAME):
    # 首先删除重名的窗口
    deleteDock(name)
    # 生成可以dock的Maya窗口
    # dockToMainWindow 将窗口dock进右侧的窗口栏中
    # label 设置标签名称
    ctrl = pm.workspaceControl(name, dockToMainWindow=('right', 1), label=DOCKNAME)
    # 通过OpenMayaUI API 获取窗口相关的 Qt 信息
    qtCtrl = omui.MQtUtil_findControl(ctrl)
    # 将 qtCtrl 转换为Python可以识别的形式
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)
    return ptr


def deleteDock(name=DOCKNAME):
    # 查询窗口是否存在
    if pm.workspaceControl(name, query=True, exists=True):
        # 存在即删除
        pm.deleteUI(name)


def getMayaMainWindow():
    # 通过OpenMayaUI API 获取Maya主窗口
    win = omui.MQtUtil_mainWindow()
    # 将窗口转换成Python可以识别的东西 这里是将它转换为QMainWindow
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    return ptr


class commodityUI(QtWidgets.QWidget):
    def __init__(self, info, dock=True):
        self.intimeCommodity = info
        # self.IntmeCommodity.findCommodity(RDX)
        # if dock:
        parent = getDock()
        # else:
        #     # 删除dock窗口
        #     deleteDock()
        #     try:
        #         # 删除窗口 如果窗口本身不存在 用try可以让代码不会停止运行并报错
        #         pm.deleteUI(DOCKNAME)
        #     except:
        #         logger.debug('No previous UI exists')
        #
        #     # 获取Maya主窗口 并将窗口负载在Qt窗口上
        #     parent = QtWidgets.QDialog(parent=getMayaMainWindow())
        #     # 设置名称 可以在后面找到它
        #     parent.setObjectName(DOCKNAME)
        #     parent.setWindowTitle(DOCKNAME)
        #     layout = QtWidgets.QVBoxLayout(parent)

        # 执行父对象，并且设置parent
        super(commodityUI, self).__init__(parent=parent)
        self.create_widgets()
        self.commodityTable()
        # self.populate()
        self.buildUI()

        self.parent().layout().addWidget(self)

        if not dock:
            parent.show()

    def create_widgets(self):
        self.searchInput = QtWidgets.QLineEdit()
        self.searchButton = QtWidgets.QPushButton('搜索')
        self.searchButton.clicked.connect(self.lll)

    def commodityTable(self):
        self.table = QtWidgets.QTableWidget()

        self.table.setRowCount(len(self.intimeCommodity))
        self.table.verticalHeader().setDefaultSectionSize(55)
        self.table.setColumnCount(6)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)

        _n = 0

        for i in self.intimeCommodity:
            commodityInfo = customMaya.readJson(i)
            name = commodityInfo[u'sku']
            commodityName = commodityInfo[u'商品名称']
            commodityMaker = commodityInfo[u'制作人']
            commodityInspector = commodityInfo[u'审核人']
            commodityProjectAcceptance = commodityInfo[u'对接人']
            commodityObj = commodityInfo[u'制作类型']
            commodityBegin = commodityInfo[u'录入时间']
            commodityMakeBegin = commodityInfo[u'开始制作时间']
            commodityPhoto = commodityInfo[u'商品图片地址']
            commodityFbx = commodityInfo[u'规格'][u'finally'][u'模型'][u'收藏级'][u'fbx文件地址']

            self.table.setItem(_n, 2, QtWidgets.QTableWidgetItem(name))
            self.table.setItem(_n, 3, QtWidgets.QTableWidgetItem(commodityName))
            self.table.setItem(_n, 4, QtWidgets.QTableWidgetItem(
                commodityMaker + '/' + commodityInspector + '/' + commodityProjectAcceptance))

            icon = QtWidgets.QLabel('')
            icon.setAlignment(QtCore.Qt.AlignCenter)

            icon.setPixmap(QtGui.QPixmap(commodityPhoto).scaled(50, 50))
            self.table.setCellWidget(_n, 0, icon)

            self.table.setCellWidget(_n, 1, self.buttonRow(commodityFbx,commodityBegin))

            # self.table.update

            _n += 1

        self.table.setColumnWidth(0, 55)
        # self.table.setColumnWidth(1,78)
        self.table.setColumnWidth(2, 78)

        # self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        # self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)

    def buildUI(self):
        main_Layout = QtWidgets.QVBoxLayout(self)

        searchWidget = QtWidgets.QWidget()

        searchLayout = QtWidgets.QHBoxLayout(searchWidget)

        searchLayout.addWidget(self.searchInput)

        searchLayout.addWidget(self.searchButton)

        main_Layout.addWidget(searchWidget)

        main_Layout.addWidget(self.table)

    def lll(self):
        print self.table.currentItem().text()

    def buttonRow(self, path,commodityBegin):
        # 列表内添加按钮
        widget = QtWidgets.QWidget()
        # 修改

        updateBtn = QtWidgets.QPushButton('检查')
        if commodityBegin:
            updateBtn.setEnabled(False)
        # updateBtn.setStyleSheet(''' text-align : center;
        #                                       background-color : NavajoWhite;
        #                                       height : 30px;
        #                                       border-style: outset;
        #                                       font : 13px  ''')


        updateBtn.clicked.connect(lambda: self.open_File(path))
        # if commodityMakeBegin is False:
        #     updateBtn.setCheckable(True)
        # 查看
        viewBtn = QtWidgets.QPushButton('导入')
        # viewBtn.setStyleSheet(''' text-align : center;
        #                               background-color : DarkSeaGreen;
        #                               height : 30px;
        #                               border-style: outset;
        #                               font : 13px; ''')

        viewBtn.clicked.connect(lambda: self.import_File(path))

        # 删除
        # deleteBtn = QtWidgets.QPushButton('删除')
        # deleteBtn.setStyleSheet(''' text-align : center;
        #                                 background-color : LightCoral;
        #                                 height : 30px;
        #                                 border-style: outset;
        #                                 font : 13px; ''')

        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(updateBtn)
        hLayout.addWidget(viewBtn)
        # hLayout.addWidget(deleteBtn)
        # hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget

    def import_File(self, path):

        # cmds.file(path,i=True,f=True)
        customMaya.importMeshFile(path)

    def open_File(self, path):
        # cmds.file(path,o=True,f=True)
        customMaya.openMeshFile(path)


c = customMaya.findSpecifiedFile(r'F:\Share\2018\rdx', 'json')
a = commodityUI(c)
a.show()
