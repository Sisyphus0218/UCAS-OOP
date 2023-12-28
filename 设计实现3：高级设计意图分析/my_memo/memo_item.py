from PIL import Image
from io import BytesIO
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
)
from PyQt5.QtGui import (
    QFont,
    QPixmap,
)

"""
便签项

MemoItem 便签项: 便签列表的组成部分
"""


class MemoItem(QWidget):
    """
    便签项

    便签列表的组成部分
    """

    def __init__(self, memo_name, memo_title, memo_content, memo_image):
        super().__init__()

        # 便签名字
        self.memo_name = memo_name

        # 便签项布局
        self.init_gui(memo_title, memo_content, memo_image)

    def init_gui(self, memo_title, memo_content, memo_image):
        """组件布局"""
        # 水平布局, 左边为文字, 右边为图片
        self.layout = QHBoxLayout(self)

        # 垂直布局, 上方为标题、下方为内容
        self.text_layout = QVBoxLayout()

        # 标题
        if not memo_title:
            memo_title = "new memo"
        self.title_label = QLabel(memo_title, self)
        font = QFont("Microsoft YaHei", 12)
        font.setBold(True)
        self.title_label.setFont(font)
        self.text_layout.addWidget(self.title_label)

        # 内容
        if memo_content:
            self.content_label = QLabel(memo_content, self)
            font = QFont("Microsoft YaHei", 10)
            self.content_label.setFont(font)
            self.text_layout.addWidget(self.content_label)

        # 将标题、内容添加到垂直布局
        self.layout.addLayout(self.text_layout)

        # 图片
        if memo_image:
            original_image = Image.open(memo_image)

            # 生成缩略图
            thumbnail_image = original_image.copy()
            thumbnail_image.thumbnail((100, 100))  # 设置缩略图的大小

            # 将缩略图转换为 QPixmap
            thumbnail_pixmap = self.image_to_pixmap(thumbnail_image)

            # 将图片添加到垂直布局
            self.image_label = QLabel(self)
            self.image_label.setPixmap(thumbnail_pixmap)
            self.image_label.setFixedSize(100, 100)
            self.layout.addWidget(self.image_label)

    def image_to_pixmap(self, image):
        """图片转pixmap"""
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.getvalue())
        return pixmap
