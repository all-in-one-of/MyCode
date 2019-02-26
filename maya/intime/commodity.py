# coding=utf-8
import os
import sys
from functools import partial

from PySide2 import QtWidgets, QtCore, QtGui
import pymel.core as pm
from maya import OpenMayaUI as omui
from maya import cmds
import customMaya

import logging
import Qt

# 初始化logging系统
logging.basicConfig()
# 设置名称 可以针对当前工具进行记录
logger = logging.getLogger()
# 设置信息反馈的模式
logger.setLevel(logging.DEBUG)

if Qt.__binding__ == 'PySide':
    logger.debug('Using PySide with shiboken')
    from shiboken import wrapInstance
    from Qt.QtCore import Signal
elif Qt.__binding__.startswith('PyQt'):
    logger.debug('Using PyQt with sip')
    from sip import wrapinstance as wrapInstance
    from Qt.QtCore import pyqtSignal as Signal
else:
    logger.debug('Using PySide2 with shiboken2')
    from shiboken2 import wrapInstance
    from Qt.QtCore import Signal


# 获取Maya的主窗口 用于 dock 窗口
def getMayaMainWindow():
    # 通过OpenMayaUI API 获取Maya主窗口
    win = omui.MQtUtil_mainWindow()
    # 将窗口转换成Python可以识别的东西 这里是将它转换为QMainWindow
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    return ptr


DOCKNAME = u'产品库'

RDX = r'F:\Share\2018\rdx'

ImageLose = r'C:\Users\Intime\Documents\MyCode\maya\intime\imageLose.jpg'

MakeState = {
    0: '未制作',
    1: '制作中···',
    2: '待审核···',
    3: '等待提交',
    4: '制作完成'
}
ColorLevel = {
    0: (255, 0, 0),  # 红色
    1: (255, 120, 0),
    2: (255, 255, 0),
    3: (64, 150, 80),
    4: (0, 255, 0)
}


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


class commodityUI(QtWidgets.QWidget):

    def __init__(self, path, dock=True):

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

        self.initCommodityInfo(path)

        self.create_widgets()
        self.buildUI()
        self.commodityTable(self.commodityNames)
        # self.populate()

        self.parent().layout().addWidget(self)

        if not dock:
            parent.show()

    def create_widgets(self):

        self.searchInput = QtWidgets.QLineEdit()

        self.searchButton = QtWidgets.QPushButton('搜索')
        self.searchButton.clicked.connect(self.searchCommodity)

        self.filtComboBox = QtWidgets.QComboBox()
        filtType = ['名称', 'sku']
        self.filtComboBox.addItems(filtType)

        self.filtComboBox.activated[str].connect(self.refrshCommodity)

    def commodityTable(self, commodityList):

        self.table.setRowCount(len(commodityList))
        self.table.verticalHeader().setDefaultSectionSize(55)
        self.table.setColumnCount(6)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)

        _n = 0

        for i in commodityList:
            commodityInfo = self.commodityInfo[i.values()[0]]
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

            self.table.setCellWidget(_n, 1, self.buttonRow(commodityFbx, commodityBegin))

            # self.table.update

            _n += 1

        self.table.setColumnWidth(0, 55)
        # self.table.setColumnWidth(1,78)
        self.table.setColumnWidth(2, 78)

        # self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        # self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)

    def buildUI(self):
        self.table = QtWidgets.QTableWidget()

        main_Layout = QtWidgets.QVBoxLayout(self)

        searchWidget = QtWidgets.QWidget()

        searchLayout = QtWidgets.QHBoxLayout(searchWidget)

        searchLayout.addWidget(self.filtComboBox)

        searchLayout.addWidget(self.searchInput)

        searchLayout.addWidget(self.searchButton)

        main_Layout.addWidget(searchWidget)

        main_Layout.addWidget(self.table)

    def refrshCommodity(self, filtType):

        if filtType == u'名称':
            self.commodityTable(self.commodityNames)
        if filtType == 'sku':
            self.commodityTable(self.commoditySKU)

    def buttonRow(self, path, commodityBegin):

        widget = QtWidgets.QWidget()

        updateBtn = QtWidgets.QPushButton('检查')
        if commodityBegin:
            updateBtn.setEnabled(False)
        updateBtn.clicked.connect(lambda: self.open_File(path))

        viewBtn = QtWidgets.QPushButton('导入')
        if commodityBegin:
            viewBtn.setEnabled(False)
        viewBtn.clicked.connect(lambda: self.import_File(path))

        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(updateBtn)
        hLayout.addWidget(viewBtn)

        widget.setLayout(hLayout)
        return widget

    def import_File(self, path):

        # cmds.file(path,i=True,f=True)
        customMaya.importMeshFile(path)

    def open_File(self, path):
        # cmds.file(path,o=True,f=True)
        customMaya.openMeshFile(path)

    def initCommodityInfo(self, path):
        print os.getcwd()
        self.commodityInfo = {}
        self.commodityNames = []
        self.commoditySKU = []
        for i in customMaya.findSpecifiedFile(path, 'json'):
            d = {}
            e = {}
            commodityOriginalInfo = customMaya.readJson(i)
            commodityOriginalSKU = customMaya.baseNameForPath(i, False)

            self.commodityInfo[commodityOriginalSKU] = commodityOriginalInfo

            d[commodityOriginalSKU] = commodityOriginalSKU
            self.commoditySKU.append(d)

            e[commodityOriginalInfo[u'商品名称']] = commodityOriginalSKU
            self.commodityNames.append(e)
            customMaya.chineseSort(self.commodityNames)

    def searchForName(self, searchText):
        commodityList = []
        for i in self.commodityNames:
            if searchText in i.keys()[0]:
                commodityList.append(i)
        return commodityList

    def searchForSku(self, searchText):
        commodityList = []
        for i in self.commoditySKU:
            if searchText in i.keys()[0]:
                commodityList.append(i)
        return commodityList

    def searchCommodity(self):
        searchText = self.searchInput.text()
        if not searchText.strip():
            cmds.warning(u'未检测到关键字')
            return

        elif self.filtComboBox.currentText() == u'名称':
            commodityList = self.searchForName(searchText)
            self.commodityTable(commodityList)
        elif self.filtComboBox.currentText() == 'sku':
            commodityList = self.searchForSku(searchText)
            self.commodityTable(commodityList)
        self.searchInput.clear()


class QCustomQWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)

        # 名字
        self.nameText = QtWidgets.QLabel()
        # sku
        self.skuText = QtWidgets.QLabel()
        # 制作人
        self.makerText = QtWidgets.QLabel()
        # 审核人
        self.inspectorText = QtWidgets.QLabel()
        # 对接人
        self.projectAcceptanceText = QtWidgets.QLabel()
        # 制作状态
        self.makeStateText = QtWidgets.QLabel()

        # 按钮layout
        self.buttonLayout = QtWidgets.QVBoxLayout()
        self.openBtn = QtWidgets.QPushButton('打开')
        self.importBtn = QtWidgets.QPushButton('导入')
        self.buttonLayout.addWidget(self.openBtn)
        self.buttonLayout.addWidget(self.importBtn)

        # 文本左layout
        self.textQVBoxLayoutLeft = QtWidgets.QVBoxLayout()
        self.textQVBoxLayoutLeft.addWidget(self.nameText)
        self.textQVBoxLayoutLeft.addWidget(self.skuText)
        self.textQVBoxLayoutLeft.addWidget(self.makeStateText)

        # 文本右layout
        self.textQVBoxLayoutRight = QtWidgets.QVBoxLayout()
        self.textQVBoxLayoutRight.addWidget(self.makerText)
        self.textQVBoxLayoutRight.addWidget(self.projectAcceptanceText)
        self.textQVBoxLayoutRight.addWidget(self.inspectorText)

        # 图片layout
        self.iconBtn = QtWidgets.QPushButton()

        # 主 layout
        self.allQHBoxLayout = QtWidgets.QHBoxLayout()

        self.allQHBoxLayout.addWidget(self.iconBtn, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayoutLeft, 1)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayoutRight, 1)
        # self.allQHBoxLayout.addWidget(self.buttonRow())
        self.allQHBoxLayout.addLayout(self.buttonLayout)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        # self.textUpQLabel.setStyleSheet('''
        #     color: rgb(0, 0, 255);
        # ''')
        # self.textDownQLabel.setStyleSheet('''
        #     color: rgb(255, 0, 0);
        # ''')

    def setIcon(self, imagePath):
        if os.path.exists(imagePath):
            self.iconBtn.setIcon(QtGui.QPixmap(imagePath))
        else:
            self.iconBtn.setIcon(QtGui.QPixmap(ImageLose))

        self.iconBtn.setIconSize(QtCore.QSize(50, 50))
        self.iconBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def setMakeState(self, info):
        self.makeStateText.setText(MakeState[info])
        self.makeStateText.setStyleSheet('color:rgb(%s,%s,%s)' % ColorLevel[info])

    # def set


