
from PyQt6.QtWidgets import QMainWindow, QComboBox, QVBoxLayout, QWidget, QLabel, QApplication, QHBoxLayout, \
    QSpacerItem, QSizePolicy, QPushButton
from PyQt6.QtCore import Qt

from qtoggle import QToggle
from windows.complete_lessson import LessonComplete
from windows.themes import apply_dark_theme,apply_light_theme,main_theme
class JournalList(QMainWindow):
    def __init__(self,selenium_functions,toggle_status):

        super().__init__()
        self.selenium_functions=selenium_functions
        self.toggle_status =toggle_status
        self.init_ui()
        self.toggle_theme(self.toggle_status)

    def init_ui(self):
        self.setup_window()
        self.create_widgets()
        self.setup_layout()

    def setup_window(self):
        self.setFixedWidth(500)
        self.setFixedHeight(300)
        self.setWindowTitle("NZ.UA")

    def create_widgets(self):
        self.choice_label = QLabel('Виберіть потрібний предмет та клас')
        
        self.combo_box1 = QComboBox()
        self.combo_box1.addItem('Виберіть предмет')

        self.setup_widget(self.combo_box1)
        elements = self.selenium_functions.get_subject()
        # self.combo_box1.addItems([element.text.strip() for element in elements if element.text.strip()])

        for element in elements:
            if element.text.startswith('Інтегрований курс'):
                self.combo_box1.addItem(element[len('Інтегрований курс '):].strip())
            else:
                self.combo_box1.addItem(element.text.strip())
        self.combo_box2 = QComboBox()
        self.combo_box2.addItem("Виберіть клас")
        self.setup_widget(self.combo_box2)

        self.combo_box1.currentIndexChanged.connect(self.updateComboBox2)

        self.connect_button = QPushButton("Підключитись")
        self.connect_button.clicked.connect(self.connect_journal)
        self.setup_widget(self.connect_button)
        self.toggle = QToggle()
        self.toggle.setChecked(self.toggle_status)
        self.toggle.clicked.connect(self.toggle_theme)

    def updateComboBox2(self, index):
        selected_subject = self.combo_box1.itemText(index)
        class_list = self.selenium_functions.get_classes(selected_subject)
        self.combo_box2.clear()
        self.combo_box2.addItems(class_list)

    def connect_journal(self):
        self.hide()
        self.selenium_functions.connect_journal(self.combo_box1, self.combo_box2)
        toggle_status = self.toggle.isChecked()
        self.third_window = LessonComplete(
            selenium_functions=self.selenium_functions,
            toggle_status=toggle_status,
            second_window=self.open_second_window
)
        self.third_window.show()

    def setup_widget(self, widget):
        widget.setFixedHeight(40)
        widget.setStyleSheet("font-size: 14px;")

    def setup_layout(self):
        self.center_widget = QWidget()
        self.setCentralWidget(self.center_widget)

        vbox = QVBoxLayout(self.center_widget)
        vbox.addSpacerItem(QSpacerItem(50, 30, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))

        vbox.addWidget(self.choice_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        hbox = QHBoxLayout()
        hbox.addSpacerItem(QSpacerItem(50, 30, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        hbox.addWidget(self.combo_box1)
        hbox.addSpacerItem(QSpacerItem(50, 30, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        hbox.addWidget(self.combo_box2)
        hbox.addSpacerItem(QSpacerItem(50, 30, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        vbox.addSpacerItem(QSpacerItem(50, 30, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        vbox.addLayout(hbox)
        button_layout= QHBoxLayout()
        vbox.addStretch(1)
        button_layout.addSpacerItem(QSpacerItem(50, 30, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))

        button_layout.addWidget(self.toggle)
        button_layout.addStretch(1)


        button_layout.addWidget(self.connect_button, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addStretch(1)
        button_layout.addStretch(1)

        vbox.addLayout(button_layout)
        self.center_widget.setLayout(vbox)

    def toggle_theme(self, checked):
        main_theme(self)
        if checked:
            apply_dark_theme(self)
            self.choice_label.setStyleSheet("""
                                        color:#C0B6FC;
                                        font-size:18px;
                                        font-weight:bold;""")
        else:
            apply_light_theme(self)
            self.choice_label.setStyleSheet("""
                                        color:#6850FA;
                                        font-size:18px;
                                        font-weight:bold;""")

    def resizeEvent(self, event):
        height = self.height()
        self.center_widget.setFixedHeight(int(height * 0.9))
        super().resizeEvent(event)

    def closeEvent(self, event):
        self.close()
        self.selenium_functions.close()
        event.accept()

    def open_second_window(self, toggle_status):
        self.show()
        self.toggle_theme(toggle_status)
        self.toggle.setChecked(toggle_status)
