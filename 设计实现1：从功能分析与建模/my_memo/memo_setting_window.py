import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTextEdit,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QColorDialog,
    QSpinBox,
    QToolBar,
    QAction,
)
from PyQt5.QtGui import (
    QTextImageFormat,
    QImage,
    QTextCursor,
    QTextCharFormat,
    QFont,
    QIcon,
)
from PyQt5.QtCore import QSize
import os
import time
import shutil
import json


class MemoSettingWindow(QMainWindow):
    """
    便签设置窗口

    TODO: 云存储，语言，背景
    """

    def __init__(self):
        super().__init__()

        # 窗口名
        self.setWindowTitle("Setting")

        # 窗口布局
        self.init_gui()

        # 显示窗口
        self.show()

    def init_gui(self):
        """TODO: 设置页面布局"""
        self.resize(370, 370)

        self.setting_layout = QVBoxLayout()

        self.sync_lable = QLabel("同步")
        self.setting_layout.addWidget(self.sync_lable)

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.setting_layout)

        self.setCentralWidget(self.central_widget)
