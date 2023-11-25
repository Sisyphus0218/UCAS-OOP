import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QColor, QPalette


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 创建一个标签
        self.label = QLabel("输入的文本：", self)

        # 创建一个多行文本框
        self.textEdit = QTextEdit(self)

        # 使用 QColor 设置多行文本框的背景颜色为浅绿色
        color = QColor(144, 238, 144)  # RGB颜色值，这里是浅绿色
        palette = QPalette()
        palette.setColor(QPalette.Base, color)
        self.textEdit.setPalette(palette)

        layout.addWidget(self.label)
        layout.addWidget(self.textEdit)

        self.setLayout(layout)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('PyQt 多行文本框例子')
        self.show()

    def onTextChanged(self):
        # 当文本框的文本发生变化时，这个槽函数会被调用
        text = self.textEdit.toPlainText()
        self.label.setText(f"输入的文本：{text}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec_())
