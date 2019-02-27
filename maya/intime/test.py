# coding=utf-8
from PIL import Image

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


# 导入必须模块
import sys

# 主函数
from PySide2.QtWidgets import *

# coding:utf-8
import sys
import time


# QWidget是所有用户界面类的基类
class SampleWindow(QWidget):
    # 主窗口类
    # 构造函数
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Sample Window")
        # 从屏幕上（300，300）位置开始（即为最左上角的点），显示一个200*150的界面（宽200，高150）
        self.setGeometry(300, 300, 400, 350)

    def setIcon(self):
        # 设置icon
        appIcon = QIcon(r"C:\Users\Intime\Desktop\ssss\a001.ico")
        self.setWindowIcon(appIcon)


if __name__ == "__main__":
    try:
        myApp = QApplication(sys.argv)
        myWindow = SampleWindow()
        myWindow.setIcon()
        myWindow.show()
        myApp.exec_()
        sys.exit(0)
    except NameError:
        print("NameError:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])