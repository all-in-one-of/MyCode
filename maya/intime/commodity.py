# coding=utf-8
import os
import sys
from functools import partial
import re
from PySide2 import QtWidgets, QtCore, QtGui
import pymel.core as pm
from maya import OpenMayaUI as omui
from maya import cmds
from PIL import Image
import customMaya

import logging
import Qt

TempPath = os.path.join(os.environ['TEMP'], 'inTimeLibrary')
customMaya.createDirectory(TempPath)
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
FlitType = [
    '名称',
    'sku',
    '制作人',
    '',
    '',
    '',
]
Makers = [
    u'韩开旺',
    u'何思民'
]


# 获取Maya的主窗口 用于 dock 窗口
def getMayaMainWindow():
    # 通过OpenMayaUI API 获取Maya主窗口
    win = omui.MQtUtil_mainWindow()
    # 将窗口转换成Python可以识别的东西 这里是将它转换为QMainWindow
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    return ptr


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
        self.allQHBoxLayout.addLayout(self.buttonLayout)

        self.setLayout(self.allQHBoxLayout)

    def setIcon(self, imagePath):
        self.iconBtn.setIcon(QtGui.QPixmap(imagePath))

        self.iconBtn.setIconSize(QtCore.QSize(50, 50))
        self.iconBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def setMakeState(self, info):
        self.makeStateText.setText(MakeState[info])
        self.makeStateText.setStyleSheet('color:rgb(%s,%s,%s)' % ColorLevel[info])

    def setNameText(self, text):
        self.nameText.setText(text)


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

        self.setMinimumWidth(370)
        self.createWidgets()
        self.createLayouts()
        cc = r'C:\Users\Intime\Documents\MyCode\maya\intime'
        self.initCommodityInfo(RDX)
        self.flitCommodity(self.radioBtn0)
        self.lineEditCompleter()

        self.parent().layout().addWidget(self)

    def createWidgets(self):

        self.testBtn = QtWidgets.QPushButton()

        # 列表框
        self.commodityList = QtWidgets.QListWidget()
        self.commodityList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # 搜索框
        self.searchInput = QtWidgets.QLineEdit()
        self.searchBtn = QtWidgets.QPushButton('搜索')
        self.searchBtn.clicked.connect(self.searchCommodity)

        self.searchLayout = QtWidgets.QHBoxLayout()
        self.searchLayout.addWidget(self.searchInput)
        self.searchLayout.addWidget(self.searchBtn)
        self.searchInput.returnPressed.connect(self.searchCommodity)

        # self.searchLayout.addWidget(self.testBtn)
        # self.testBtn.clicked.connect(self.lll)

        # 分类框

        self.commodityNmuber = QtWidgets.QLabel()

        self.radioBtn0 = QtWidgets.QRadioButton('名称')
        self.radioBtn1 = QtWidgets.QRadioButton('sku')
        self.radioBtn2 = QtWidgets.QRadioButton('完成度')
        self.radioBtn3 = QtWidgets.QRadioButton('制作人')

        self.radioBtn0.clicked.connect(lambda: self.flitCommodity(self.radioBtn0))
        self.radioBtn1.clicked.connect(lambda: self.flitCommodity(self.radioBtn1))
        self.radioBtn2.clicked.connect(lambda: self.flitCommodity(self.radioBtn2))
        self.radioBtn3.clicked.connect(lambda: self.flitCommodity(self.radioBtn3))

        self.radioBtn0.setChecked(True)

        self.radioLayout = QtWidgets.QHBoxLayout()

        self.radioLayout.addWidget(self.commodityNmuber)
        self.radioLayout.addWidget(self.radioBtn0)
        self.radioLayout.addWidget(self.radioBtn1)
        self.radioLayout.addWidget(self.radioBtn2)
        self.radioLayout.addWidget(self.radioBtn3)

        ######

    def createLayouts(self):
        mainLayout = QtWidgets.QVBoxLayout(self)

        mainLayout.addLayout(self.searchLayout)
        mainLayout.addLayout(self.radioLayout)
        mainLayout.addWidget(self.commodityList)

    def refreshCommodityList(self, commodityList):
        self.setCommodityNumber(len(commodityList))
        self.commodityList.clear()
        for i in commodityList:
            sku = i.values()[0]
            self.readCommodity(sku)

    def initCommodityInfo(self, path=RDX):
        self.commodityInfo = {}
        self.commodityNames = []
        self.commoditySKU = []
        self.commodityMaker = []
        self.commodityMakeState = []
        self.commodityIcon = {}
        for i in customMaya.findSpecifiedFile(path, 'json'):
            d = {}
            e = {}
            f = {}
            g = {}
            commodityOriginalInfo = customMaya.readJson(i)
            commodityOriginalSKU = customMaya.baseNameForPath(i, False)

            self.commodityInfo[commodityOriginalSKU] = commodityOriginalInfo

            d[commodityOriginalSKU] = commodityOriginalSKU
            self.commoditySKU.append(d)

            e[commodityOriginalInfo[u'商品名称']] = commodityOriginalSKU
            self.commodityNames.append(e)
            customMaya.chineseSort(self.commodityNames)

            f[commodityOriginalInfo[u'制作人']] = commodityOriginalSKU
            self.commodityMaker.append(f)
            customMaya.chineseSort(self.commodityMaker)

            g[commodityOriginalInfo[u'制作状态']] = commodityOriginalSKU
            self.commodityMakeState.append(g)
            self.commodityMakeState.sort()
            self.commodityMakeState.reverse()

            originalCommodityImage = commodityOriginalInfo[u'商品图片地址']

            cacheImage = os.path.join(TempPath, os.path.basename(originalCommodityImage))
            imageSize = (64, 64)
            if os.path.exists(cacheImage) is False:
                try:
                    customMaya.imageSaveAs(originalCommodityImage,
                                           cacheImage,
                                           imageSize)
                    self.commodityIcon[commodityOriginalSKU] = cacheImage
                except:
                    customMaya.imageSaveAs(ImageLose,
                                           cacheImage,
                                           imageSize)
                    self.commodityIcon[commodityOriginalSKU] = cacheImage

            else:
                # try:
                #     customMaya.imageSaveAs(originalCommodityImage,
                #                            cacheImage,
                #                            imageSize)
                #     self.commodityIcon[commodityOriginalSKU] = cacheImage
                # except:
                #     customMaya.imageSaveAs(ImageLose,
                #                            cacheImage,
                #                            (50, 50))
                self.commodityIcon[commodityOriginalSKU] = cacheImage
        self.commodityInfoList = self.commodityNames

        # break

    def readCommodity(self, sku):
        # 自定义组件
        self.myQCustomQWidget = QCustomQWidget()

        commodityInfo = self.commodityInfo[sku]

        # 创建列表组件
        myQListWidgetItem = QtWidgets.QListWidgetItem(self.commodityList)

        commodityPhoto = self.commodityIcon[sku]
        self.myQCustomQWidget.setIcon(commodityPhoto)
        self.myQCustomQWidget.iconBtn.clicked.connect(lambda: self.openExplorer(os.path.dirname(commodityPhoto)))

        commodityName = commodityInfo[u'商品名称']
        self.setNameText(self.width(), commodityName)
        # self.myQCustomQWidget.nameText.setText('名称：%s' % commodityName.encode('utf-8'))

        self.myQCustomQWidget.skuText.setText('sku：%s' % commodityInfo[u'sku'].encode('utf-8'))
        self.myQCustomQWidget.makerText.setText('制作人：%s' % commodityInfo[u'制作人'].encode('utf-8'))
        self.myQCustomQWidget.setMakeState(commodityInfo[u'制作状态'])
        self.myQCustomQWidget.inspectorText.setText('审核人：%s' % commodityInfo[u'审核人'].encode('utf-8'))
        self.myQCustomQWidget.projectAcceptanceText.setText('对接人：%s' % commodityInfo[u'对接人'].encode('utf-8'))
        # 按钮
        commodityFbx = commodityInfo[u'规格'][u'finally'][u'模型'][u'收藏级'][u'fbx文件地址']
        self.myQCustomQWidget.openBtn.clicked.connect(lambda: self.openFile(commodityFbx))
        self.myQCustomQWidget.importBtn.clicked.connect(lambda: self.importFile(commodityFbx))
        self.setBtn(self.myQCustomQWidget.importBtn, commodityInfo[u'制作状态'])
        self.setBtn(self.myQCustomQWidget.openBtn, commodityInfo[u'制作状态'])

        # 设置列表组件大小为自定义组件的大小
        myQListWidgetItem.setSizeHint(self.myQCustomQWidget.sizeHint())

        # 添加自定义组件到列表组件
        self.commodityList.setItemWidget(myQListWidgetItem, self.myQCustomQWidget)
        # myQListWidgetItem.setText('  ' + sku)
        # # myQListWidgetItem.setTextAlignment(QtCore.Qt.AlignCenter)
        # # myQListWidgetItem.setTextColor(QtGui.QColor('#282828'))
        # self.commodityList.setItemSelected(myQListWidgetItem, True)

    def importFile(self, path):
        customMaya.importMeshFile(path)

    def openFile(self, path):
        customMaya.openMeshFile(path)

    def openExplorer(self, path):
        os.system("explorer.exe %s" % path)

    def flitCommodity(self, btn):

        a = self.commodityInfoList
        if btn.text() == u'名称' and btn.isChecked() is True:
            # self.refreshCommodityList(self.commodityNames)
            a = []
            for i in self.commodityInfoList:
                b = {}
                for sku in i.values():
                    b[self.commodityInfo[sku][u'商品名称']] = sku
                    a.append(b)
            customMaya.chineseSort(a)


        elif btn.text() == u'sku' and btn.isChecked() is True:
            pass
        elif btn.text() == u'完成度' and btn.isChecked() is True:
            a = []
            for i in self.commodityInfoList:
                b = {}
                for sku in i.values():
                    b[self.commodityInfo[sku][u'制作状态']] = sku
                    a.append(b)
            a.sort()

        elif btn.text() == u'制作人' and btn.isChecked() is True:
            a = []
            for i in self.commodityInfoList:
                b = {}
                for sku in i.values():
                    b[self.commodityInfo[sku][u'制作人']] = sku
                    a.append(b)
            customMaya.chineseSort(a)

        self.commodityInfoList = a
        self.refreshCommodityList(self.commodityInfoList)

    def setCommodityNumber(self, num):
        self.commodityNmuber.setText('总计：%s/%s' % (str(num), len(self.commoditySKU)))

    # 监听窗口事件
    def resizeEvent(self, event):
        self.refreshCommodityList(self.commodityInfoList)
        # print self.width()
        # QtWidgets.QWidget.resizeEvent(self, event)

    def setNameText(self, width, text):

        if width < 450 and len(text) > 4:
            nt = u'名称：' + text[:4] + u'···'
            self.myQCustomQWidget.setNameText(nt)
        else:
            self.myQCustomQWidget.setNameText(u'名称：' + text)

    def searchCommodity(self):
        text = self.searchInput.text()
        self.commodityInfoList = []
        if re.compile(u'[\u4e00-\u9fa5]').search(text):
            if text in ''.join(Makers):
                for i in self.commodityMaker:
                    if text in i.keys():
                        self.commodityInfoList.append(i)
                        self.radioBtn3.setChecked(True)
            else:
                for i in self.commodityNames:
                    if text in i.keys()[0]:
                        self.commodityInfoList.append(i)
                        self.radioBtn0.setChecked(True)

        else:
            for i in self.commoditySKU:
                if text in i.keys()[0]:
                    self.commodityInfoList.append(i)
                    self.radioBtn1.setChecked(True)

        self.refreshCommodityList(self.commodityInfoList)

    def lll(self):
        print self.commodityList.selectedItems()[0].text()

    def setBtn(self, btn, num):
        if num <= 1:
            btn.setEnabled(False)

    def lineEditCompleter(self):
        items = []
        for i in self.commodityNames:
            for k, v in i.items():
                if k not in items:
                    items.append(k)
                if v not in items:
                    items.append(v)
        self.completer = QtWidgets.QCompleter(items)
        # self.completer.setMaxVisibleItems(100)
        self.searchInput.setCompleter(self.completer)
