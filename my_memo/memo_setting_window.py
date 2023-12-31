from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QComboBox,
    QSlider,
)
from PyQt5.QtGui import (
    QFont,
    QIcon,
    QColor,
    QPixmap
)
from PyQt5.QtCore import QSize, Qt

"""
便签设置

MemoSettingWindow 便签设置窗口: 设置便签颜色、透明度, 存放GitHub链接
"""


def singleton(cls):
    instances = {}

    def wrapper(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return wrapper


@singleton
class MemoSettingWindow(QMainWindow):
    """
    便签设置窗口

    设置便签颜色、透明度, 存放GitHub链接
    """

    def __init__(self, memo_app, pos_x, pos_y):
        super().__init__()

        # 便签程序
        self.memo_app = memo_app

        # 窗口布局
        self.init_gui(pos_x, pos_y)

    def init_gui(self, pos_x, pos_y):
        """设置页面布局"""
        # 窗口名
        self.setWindowTitle("设置")

        # 窗口图标
        self.setWindowIcon(QIcon("icon/gear.png"))

        # 窗口位置和大小
        self.setGeometry(pos_x, pos_y, 450, 450)

        # 窗口字体设置
        font = QFont("微软雅黑", 12)
        self.setFont(font)

        # 窗口布局
        self.setting_layout = QVBoxLayout()

        # 便签颜色设置
        self.color_label = QLabel("便签颜色")

        self.color_box = QComboBox(self)

        color_dic = {"pink": (255, 175, 223),
                     "yellow": (255, 230, 110),
                     "blue": (158, 223, 255),
                     "green": (161, 239, 155),
                     "purple": (215, 175, 255),
                     "grey": (224, 224, 224)
                     }

        for color in color_dic.values():
            pixColor = QPixmap(70, 20)
            pixColor.fill(QColor(color[0], color[1], color[2]))
            self.color_box.addItem(QIcon(pixColor), '')
            self.color_box.setIconSize(QSize(70, 20))

        self.color_box.setFixedSize(100, 30)
        self.color_box.currentIndexChanged.connect(self.choose_color)
        self.color_box.setCurrentIndex(
            self.memo_app.setting_info["background"]["index"])

        self.setting_layout.addWidget(self.color_label)
        self.setting_layout.addWidget(self.color_box)

        # 分割线
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.setting_layout.addWidget(line)

        # 便签透明度设置
        self.opacity_label = QLabel("便签透明度")
        opacity_value = int(self.memo_app.setting_info["opacity"]*100)
        self.opacity_label.setText(f'便签透明度: {opacity_value}%')

        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(opacity_value)
        self.opacity_slider.valueChanged.connect(self.update_opacity)

        self.setting_layout.addWidget(self.opacity_label)
        self.setting_layout.addWidget(self.opacity_slider)

        # 分割线
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.setting_layout.addWidget(line)

        # 关于
        self.about_label = QLabel("关于")

        self.url_label = QLabel(
            '<a href="https://github.com/Sisyphus0218/UCAS-OOP/tree/master/my_memo">GitHub</a>')
        self.url_label.setOpenExternalLinks(True)

        self.setting_layout.addWidget(self.about_label)
        self.setting_layout.addWidget(self.url_label)

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.setting_layout)
        self.setCentralWidget(self.central_widget)

        # 显示窗口
        self.show()

    def choose_color(self, index):
        """选择便签颜色"""
        color_dic = {"pink": (255, 228, 241),
                     "yellow": (255, 247, 209),
                     "blue": (226, 241, 255),
                     "green": (228, 249, 224),
                     "purple": (242, 230, 255),
                     "grey": (243, 242, 241)
                     }

        if (index == 0):
            color = "pink"
        elif (index == 1):
            color = "yellow"
        elif (index == 2):
            color = "blue"
        elif (index == 3):
            color = "green"
        elif (index == 4):
            color = "purple"
        elif (index == 5):
            color = "grey"

        self.memo_app.setting_info["background"] = {
            "color": color, "rgb": color_dic[color], "index": index}
        self.memo_app.save_setting_info()

    def update_opacity(self, value):
        """选择便签透明度"""
        opacity_value = value / 100.0
        self.opacity_label.setText(f'透明度: {value}%')
        self.memo_app.setting_info["opacity"] = opacity_value
        self.memo_app.save_setting_info()
