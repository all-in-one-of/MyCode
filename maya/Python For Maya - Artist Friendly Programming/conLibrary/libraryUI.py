# coding=utf-8
import pprint
from maya import cmds

import controllerLibrary

reload(controllerLibrary)
from PySide2 import QtWidgets, QtCore, QtGui


class ControllerLibraryUI(QtWidgets.QDialog):

    # 构建函数
    def __init__(self):
        # 调用QtWidgets.QDialog的init方法
        super(ControllerLibraryUI, self).__init__()
        # 设置Qt窗口名称
        self.setWindowTitle(u'模型库')
        # 调用功能函数
        self.library = controllerLibrary.ControllerLibrary()
        #  创建窗口UI
        self.buildUI()
        # 刷新调用
        self.populate()

    def buildUI(self):
        # 创建垂直布局容器
        layout = QtWidgets.QVBoxLayout(self)
        # 保存相关的widget容器
        saveWidget = QtWidgets.QWidget()
        # 保存相关的水平布局容器 （add到saveWidget中）
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        # 将相关的容器添加到主布局中
        layout.addWidget(saveWidget)

        self.saveNameField = QtWidgets.QLineEdit()  # 输入框
        # 将输入框添加到saveLayout中
        saveLayout.addWidget(self.saveNameField)

        saveBtn = QtWidgets.QPushButton('保存')  # save按钮
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)
        # 列表控件
        size = 64
        buffer = 12
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)  # 开启图标模式
        self.listWidget.setIconSize(QtCore.QSize(size, size))  # 设置图标大小
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)  # 设置调整窗口的时候自动换行
        self.listWidget.setGridSize(QtCore.QSize(size + buffer, size + buffer))  # 设置图标之间的间距
        layout.addWidget(self.listWidget)

        # 横向按钮容器
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        importBtn = QtWidgets.QPushButton('打开')
        importBtn.clicked.connect(self.load)

        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton('刷新')
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)

        closeBtn = QtWidgets.QPushButton('关闭')
        closeBtn.clicked.connect(self.close)
        btnLayout.addWidget(closeBtn)

    def populate(self):
        # 清理列表的内容 以免重复加载
        self.listWidget.clear()
        # 执行功能函数中的find功能
        self.library.find()
        # self.library是功能函数返回的字典
        # items会遍历字典中的所有元素 for循环可以调用到字典相关的元素
        for name, info in self.library.items():
            # 添加item到list组件中 显示name名称
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)

            # 获取截图路径
            screenshot = info.get('screenshot')
            # 如果截图存在
            if screenshot:
                # item设置图标
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)

            item.setToolTip(pprint.pformat(info))

    def load(self):
        currentItem = self.listWidget.currentItem()
        if not currentItem:
            return
        name = currentItem.text()
        print name

        self.library.load(name)

    def save(self):
        name = self.saveNameField.text()
        if not name.strip():
            cmds.warning(u'输入名字')
            return
        self.library.save(name)
        self.populate()
        self.saveNameField.text('')


def showUI():
    ui = ControllerLibraryUI()
    ui.show()
    return ui
