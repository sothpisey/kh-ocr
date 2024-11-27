from PySide6.QtWidgets import QApplication, QMainWindow, QToolTip
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor


class canvas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.8)
        self.showFullScreen()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(0, 0, 0, 150))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())
        painter.end()

    def mouseMoveEvent(self, event):
        mousePosition = event.position()
        position = self.mapToGlobal(mousePosition.toPoint())
        position.setX(position.x() + 10)
        position.setY(position.y() - 60)
        QToolTip.showText(position, f'X: {int(mousePosition.x())}\nY: {int(mousePosition.y())}')

    def mousePressEvent(self, event):
        mousePosition = event.position()
        print(f'Press Position: x = {mousePosition.x()}, y = {mousePosition.y()}')

    def mouseReleaseEvent(self, event):
        mousePosition = event.position()
        print(f'Release Position: x = {mousePosition.x()}, y = {mousePosition.y()}')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Q:
            self.close()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = canvas()
    sys.exit(app.exec())
