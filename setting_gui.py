import sys
from PySide6.QtWidgets import QApplication, QLabel, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QFormLayout, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from helper import ConfigManager

class SettingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Settings')
        self.setWindowIcon(QIcon('./icon/setting.png'))
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)


        self.language_selector = QComboBox()
        self.language_selector.addItems(['Khmer', 'English'])
        self.language_selector.setCurrentText(self.check_config_language())

        form_layout = QFormLayout()
        form_layout.addRow('Language:', self.language_selector)

        self.cancel_button = QPushButton('Cancel')
        self.apply_button = QPushButton('Apply')

        self.cancel_button.clicked.connect(self.on_cancel_clicked)
        self.apply_button.clicked.connect(self.on_apply_clicked)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.apply_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def check_config_language(self) -> str:
        if ConfigManager.ReadConfig().ocr()['language'] == 'khm':
            return 'Khmer'
        elif ConfigManager.ReadConfig().ocr()['language'] == 'eng':
            return 'English'

    def on_cancel_clicked(self) -> None:
        self.close()

    def on_apply_clicked(self) -> None:
        selected_language = self.language_selector.currentText()

        if selected_language == 'Khmer':
            ConfigManager.WriteConfig().ocr(language='khm')
        elif selected_language == 'English':
            ConfigManager.WriteConfig().ocr(language='eng')

        QMessageBox.information(self, ' ', f'You changed to  {selected_language} language')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setting_window = SettingWindow()
    setting_window.show()
    sys.exit(app.exec())
