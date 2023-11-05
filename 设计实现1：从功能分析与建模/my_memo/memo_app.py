import os
import sys
import json
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
)

from memo import MemoListWindow


"""
TODO:
笔记/便签：开发一个随手记录零碎信息的应用
基本要求：支持基本文字排版；支持保存 读取
扩展要求：支持插入图片、视频、公式、表格等；支持 Markdown 、……
硬核要求：导入导出、历史记录、云存储接入、……

--------------------

设置界面
- 语言
- 皮肤
- README (加上icon来源, 协议)
- 同步 (如果可以)

收尾
- 打开窗口时窗口的位置
- 便签窗口置顶
- 编辑时间
- 每次打开上一次最后关闭的便签
- 回收站
- 打包

--------------------

最后任务
- 导出为pdf
- 打开时显示上一次关闭的便签
"""


class MemoApp(QMainWindow):
    """
    便签程序

    管理所有窗口，管理便签的文件和相关信息
    """

    def __init__(self):
        super().__init__()

        # 便签信息：包括便签名、标题、图片路径等
        self.memo_info = {}
        self.load_memo_info()

        # 便签列表
        self.is_memo_list_open = True
        self.memo_list_window = MemoListWindow(self)

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

    def delete_file(self, file_path):
        """删除文件"""
        try:
            os.remove(file_path)
            # print(f"{file_path} 文件已成功删除")
        except FileNotFoundError:
            print(f"文件 {file_path} 不存在")
        except Exception as e:
            print(f"删除 {file_path} 文件时出现错误: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    memo_app = MemoApp()
    sys.exit(app.exec_())
