import os
import time
import shutil
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (
    QMainWindow,
    QTextEdit,
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
    QColor,
    QPalette
)
from PyQt5.QtCore import QSize, Qt

from memo_item import MemoItem
from memo_setting_window import MemoSettingWindow

"""
便签

MemoListWindow 便签列表窗口: 显示便签列表, 新建、删除便签, 打开便签设置页面
MemoWindow 便签窗口: 文字排版、插入图片、新建便签、打开便签列表
"""


def singleton(cls):
    instances = {}

    def wrapper(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return wrapper


@singleton
class MemoListWindow(QMainWindow):
    """
    便签列表窗口

    显示便签列表, 新建、删除便签, 打开便签设置页面
    """

    def __init__(self, memo_app):
        super().__init__()

        # 便签程序
        self.memo_app = memo_app

        # 被选中的便签名字
        self.selected_memo = ""

        # 窗口布局
        self.init_gui()

    def init_gui(self):
        """窗口布局"""
        # 窗口名
        self.setWindowTitle("便签列表")

        # 窗口图标
        self.setWindowIcon(QIcon("icon/journals.png"))

        # 窗口大小
        self.resize(450, 450)

        # 工具栏和便签列表
        self.set_tool_bar()
        self.set_memo_list()
        self.addToolBar(self.tool_bar)
        self.setCentralWidget(self.memo_list)

        # 显示窗口
        self.show()

    def set_tool_bar(self):
        """工具栏布局"""
        # 工具栏
        self.tool_bar = QToolBar()
        self.tool_bar.setMovable(False)
        self.tool_bar.setIconSize(QSize(32, 32))

        # 新建便签
        self.new_action = QAction(
            QIcon("icon/plus-circle.png"), "新建<br>Ctrl+N", self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.triggered.connect(self.new_memo)
        self.tool_bar.addAction(self.new_action)

        # 删除便签
        self.delete_action = QAction(
            QIcon("icon/x-circle.png"), "删除<br>Del", self)
        self.delete_action.setShortcut("Del")
        self.delete_action.triggered.connect(self.delete_memo)
        self.tool_bar.addAction(self.delete_action)

        # 设置
        self.setting_action = QAction(QIcon("icon/gear.png"), "设置", self)
        self.setting_action.triggered.connect(self.show_setting)
        self.tool_bar.addAction(self.setting_action)

    def insert_memo_item(self, memo_item):
        """插入便签项"""
        list_item = QListWidgetItem()
        list_item.setSizeHint(memo_item.sizeHint())  # 设置项的大小
        list_item.setBackground(QColor(227, 226, 225))  # 使用浅灰色背景
        self.memo_list.addItem(list_item)
        self.memo_list.setItemWidget(list_item, memo_item)

    def load_memo_list(self):
        """将便签加载到便签列表"""
        self.memo_list.clear()
        self.memo_list.setSpacing(5)
        for memo_name in self.memo_app.memo_info:
            memo_title = self.memo_app.memo_info[memo_name]["abstract"]["title"]
            memo_content = self.memo_app.memo_info[memo_name]["abstract"]["content"]
            memo_image = self.memo_app.memo_info[memo_name]["abstract"]["first_image"]
            memo_item = MemoItem(memo_name, memo_title,
                                 memo_content, memo_image)
            self.insert_memo_item(memo_item)

    def set_memo_list(self):
        """便签列表布局"""
        # 便签列表
        self.memo_list = QListWidget()

        # 将便签加载到便签列表
        self.load_memo_list()

        # 双击列表项, 绑定选择便签事件
        self.memo_list.itemDoubleClicked.connect(self.select_memo)

    def cal_memo_pos(self):
        """计算便签的位置"""
        distance_right = self.memo_app.get_distance(self)
        if distance_right < 480:
            pos_bias = -480
        else:
            pos_bias = 480

        new_pos_x = self.geometry().x() + pos_bias
        new_pos_y = self.geometry().y()

        return new_pos_x, new_pos_y

    def new_memo(self):
        """新建便签"""
        # 以时间戳作为便签名
        current_time = time.strftime("%Y%m%d%H%M%S")
        file_name = "note" + current_time + ".html"
        file_path = "memo/" + file_name
        self.selected_memo = file_name

        # 在便签列表插入新建的便签项
        memo_name = file_name
        memo_title = ""
        memo_content = ""
        memo_image = ""
        memo_item = MemoItem(memo_name, memo_title, memo_content, memo_image)
        self.insert_memo_item(memo_item)

        # 将这个便签加入MemoApp字典
        pos_x, pos_y = self.cal_memo_pos()
        memo_window = MemoWindow(
            self.selected_memo, self.memo_app, pos_x, pos_y)
        self.memo_app.memo_windows[self.selected_memo] = memo_window

        # 在文本框加载便签内容
        file = open(file_path, "w")
        with open(file_path, "r") as file:
            content = file.read()
            memo_window.text_box.setHtml(content)

        # 便签数目加1
        self.memo_app.memo_num += 1

        # 添加便签信息
        self.memo_app.memo_info[self.selected_memo] = {
            "image": [],
            "abstract": {"title": "", "content": "", "first_image": ""},
        }

    def delete_memo(self):
        """删除便签"""
        # 若没有选中便签, 直接返回
        selected_items = self.memo_list.selectedItems()
        if not selected_items:
            return

        # 获取选中的便签名
        for item in selected_items:
            if isinstance(item, QListWidgetItem):
                memo_item = self.centralWidget().itemWidget(item)
                if isinstance(memo_item, MemoItem):
                    self.selected_memo = memo_item.memo_name

        # 从便签列表删除便签项
        for item in selected_items:
            self.memo_list.takeItem(self.memo_list.row(item))

        # 若便签已经被打开, 还需要关闭便签窗口
        if self.selected_memo in self.memo_app.memo_windows:
            close_window = self.memo_app.memo_windows[self.selected_memo]
            del self.memo_app.memo_windows[self.selected_memo]
            close_window.close()

        # 删除便签文件
        file_path = "memo/" + self.selected_memo
        self.memo_app.delete_file(file_path)

        # 便签数目减1
        self.memo_app.memo_num -= 1

        # 根据便签信息删除图片
        if self.memo_app.memo_info[self.selected_memo]["image"]:
            for image_filename in self.memo_app.memo_info[self.selected_memo]["image"]:
                image_path = "assets/" + image_filename
                self.memo_app.delete_file(image_path)

        # 删除便签信息
        del self.memo_app.memo_info[self.selected_memo]

        # 保存便签信息
        self.memo_app.save_memo_info()

    def select_memo(self, item):
        """选择便签"""
        # 获取选中的便签
        if isinstance(item, QListWidgetItem):
            memo_item = self.centralWidget().itemWidget(item)
            if isinstance(memo_item, MemoItem):
                self.selected_memo = memo_item.memo_name

        # 若便签已经被打开, 直接显示, 否则加载便签
        if self.selected_memo in self.memo_app.memo_windows:
            self.memo_app.memo_windows[self.selected_memo].showNormal()
        else:
            self.load_memo()

    def load_memo(self):
        """加载便签"""
        # 新建便签窗口, 加入便签窗口字典
        pos_x, pos_y = self.cal_memo_pos()
        memo_window = MemoWindow(
            self.selected_memo, self.memo_app, pos_x, pos_y)
        self.memo_app.memo_windows[self.selected_memo] = memo_window

        # 加载相应的便签文件
        file_path = "memo/" + self.selected_memo
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            memo_window.text_box.setHtml(content)

    def show_setting(self):
        """打开设置窗口"""
        pos_x, pos_y = self.cal_memo_pos()
        self.memo_app.memo_setting_window = MemoSettingWindow(
            self.memo_app, pos_x, pos_y)
        self.memo_app.memo_setting_window.showNormal()

    def closeEvent(self, event):
        """关闭便签列表窗口"""
        # 设置 is_memo_list_open 为 False
        self.memo_app.is_memo_list_open = False

        # 关闭窗口
        self.close()


class MemoWindow(QMainWindow):
    """
    便签窗口

    文字排版、插入图片、新建便签、打开便签列表
    """

    def __init__(self, memo_name, memo_app, pos_x, pos_y):
        super().__init__()

        # 便签程序
        self.memo_app = memo_app

        # 便签名字
        self.memo_name = memo_name

        # 窗口布局
        self.init_gui(pos_x, pos_y)

    def init_gui(self, pos_x, pos_y):
        """窗口布局"""
        # 窗口名
        self.setWindowTitle("便签")

        # 窗口图标
        self.setWindowIcon(QIcon("icon/journal-richtext.png"))

        # 窗口位置和大小
        pos_x, pos_y
        self.setGeometry(pos_x, pos_y, 450, 450)

        # 窗口颜色
        color = self.memo_app.setting_info["background"]["rgb"]
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(color[0], color[1], color[2]))
        self.setPalette(palette)

        # 窗口透明度
        opacity_value = self.memo_app.setting_info["opacity"]
        self.setWindowOpacity(opacity_value)

        # 工具栏和文本框
        self.set_tool_bar()
        self.set_text_box()
        self.addToolBar(self.tool_bar)
        self.setCentralWidget(self.text_box)

        # 显示窗口
        self.show()

    def set_tool_bar(self):
        """工具栏布局"""
        # 工具栏
        self.tool_bar = QToolBar()
        self.tool_bar.setMovable(False)
        self.tool_bar.setIconSize(QSize(32, 32))  # 设置图标大小为32x32像素

        # 粗体
        self.bold_action = QAction(
            QIcon("icon/type-bold.png"), "粗体<br>Ctrl+B", self)
        self.bold_action.setShortcut("Ctrl+B")
        self.bold_action.triggered.connect(self.toggle_bold)
        self.tool_bar.addAction(self.bold_action)

        # 斜体
        self.italic_action = QAction(
            QIcon("icon/type-italic.png"), "斜体<br>Ctrl+I", self
        )
        self.italic_action.setShortcut("Ctrl+I")
        self.italic_action.triggered.connect(self.toggle_italic)
        self.tool_bar.addAction(self.italic_action)

        # 下划线
        self.underline_action = QAction(
            QIcon("icon/type-underline.png"), "下划线<br>Ctrl+U", self
        )
        self.underline_action.setShortcut("Ctrl+U")
        self.underline_action.triggered.connect(self.toggle_underline)
        self.tool_bar.addAction(self.underline_action)

        # 删除线
        self.overstrike_action = QAction(
            QIcon("icon/type-strikethrough.png"), "删除线<br>Ctrl+T", self
        )
        self.overstrike_action.setShortcut("Ctrl+T")
        self.overstrike_action.triggered.connect(self.toggle_strikeout)
        self.tool_bar.addAction(self.overstrike_action)

        # 分割线
        self.tool_bar.addSeparator()

        # 字体
        self.font_color_action = QAction(
            QIcon("icon/palette.png"), "字体颜色", self)
        self.font_color_action.triggered.connect(self.set_font_color)
        self.tool_bar.addAction(self.font_color_action)

        # 字号
        self.font_size_box = QSpinBox(self)
        self.font_size_box.setValue(12)
        self.font_size_box.setStyleSheet(
            "QSpinBox { width: 50px; height: 28px; }")
        self.font_size_box.valueChanged.connect(self.set_font_size)
        self.tool_bar.addWidget(self.font_size_box)

        # 分割线
        self.tool_bar.addSeparator()

        # 添加图片
        self.add_image_action = QAction(QIcon("icon/image.png"), "添加图片", self)
        self.add_image_action.triggered.connect(self.add_image)
        self.tool_bar.addAction(self.add_image_action)

        # 分割线
        self.tool_bar.addSeparator()

        # 打开便签列表
        self.open_memo_list_window_action = QAction(
            QIcon("icon/card-list.png"), "打开便签列表", self
        )
        self.open_memo_list_window_action.triggered.connect(
            self.open_memo_list_window)
        self.tool_bar.addAction(self.open_memo_list_window_action)

        # 新建便签
        self.new_memo_action = QAction(
            QIcon("icon/plus-circle.png"), "新建便签<br>Ctrl+N", self
        )
        self.new_memo_action.setShortcut("Ctrl+N")
        self.new_memo_action.triggered.connect(self.new_memo)
        self.tool_bar.addAction(self.new_memo_action)

        # 便签置顶
        self.top_memo_action = QAction(
            QIcon("icon/arrow-bar-up.png"), "置顶便签", self
        )
        self.top_memo_action.triggered.connect(self.top_memo)
        self.tool_bar.addAction(self.top_memo_action)

    def set_text_box(self):
        """文本框布局"""
        self.text_box = QTextEdit(self, placeholderText="开始记录...")
        font = QFont("微软雅黑", 12)
        self.text_box.setFont(font)

        color = self.memo_app.setting_info["background"]["rgb"]
        palette = QPalette()
        palette.setColor(QPalette.Base, QColor(color[0], color[1], color[2]))
        self.text_box.setPalette(palette)

    def toggle_bold(self):
        """粗体"""
        cursor = self.text_box.textCursor()

        # 若没选中, 直接返回
        if not cursor.hasSelection():
            return

        # 所选范围
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        # 选中第一个字符, 判断是否为粗体
        cursor.setPosition(start)
        cursor.setPosition(start + 1, QTextCursor.KeepAnchor)
        char_format = cursor.charFormat()
        is_first_char_bold = char_format.font().bold()

        # 重新选中原来的文本, 若第一个字符为粗体, 就取消粗体, 反之加粗
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        char_format = cursor.charFormat()
        font = char_format.font()
        font.setBold(not is_first_char_bold)
        char_format.setFont(font)
        cursor.setCharFormat(char_format)
        self.text_box.setTextCursor(cursor)

    def toggle_italic(self):
        """斜体"""
        cursor = self.text_box.textCursor()

        # 若没选中, 直接返回
        if not cursor.hasSelection():
            return

        # 所选范围
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        # 选中第一个字符, 判断是否为斜体
        cursor.setPosition(start)
        cursor.setPosition(start + 1, QTextCursor.KeepAnchor)
        char_format = cursor.charFormat()
        is_first_char_italic = char_format.font().italic()

        # 重新选中原来的文本, 若第一个字符为斜体, 就取消斜体, 反之加上斜体
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        char_format = cursor.charFormat()
        font = char_format.font()
        font.setItalic(not is_first_char_italic)
        char_format.setFont(font)
        cursor.setCharFormat(char_format)
        self.text_box.setTextCursor(cursor)

    def toggle_underline(self):
        """下划线"""
        cursor = self.text_box.textCursor()

        # 若没选中, 直接返回
        if not cursor.hasSelection():
            return

        # 所选范围
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        # 选中第一个字符, 判断是否有下划线
        cursor.setPosition(start)
        cursor.setPosition(start + 1, QTextCursor.KeepAnchor)
        char_format = cursor.charFormat()
        is_first_char_underline = char_format.fontUnderline()

        # 重新选中原来的文本, 若第一个字符有下划线, 就取消下划线, 反之加上下划线
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        char_format = cursor.charFormat()
        font = char_format.font()
        font.setUnderline(not is_first_char_underline)
        char_format.setFont(font)
        cursor.setCharFormat(char_format)
        self.text_box.setTextCursor(cursor)

    def toggle_strikeout(self):
        """删除线"""
        cursor = self.text_box.textCursor()

        # 若没选中, 直接返回
        if not cursor.hasSelection():
            return

        # 所选范围
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        # 选中第一个字符, 判断是否有删除线
        cursor.setPosition(start)
        cursor.setPosition(start + 1, QTextCursor.KeepAnchor)
        char_format = cursor.charFormat()
        is_first_char_strikeout = char_format.fontStrikeOut()

        # 重新选中原来的文本, 若第一个字符有删除线, 就取消删除线, 反之加上删除线
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        char_format = cursor.charFormat()
        font = char_format.font()
        font.setStrikeOut(not is_first_char_strikeout)
        char_format.setFont(font)
        cursor.setCharFormat(char_format)
        self.text_box.setTextCursor(cursor)

    def add_image(self):
        """添加图片"""
        file_dialog = QFileDialog()
        image_file, _ = file_dialog.getOpenFileName(
            self, "选择图片", "", "Images (*.png *.jpg *.jpeg *.gif *.bmp)"
        )

        if image_file:
            # 生成时间戳, 重命名图片, 防止图片重名
            current_time = time.strftime("%Y%m%d%H%M%S")

            # 复制图片文件到assets文件夹
            image_filename = os.path.basename(image_file)
            new_image_filename = current_time + "-" + image_filename
            destination_path = "assets/" + new_image_filename
            shutil.copy(image_file, destination_path)

            image = QImage(destination_path)
            image_format = QTextImageFormat()
            image_format.setName(destination_path)

            # 设置图片的宽度和高度
            scale_factor = 300.0 / image.height()
            image_format.setWidth(image.width() * scale_factor)
            image_format.setHeight(image.height() * scale_factor)

            # 插入图片
            cursor = self.text_box.textCursor()
            cursor.insertImage(image_format)

            # 添加到便签信息
            self.memo_app.memo_info[self.memo_name]["image"].append(
                new_image_filename)

    def set_font_color(self):
        """设置文字颜色"""
        cursor = self.text_box.textCursor()

        # 打开颜色选择对话框
        color_dialog = QColorDialog(self)
        color = color_dialog.getColor()

        # 若没选中, 直接返回
        if not cursor.hasSelection():
            return

        # 设置文本颜色
        char_format = QTextCharFormat()
        char_format.setForeground(color)
        cursor.mergeCharFormat(char_format)

    def set_font_size(self):
        """设置文字大小"""
        value = self.font_size_box.value()
        self.text_box.setFontPointSize(value)

    def open_memo_list_window(self):
        """打开便签列表"""
        self.memo_app.memo_list_window = MemoListWindow(self.memo_app)
        self.memo_app.memo_list_window.showNormal()

        if not self.memo_app.is_memo_list_open:
            self.memo_app.is_memo_list_open = True

    def cal_memo_pos(self):
        """计算便签的位置"""
        distance_right = self.memo_app.get_distance(self)
        if distance_right < 480:
            pos_bias = -480
        else:
            pos_bias = 480

        new_pos_x = self.geometry().x() + pos_bias
        new_pos_y = self.geometry().y()

        return new_pos_x, new_pos_y

    def new_memo(self):
        """新建便签"""
        # 以时间戳作为便签名
        current_time = time.strftime("%Y%m%d%H%M%S")
        file_name = "note" + current_time + ".html"
        file_path = "memo/" + file_name

        # 若便签列表打开了, 在便签列表插入新建的便签
        if self.memo_app.is_memo_list_open:
            self.memo_app.memo_list_window.memo_list.selected_memo = file_name
            memo_name = file_name
            memo_title = ""
            memo_content = ""
            memo_image = ""
            memo_item = MemoItem(memo_name, memo_title,
                                 memo_content, memo_image)
            self.memo_app.memo_list_window.insert_memo_item(memo_item)

        # 将这个便签加入MemoApp字典
        pos_x, pos_y = self.cal_memo_pos()
        memo_window = MemoWindow(file_name, self.memo_app, pos_x, pos_y)
        self.memo_app.memo_windows[file_name] = memo_window

        # 在文本框加载便签内容
        file = open(file_path, "w")
        with open(file_path, "r") as file:
            content = file.read()
            memo_window.text_box.setHtml(content)

        # 便签数目加1
        self.memo_app.memo_num += 1

        # 添加便签信息
        self.memo_app.memo_info[file_name] = {
            "image": [],
            "abstract": {"title": "", "content": "", "first_image": ""},
        }

    def top_memo(self):
        """置顶便签"""
        # 获取当前窗口标志
        flags = self.windowFlags()

        # 判断是否已经置顶
        if flags & Qt.WindowStaysOnTopHint:
            # 取消置顶
            self.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
        else:
            # 设置置顶
            self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)

        # 使窗口标志生效
        self.show()

    def save_memo(self):
        """保存便签"""
        # 保存便签信息
        self.memo_app.save_memo_info()

        # 保存便签文件
        text = self.text_box.toHtml()
        file_path = "memo/" + self.memo_name
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)

    def parse_memo(self):
        """解析便签, 获取便签摘要"""
        # 获取文本框中的HTML内容
        html_text = self.text_box.toHtml()

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html_text, "html.parser")

        # 获取所有文本内容
        text = soup.get_text()

        # 分割文本成行
        lines = text.split("\n")

        # 获取第一行和第二行文本, 限制字数不超过12
        first_line = ""
        second_line = ""
        is_first_line_found = False
        for line in lines:
            if line != "":
                if not is_first_line_found:
                    first_line = line
                    is_first_line_found = True
                else:
                    second_line = line
                    break

        if len(first_line) > 12:
            first_line = first_line[:12]
        if len(second_line) > 12:
            second_line = second_line[:12]

        # 查找第一个图片标签并提取图片
        images = soup.findAll("img")
        first_image_src = ""
        if images:
            first_image_src = images[0]["src"]

        # 保存便签信息
        self.memo_app.memo_info[self.memo_name]["abstract"]["title"] = first_line
        self.memo_app.memo_info[self.memo_name]["abstract"]["content"] = second_line
        self.memo_app.memo_info[self.memo_name]["abstract"][
            "first_image"
        ] = first_image_src

    def closeEvent(self, event):
        """关闭便签窗口, 若便签为空自动删除"""
        content = self.text_box.toPlainText()

        # 若窗口在被打开的窗口中（若不在说明已经被便签列表删除了, 直接关闭窗口）
        if self.memo_name in self.memo_app.memo_windows:
            # 若便签为空
            if not content:
                # 若便签列表被打开, 需要在便签列表中删除相应便签项
                if self.memo_app.is_memo_list_open:
                    # 在便签列表中定位这个便签项
                    for i in range(self.memo_app.memo_list_window.memo_list.count()):
                        item = self.memo_app.memo_list_window.memo_list.item(i)
                        widget = self.memo_app.memo_list_window.memo_list.itemWidget(
                            item
                        )
                        if (
                            isinstance(widget, MemoItem)
                            and widget.memo_name == self.memo_name
                        ):
                            # 在便签列表删除便签项
                            self.memo_app.memo_list_window.memo_list.takeItem(
                                i)
                            break

                # 删除便签带有的图片
                if self.memo_app.memo_info[self.memo_name]["image"]:
                    for image_filename in self.memo_app.memo_info[self.memo_name][
                        "image"
                    ]:
                        image_path = "assets/" + image_filename
                        self.memo_app.delete_file(image_path)

                # 删除便签信息
                del self.memo_app.memo_info[self.memo_name]
                self.save_memo()

                # 删除文件
                file_path = "memo/" + self.memo_name
                self.memo_app.delete_file(file_path)

                # 便签数目减1
                self.memo_app.memo_num -= 1

            # 若便签不为空
            else:
                # 保存便签
                self.save_memo()

                # 若便签列表被打开, 更新便器列表
                if self.memo_app.is_memo_list_open:
                    self.parse_memo()
                    self.save_memo()
                    self.memo_app.memo_list_window.load_memo_list()

            # 从字典中删除便签
            del self.memo_app.memo_windows[self.memo_name]

        # 关闭窗口
        self.close()
