from PyQt6.QtWidgets import QVBoxLayout, QLabel, QDialog
from PyQt6.QtCore import Qt

class LoadingDialog(QDialog):
    def __init__(self,toggle_status,text):
        super().__init__()
        self.toggle_status = toggle_status
        self.setFixedSize(450, 200)
        self.setStyleSheet("""
                    font-family: "Verdana";
                    font-size: 14px;
                    font-weight: bold;
                """)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        layout = QVBoxLayout()
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)
        if toggle_status == False:
            self.setStyleSheet('background-color:white;'
                               'color:black')
        else:
            self.setStyleSheet('color:white')