import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QDesktopWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Window Distance from Screen Edges')
        self.setGeometry(100, 100, 400, 300)

        label = QLabel('This is the main window!', self)
        label.setGeometry(50, 50, 300, 200)

        # 获取屏幕的几何信息
        screen_geometry = QDesktopWidget().screenGeometry()

        # 获取窗口的几何信息
        window_geometry = self.geometry()

        # 计算窗口相对于屏幕左边缘和右边缘的距离
        distance_left = window_geometry.x() - screen_geometry.x()
        distance_right = screen_geometry.width() - (window_geometry.x() + window_geometry.width())

        print("窗口相对于屏幕左边缘的距离：", distance_left)
        print("窗口相对于屏幕右边缘的距离：", distance_right)

def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
