import sys
from PySide6.QtWidgets import QApplication
from capture_gui import CaptureWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CaptureWindow()
    window.showFullScreen()
    sys.exit(app.exec())