class commodityLibraryUI(QtWidgets.QWidget):

    def __init__(self, dock=True):
        if dock:
            parent = getDock(DOCKNAME)
        else:
            # 删除dock窗口
            deleteDock(DOCKNAME)

            try:
                # 删除窗口 如果窗口本身不存在 用try可以让代码不会停止运行并报错
                pm.deleteUI(DOCKNAME)

            except:
                logger.debug('No previous UI exists')

            # 获取Maya主窗口 并将窗口负载在Qt窗口上
            parent = QtWidgets.QDialog(parent=getMayaMainWindow())
            parent.setObjectName(DOCKNAME)
            parent.setWindowTitle(DOCKNAME)
            layout = QtWidgets.QVBoxLayout(parent)

        if not dock:
            parent.show()

        super(commodityLibraryUI, self).__init__(parent=parent)

        self.createWidgets()
        self.createLayouts()
        self.initCommodityInfo(r'C:\Users\Intime\Documents\MyCode\maya\intime')
        self.refreshCommodityList()

        self.parent().layout().addWidget(self)

    def createWidgets(self):

        self.commodityList = QtWidgets.QListWidget()

    def createLayouts(self):
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(self.commodityList)

    def refreshCommodityList(self):

        for i in self.commodityNames:
            sku = i.values()[0]
            self.readCommodity(sku)

    def initCommodityInfo(self, path):
        self.commodityInfo = {}
        self.commodityNames = []
        self.commoditySKU = []
        for i in customMaya.findSpecifiedFile(path, 'json'):
            d = {}
            e = {}
            commodityOriginalInfo = customMaya.readJson(i)
            commodityOriginalSKU = customMaya.baseNameForPath(i, False)

            self.commodityInfo[commodityOriginalSKU] = commodityOriginalInfo

            d[commodityOriginalSKU] = commodityOriginalSKU
            self.commoditySKU.append(d)

            e[commodityOriginalInfo[u'商品名称']] = commodityOriginalSKU
            self.commodityNames.append(e)
            customMaya.chineseSort(self.commodityNames)

    def readCommodity(self, sku):

        commodityInfo = self.commodityInfo[sku]

        # 自定义组件
        myQCustomQWidget = QCustomQWidget()

        # 创建列表组件
        myQListWidgetItem = QtWidgets.QListWidgetItem(self.commodityList)

        commodityPhoto = commodityInfo[u'商品图片地址']
        myQCustomQWidget.setIcon(commodityPhoto)
        myQCustomQWidget.iconBtn.clicked.connect(lambda: self.openExplorer(os.path.dirname(commodityPhoto)))

        myQCustomQWidget.nameText.setText('名称：%s' % commodityInfo[u'商品名称'].encode('utf-8'))
        myQCustomQWidget.skuText.setText('sku：%s' % commodityInfo[u'sku'].encode('utf-8'))
        myQCustomQWidget.makerText.setText('制作人：%s' % commodityInfo[u'制作人'].encode('utf-8'))
        myQCustomQWidget.setMakeState(commodityInfo[u'制作状态'])
        myQCustomQWidget.inspectorText.setText('审核人：%s' % commodityInfo[u'审核人'].encode('utf-8'))
        myQCustomQWidget.projectAcceptanceText.setText('对接人：%s' % commodityInfo[u'对接人'].encode('utf-8'))

        # 按钮
        commodityFbx = commodityInfo[u'规格'][u'finally'][u'模型'][u'收藏级'][u'fbx文件地址']
        myQCustomQWidget.openBtn.clicked.connect(lambda: self.openFile(commodityFbx))
        myQCustomQWidget.importBtn.clicked.connect(lambda: self.importFile(commodityFbx))

        # 设置列表组件大小为自定义组件的大小
        myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())

        # 添加自定义组件到列表组件
        self.commodityList.setItemWidget(myQListWidgetItem, myQCustomQWidget)

    def importFile(self, path):
        customMaya.importMeshFile(path)

    def openFile(self, path):
        customMaya.openMeshFile(path)

    def openExplorer(self, path):
        os.system("explorer.exe %s" % path)
