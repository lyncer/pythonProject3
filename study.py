from PyQt5.QtWidgets import *
import sys

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

    def ui(self):
        self.resize(400,600)
        self.label = QLabel(self)
        self.label.setText('shit')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.ui()
    window.show()
    sys.exit(app.exec_())