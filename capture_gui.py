from PySide6.QtWidgets import QApplication, QMainWindow, QToolTip, QMenu, QFileDialog
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QAction, QIcon
from helper import ConfigManager, ImageUtility

class CaptureWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)
        #self.showFullScreen()
        self.startPoint = None
        self.finishPoint = None
        self.menu = None

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
        self.clear_screen()
        self.startPoint = mousePosition.toPoint()
        self.update()
        print(f'Press Position: x = {mousePosition.x()}, y = {mousePosition.y()}')

    def mouseReleaseEvent(self, event):
        ConfigManager.WriteConfig().capture(self.startPoint.x(),
                                            self.startPoint.y(),
                                            self.finishPoint.x(),
                                            self.finishPoint.y()
                                            )
        if self.menu:
            self.menu.close()

        mousePosition = event.position().toPoint()
        self.show_popup_menu(mousePosition)
        print(f'Release Position: x = {mousePosition.x()}, y = {mousePosition.y()}')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Q:
            self.close()

    def show_popup_menu(self, position: QPoint):
        if self.menu:
            self.menu.close()

        copy_image_action = QAction('Copy image', self)
        save_image_action = QAction('Save', self)
        capture_text_action = QAction('Capture Text', self)
        clear_action = QAction('Redo', self)
        exit_action = QAction('Exit', self)

        copy_image_action.triggered.connect(self.copy_image)
        save_image_action.triggered.connect(self.save_image)
        capture_text_action.triggered.connect(self.capture_text)
        clear_action.triggered.connect(self.clear_screen)
        exit_action.triggered.connect(self.exit_application)
        
        copy_image_action.setIcon(QIcon('./icon/copy_image.png'))
        save_image_action.setIcon(QIcon('./icon/save_image.png'))
        capture_text_action.setIcon(QIcon('./icon/capture.png'))
        clear_action.setIcon(QIcon('./icon/redo.png'))
        exit_action.setIcon(QIcon('./icon/exit.png'))
        
        repositionMenu = QPoint(position.x(), position.y() - 130)
        self.menu = QMenu(self)
        self.menu.aboutToHide.connect(self.clear_screen)
        self.menu.addAction(copy_image_action)
        self.menu.addAction(save_image_action)
        self.menu.addAction(capture_text_action)
        self.menu.addAction(clear_action)
        self.menu.addSeparator()
        self.menu.addAction(exit_action)
        self.menu.exec(repositionMenu)

    def copy_image(self):
        self.exit_application()
        ImageUtility.capture_screen_area(**ConfigManager.ReadConfig().capture())
        ImageUtility.image_to_clipboard(ConfigManager.ReadConfig().capture()['image_path'])

    def save_image(self):
        self.showMinimized()
        ImageUtility.capture_screen_area(**ConfigManager.ReadConfig().capture())
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save', 'image.png', 'Image (*.png)')
        if file_name:
            print(f'File will be saved to: {file_name}')
            with open('./capture.png', 'rb') as file:
                image_data = file.read()
                with open(file_name, 'wb') as out_file:
                    out_file.write(image_data)

    def capture_text(self):
        self.exit_application()
        ImageUtility.capture_screen_area(**ConfigManager.ReadConfig().capture())
        ImageUtility.image_to_text_clipboard()
    
    def clear_screen(self):
        if self.menu and not self.menu.isHidden():
            self.menu.close()
        self.startPoint, self.finishPoint = None, None
        self.update()
    
    def exit_application(self):
        self.close()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = CaptureWindow()
    window.showFullScreen()
    sys.exit(app.exec())
