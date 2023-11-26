import os
import sys
import json
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QDesktopWidget
)

from memo import MemoListWindow


"""
TODO 

- README (加上icon来源, 协议)
- 编辑时间
- 打包
- 导出为pdf
- 云存储
"""

"""
便签程序

MemoApp 便签程序: 管理所有窗口, 管理便签的文件和相关信息
"""


class MemoApp(QMainWindow):
    """
    便签程序

    管理所有窗口, 管理便签的文件和相关信息
    """

    def __init__(self):
        super().__init__()

        # 便签信息: 包括便签名、标题、图片路径等
        self.memo_info = {}
        self.load_memo_info()

        # 设置信息: 包括便签透明度、背景颜色
        self.setting_info = {}
        self.load_setting_info()

        # 便签列表
        self.is_memo_list_open = True
        self.memo_list_window = MemoListWindow(self)

        # 便签设置
        self.is_setting_window_open = False
        self.memo_setting_window = None

        # 被打开的便签窗口
        self.memo_windows = {}

        # 便签数目
        self.memo_num = self.memo_list_window.memo_list.count()

    def load_memo_info(self):
        """从json文件加载便签信息"""
        try:
            with open("memo_info.json", "r") as json_file:
                self.memo_info = json.load(json_file)
        except FileNotFoundError:
            pass

    def save_memo_info(self):
        """保存便签信息到json文件"""
        with open("memo_info.json", "w") as json_file:
            json.dump(self.memo_info, json_file, indent=4)

    def load_setting_info(self):
        """从json文件加载设置信息"""
        try:
            with open("setting_info.json", "r") as json_file:
                self.setting_info = json.load(json_file)
        except FileNotFoundError:
            pass

    def save_setting_info(self):
        """保存设置信息到json文件"""
        with open("setting_info.json", "w") as json_file:
            json.dump(self.setting_info, json_file, indent=4)

    def delete_file(self, file_path):
        """删除文件"""
        try:
            os.remove(file_path)
            # print(f"{file_path} 文件已成功删除")
        except FileNotFoundError:
            print(f"文件 {file_path} 不存在")
        except Exception as e:
            print(f"删除 {file_path} 文件时出现错误: {e}")

    def get_distance(self, window):
        """计算窗口相对于屏幕右边缘距离"""
        # 获取屏幕的几何信息
        screen_geometry = QDesktopWidget().screenGeometry()

        # 获取窗口的几何信息
        window_geometry = window.geometry()

        # 计算窗口相对于屏幕右边缘的距离
        distance_right = screen_geometry.width() - (window_geometry.x() +
                                                    window_geometry.width())

        return distance_right


if __name__ == "__main__":
    app = QApplication(sys.argv)
    memo_app = MemoApp()
    sys.exit(app.exec_())
