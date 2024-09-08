from PyQt6.QtWidgets import (QMainWindow, QLineEdit, QPushButton, QSizePolicy, QVBoxLayout, QWidget, QHBoxLayout,
                             QCompleter, QApplication, QSpacerItem, QLabel, QDialog)
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCore import Qt
from seleniumbase import Driver
from qtoggle import QToggle
from selenium_commands import SeCommands
from windows.journal_list import JournalList
from windows.themes import apply_dark_theme, apply_light_theme, main_theme, set_placeholder_text_color
from json_comands import add_user, read_credentials
import sys
from windows.load_dialog import LoadingDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setup_window()
        self.create_widgets()
        self.setup_layout()
        self.setup_connections()

    def setup_window(self):
        self.setFixedWidth(400)
        self.setFixedHeight(300)
        self.setWindowTitle("NZ.UA")
    def create_widgets(self):
        self.input_login = QLineEdit()
        self.input_login.setPlaceholderText("Введіть логін")
        self.setup_widget(self.input_login)
        set_placeholder_text_color(self.input_login, QColor("#000"))

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Введіть пароль")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        completer = QCompleter(self.logins())
        self.input_login.setCompleter(completer)
        completer.popup().setStyleSheet("QListView { font-size: 14px; background-color: #8490f4; }")
        completer.activated.connect(self.on_login_selected)
        set_placeholder_text_color(self.input_password, QColor("#000"))
        self.setup_widget(self.input_password)

        self.login = QPushButton('Увійти')
        self.login.setFixedHeight(50)
        self.login.setStyleSheet("font-size: 16px;")
        self.login.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.toggle = QToggle()
        self.toggle_theme(self.toggle.isChecked())
        self.toggle.clicked.connect(self.toggle_theme)
        self.error_label = QLabel()

    def toggle_theme(self, checked):
        main_theme(self)
        if checked:
            apply_dark_theme(self)
        else:
            apply_light_theme(self)

    def setup_connections(self):
        self.login.clicked.connect(self.on_login_clicked)

    def setup_widget(self, widget):
        widget.setFixedHeight(40)
        widget.setStyleSheet("font-size: 14px;")

    def setup_layout(self):
        self.container = QWidget()
        layout = QVBoxLayout(self.container)
        hbox = QHBoxLayout()
        layout.addWidget(self.input_login)
        layout.addSpacerItem(QSpacerItem(100, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        layout.addWidget(self.input_password)
        layout.addLayout(hbox)
        hbox.addWidget(self.toggle)
        hbox.addWidget(self.login)
        hbox.addSpacerItem(QSpacerItem(100, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))
        error_label_hbox = QHBoxLayout()
        error_label_hbox.addStretch(1)
        error_label_hbox.addWidget(self.error_label)
        error_label_hbox.addStretch(1)
        layout.addLayout(error_label_hbox)
        self.error_label.setStyleSheet("""
            font-size:16px;
            font-weight:bold;
            color: red;
        """)
        self.central_widget = QWidget()
        self.central_layout = QHBoxLayout(self.central_widget)
        self.central_layout.addStretch(1)
        self.central_layout.addWidget(self.container)
        self.central_layout.addStretch(1)
        self.setCentralWidget(self.central_widget)

    def logins(self):
        credentials = read_credentials('main/credentials.json')
        return [cred['login'] for cred in credentials.values()]

    def on_login_selected(self, login):
        for user in read_credentials('main/credentials.json').values():
            if user['login'] == login:
                self.input_password.setText(user['password'])

    def on_login_clicked(self):
        if self.input_login.text() and self.input_password.text():
            self.hide()
            login = self.input_login.text()
            password = self.input_password.text()

            self.loading_dialog = LoadingDialog(toggle_status=self.toggle.isChecked(),text="Почекайте, відбувається підключення до сайту")
            self.loading_dialog.show()
            QApplication.processEvents()

            self.driver = Driver(undetectable=True,headless2=True)
            self.selenium_functions = SeCommands(self.driver)
            login_success = self.selenium_functions.open_site(login=login, password=password)
            self.loading_dialog.close()


            if login_success:
                add_user(login=login, password=password, credentials_path='main/credentials.json')
                toggle_status = self.toggle.isChecked()
                self.close()
                self.second_window = JournalList(self.selenium_functions, toggle_status)
                self.second_window.show()
            else:
                self.selenium_functions.close()
                self.show()
                self.repaint()
                self.show_error('Неправильний логін або пароль')
        else:
            self.show_error('Введіть ваш логін та пароль')

    def show_error(self, message):
        self.error_label.setText(message)
        self.input_login.clear()
        self.input_password.clear()

    def resizeEvent(self, event):
        window_height = self.central_widget.height()
        window_width = self.central_widget.width()
        self.container.setFixedHeight(int(window_height * 0.8))
        self.container.setFixedWidth(int(window_width * 0.8))
        super().resizeEvent(event)

    def closeEvent(self, event):
        self.close()
        event.accept()


