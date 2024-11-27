from PySide6.QtWidgets import QApplication, QMainWindow, QToolTip
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QColor, QPen


class canvas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)
        self.showFullScreen()
        self.startPoint = None
        self.finishPoint = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(0, 0, 0, 150))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())
        
        if self.startPoint and self.finishPoint:
            rectGeometry = QRect(self.startPoint, self.finishPoint)
            pen = QPen()
            pen.setColor(QColor(0, 255, 255))
            pen.setWidth(2)
            pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(QColor(0, 0, 255, 30))

            painter.drawRect(rectGeometry)

    def mouseMoveEvent(self, event):
        if self.startPoint:
            mousePosition = event.position()
            self.finishPoint = mousePosition.toPoint()
            self.update()
            toolTipPosition = self.mapToGlobal(mousePosition.toPoint())
            toolTipPosition.setX(toolTipPosition.x() + 10)
            toolTipPosition.setY(toolTipPosition.y() - 60)
            QToolTip.showText(toolTipPosition, f'X: {int(mousePosition.x())}\nY: {int(mousePosition.y())}')

    def mousePressEvent(self, event):
        mousePosition = event.position()
        self.finishPoint = None
        self.startPoint = mousePosition.toPoint()
        self.update()
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
