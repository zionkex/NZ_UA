import os
import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from windows.complete_lessson import LessonComplete
from windows.login_password import MainWindow

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    app.setWindowIcon(QIcon('main\images/logo.ico'))
    window = MainWindow()
    window.setWindowIcon(QIcon('main\images/logo.ico'))
    window.show()
    sys.exit(app.exec())
