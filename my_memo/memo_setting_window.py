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
    QFrame,
    QComboBox
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

        # 窗口布局
        self.init_gui()

        # 显示窗口
        self.show()

    def init_gui(self):
        """TODO: 设置页面布局"""
        # 窗口名
        self.setWindowTitle("Setting")

        # 窗口图标
        self.setWindowIcon(QIcon("icon/gear.png"))

        # 窗口大小
        self.resize(450, 450)

        # 窗口字体设置
        font = QFont("微软雅黑", 12)
        self.setFont(font)

        # 窗口布局
        self.setting_layout = QVBoxLayout()

        # 颜色
        self.color_lable = QLabel("颜色")

        self.color_box = QComboBox(self)
        self.color_box.addItem('选项1')
        self.color_box.addItem('选项2')
        self.color_box.addItem('选项3')
        self.color_box.currentIndexChanged.connect(self.choose_color)

        self.setting_layout.addWidget(self.color_lable)
        self.setting_layout.addWidget(self.color_box)

        # 分割线
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.setting_layout.addWidget(line)

        # 语言
        self.language_lable = QLabel("语言")
        self.setting_layout.addWidget(self.language_lable)

        self.language_box = QComboBox(self)
        self.language_box.addItem('选项1')
        self.language_box.addItem('选项2')
        self.language_box.addItem('选项3')
        self.language_box.currentIndexChanged.connect(self.choose_color)

        self.setting_layout.addWidget(self.language_lable)
        self.setting_layout.addWidget(self.language_box)

        # 分割线
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.setting_layout.addWidget(line)

        # 关于
        self.about_lable = QLabel("关于")
        self.setting_layout.addWidget(self.about_lable)

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.setting_layout)
        self.setCentralWidget(self.central_widget)

    def choose_color(self):
        pass
