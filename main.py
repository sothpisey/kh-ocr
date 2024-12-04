import sys
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QLabel, QWidgetAction, QWidget
from PySide6.QtCore import QPoint
from setting_gui import SettingWindow
from capture_gui import CaptureWindow
from helper import ConfigManager


class SystemTray:
    def __init__(self, app):
        self.app = app
        self.tray = QSystemTrayIcon()
        self.menu = QMenu()
        self.setting_window = SettingWindow()
        self.capture_window = CaptureWindow()
        self.language_label_action = None

        self._setup_tray()
        self._setup_actions()
        self._setup_menu()
        self._connect_signals()

    def _setup_tray(self):
        self.tray.setIcon(QIcon('./icon/app_icon.png'))
        self.tray.setVisible(True)
        self.tray.setToolTip('KH-OCR')
        self.tray.activated.connect(self._on_tray_activated)

    def _setup_actions(self):
        self.setting_action = QAction('Setting', self.menu)
        self.capture_action = QAction('Capture', self.menu)
        self.quit_action = QAction('Quit', self.menu)

        self.setting_action.setIcon(QIcon('./icon/setting.png'))
        self.capture_action.setIcon(QIcon('./icon/capture.png'))
        self.quit_action.setIcon(QIcon('./icon/exit.png'))

        self.setting_action.triggered.connect(self._toggle_setting_window)
        self.capture_action.triggered.connect(self._toggle_capture_window)
        self.quit_action.triggered.connect(self.app.quit)

    def _setup_menu(self):
        self.language_label_action = self._add_label_to_menu(self.menu, SettingWindow().check_config_language())
        self.menu.addAction(self.setting_action)
        self.menu.addAction(self.capture_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)

    def _connect_signals(self):
        self.setting_window.applied.connect(self._update_label)

    def _toggle_setting_window(self):
        if self.setting_window:
            if self.setting_window.isVisible():
                self.setting_window.hide()
            else:
                self.setting_window.show()

    def _toggle_capture_window(self):
        if self.capture_window:
            if self.capture_window.isVisible():
                self.capture_window.hide()
            else:
                self.capture_window.showFullScreen()

    def _on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.Context:
            self.menu.exec(self.tray.geometry().bottomLeft() + QPoint(-120, -86))

    def _add_label_to_menu(self, menu, label_text):
        label = QLabel(label_text)
        label.setStyleSheet('padding: 4px; color: White; font-weight: bold;')

        label_action = QWidgetAction(menu)
        label_action.setDefaultWidget(label)
        menu.addAction(label_action)
        return label_action

    def _update_label(self, selected_language):
        new_language = selected_language
        if self.language_label_action:
            label_widget = self.language_label_action.defaultWidget()
            if isinstance(label_widget, QLabel):
                label_widget.setText(new_language)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    system_tray = SystemTray(app)
    sys.exit(app.exec())
