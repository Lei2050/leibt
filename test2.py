from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import uic
import sys

class UI(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("test.ui", self) # 加载窗口


app = QApplication(sys.argv)
window = UI()
window.show()

sys.exit(app.exec())
