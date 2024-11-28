import sys
from PySide6.QtWidgets import QApplication
from drawing_gui import Canvas


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Canvas()
    window.show()
    sys.exit(app.exec())
