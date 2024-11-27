import sys
from PySide6.QtWidgets import QApplication
from capture import canvas


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = canvas()
    window.show()
    sys.exit(app.exec())
