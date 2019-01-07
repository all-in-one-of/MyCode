# coding=utf-8

import sys
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as om

def maya_main_window():
    main_window_ptr = om.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr),QtWidgets.QWidget)

class TestDialog(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)
        self.setWindowTitle('啦啦啦')

if __name__ == '__main__':

    d = TestDialog()
    d.show()
