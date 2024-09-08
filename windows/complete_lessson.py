import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QComboBox, QPushButton, QLabel, QLineEdit, QWidget, \
    QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QCheckBox
from PyQt6.QtCore import Qt
from windows.themes import apply_dark_theme, apply_light_theme, main_theme
from qtoggle import QToggle
from windows.load_dialog import LoadingDialog


class LessonComplete(QMainWindow):
    def __init__(self,selenium_functions, toggle_status,second_window):
        super().__init__()
        self.second_window = second_window
        self.selenium_functions = selenium_functions
        self.toggle_status = toggle_status

        self.setWindowTitle("NZ.UA")
        self.setGeometry(400, 200, 400, 300)

        self.init_ui()

    def init_ui(self):
        self.setup_window()
        self.create_widgets()
        self.toggle_theme(self.toggle_status)
        self.setup_layout()

    def setup_window(self):
        self.setFixedWidth(500)
        self.setFixedHeight(300)
        self.setWindowTitle("NZ.UA")

    def create_widgets(self):
        self.back_button = QPushButton('Назад')
        self.back_button.clicked.connect(self.back_journals)
        self.file_select_button = QPushButton('Виберіть файл', self)
        self.file_select_button.clicked.connect(self.update_file_list)
        self.row_label = QLabel("Виберіть номер рядка:", self)
        self.column_label = QLabel("Виберіть номер стовпчика:", self)
        self.lesson_number_label = QLabel("Виберіть номер урока:", self)
        self.file_combo = QComboBox(self)
        self.file_combo.setFixedWidth(250)
        self.file_combo.currentIndexChanged.connect(self.check_extension)

        self.row_entry = QLineEdit(self)
        self.column_entry = QLineEdit(self)
        self.lesson_number_entry = QLineEdit(self)
        self.doc_button = QPushButton('Запустити', self)
        self.doc_button.clicked.connect(self.docx)
        self.doc_button.setMinimumSize(250, 40)
        self.toggle = QToggle()
        self.toggle.clicked.connect(self.toggle_theme)
        self.toggle.setChecked(self.toggle_status)
        self.check_homework_label = QLabel('Чи додавати домашнє завдання?')
        self.check_homework = QCheckBox()
        self.check_homework.setChecked(True)
        self.check_homework.stateChanged.connect(self.update_homework_label)
        self.homework_status_label = QLabel("Так")
        self.check_homework_label.hide()
        self.check_homework.hide()
        self.homework_status_label.hide()
        self.info_label=QLabel()

        self.update_info_label()
        self.error_label = QLabel()


    def update_info_label(self):
        journal_info_text = self.selenium_functions.journal_info()
        self.info_label.setText(journal_info_text)
    def setup_layout(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        file_select_layout = QHBoxLayout()
        seq_layout = QHBoxLayout()
        new_row_layout = QHBoxLayout()
        self.new_column_layout = QHBoxLayout()
        doc_button_layout = QHBoxLayout()

        self.setCentralWidget(main_widget)
        main_widget.setLayout(main_layout)
        main_layout.addWidget(self.info_label,alignment=Qt.AlignmentFlag.AlignHCenter)

        main_layout.addLayout(file_select_layout)
        file_select_layout.addWidget(self.back_button)
        main_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        file_select_layout.addWidget(self.file_select_button)
        main_layout.addLayout(seq_layout)
        seq_layout.addWidget(self.lesson_number_label)

        seq_layout.addSpacerItem(QSpacerItem(20, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        seq_layout.addWidget(self.lesson_number_entry)

        file_select_layout.addWidget(self.file_combo)

        main_layout.addLayout(new_row_layout)

        main_layout.addLayout(self.new_column_layout)

        self.new_column_layout.addWidget(self.column_label)

        self.new_column_layout.addWidget(self.check_homework_label)
        self.new_column_layout.addWidget(self.check_homework)
        self.new_column_layout.addWidget(self.homework_status_label)
        self.new_column_layout.addSpacerItem(QSpacerItem(20, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.new_column_layout.addWidget(self.column_entry)

        main_layout.addLayout(doc_button_layout)
        doc_button_layout.addWidget(self.toggle)
        doc_button_layout.addSpacerItem(QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        doc_button_layout.addWidget(self.doc_button)

        doc_button_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        main_layout.addWidget(self.error_label,alignment=Qt.AlignmentFlag.AlignHCenter)
        self.show()

    def update_file_list(self):
        initial_directory = "/path/to/directory"
        file_path, _ = QFileDialog.getOpenFileName(self, "Виберіть документ", initial_directory,
                                                   "Documents (*.doc *.docx *.xlsx *.xls);;All Files (*)")

        if file_path:
            file_name = os.path.basename(file_path)
            self.file_combo.insertItem(0, file_name, file_path)
            self.file_combo.setCurrentIndex(0)
            index = self.file_combo.findText(file_name)
            self.file_combo.setItemData(index, file_path)
   

    def back_journals(self):
        self.hide()
        self.loading_dialog = LoadingDialog(toggle_status=self.toggle.isChecked(),text="Почекайте пару секунд")
        # self.loading_dialog.show()
        # QApplication.processEvents()
        self.selenium_functions.back_to_journals()
        # self.loading_dialog.close()
        self.second_window(self.toggle.isChecked())


    def check_extension(self):
        file_path = self.file_combo.currentText()
        file_extension = file_path.split('.')[-1]
        self.clear_error(self.row_entry)
        self.clear_error(self.column_entry)
        self.row_entry.clear()

        self.column_entry.clear()

        if file_extension in ['xls', 'xlsx']:
            self.row_label.hide()
            self.row_entry.hide()
            self.column_entry.setText("1")
            self.column_label.hide()
            self.column_entry.hide()
            self.check_homework_label.show()
            self.check_homework.show()
            self.homework_status_label.show()
        elif file_extension in ['docx', 'doc']:
            self.check_homework_label.hide()
            self.check_homework.hide()
            self.homework_status_label.hide()
            self.column_label.show()
            self.column_entry.show()
            if file_extension =='doc':
                self.show_error('Обновіть ваш документ до формату DOCX')

        else:
            self.show_error('Виберіть файл Word або Excel')

        


    def docx(self):
        column_text =self.column_entry.text().strip()
        lesson_text = self.lesson_number_entry.text().strip()
        file_name = self.file_combo.currentText()
        file_path = self.file_combo.itemData(self.file_combo.findText(file_name))
        file_extension = file_name.split('.')[-1]
        homework_check = self.check_homework.isChecked()

        if column_text.isdigit() and lesson_text.isdigit():
            self.clear_error(self.lesson_number_entry)
            self.clear_error(self.column_entry)
            column = int(self.column_entry.text().strip())
            lesson_number = int(self.lesson_number_entry.text().strip())
        elif lesson_text.isdigit() and file_extension in ['xlsx','xls']:
            self.clear_error(self.lesson_number_entry)
            lesson_number = int(self.lesson_number_entry.text().strip())
            print(lesson_number)
            
        elif not column_text.isdigit() and not lesson_text.isdigit():
            self.show_error('Введіть цілі числа для обох полів')
            self.column_entry.setStyleSheet('background-color: #FA8D8D;')
            self.lesson_number_entry.setStyleSheet('background-color: #FA8D8D;')
            return

        elif not lesson_text.isdigit():
            self.clear_error(self.column_entry)
            self.show_error('Введіть ціле число для номера урока')
            self.lesson_number_entry.setStyleSheet('background-color: #FA8D8D;')
            return
        elif not column_text.isdigit():
        # and file_extension in ['docx','doc'] 
            self.clear_error(self.lesson_number_entry)
            self.show_error('Введіть ціле число для номера стовпчика')
            self.column_entry.setStyleSheet('background-color: #FA8D8D;')
            return
        self.hide()
        self.loading_dialog = LoadingDialog(toggle_status=self.toggle.isChecked(),text="Почекайте,відбувається заповнення журналів")
        self.loading_dialog.show()
        QApplication.processEvents()
        if file_extension == 'xlsx':
            self.selenium_functions.add_data(document_path=file_path,homework=homework_check, engine="openpyxl", lesson=lesson_number)
        elif file_extension == 'xls':
            self.selenium_functions.add_data(document_path=file_path,homework=homework_check, engine="xlrd",lesson=lesson_number)
        elif file_extension == 'docx':
            self.selenium_functions.add_data(document_path=file_path,homework=homework_check, column_number=column, lesson=lesson_number, engine='docx')
        
        self.loading_dialog.close()
        self.show()

    def toggle_theme(self, checked):
        main_theme(self)
        if checked:
            apply_dark_theme(self)
            self.info_label.setStyleSheet("""
                                                    color:#C0B6FC;
                                                    font-size:18px;
                                                    font-weight:bold;""")
        else:
            apply_light_theme(self)
            self.info_label.setStyleSheet("""
                                                    color:#6850FA;
                                                    font-size:18px;
                                                    font-weight:bold;""")

    def update_homework_label(self):
        if self.check_homework.isChecked():
            self.homework_status_label.setText("Так")
        else:
            self.homework_status_label.setText("Ні")

    def closeEvent(self, event):
        self.hide()
        event.accept()

    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: red;
        """)
        self.error_label.show()

    def clear_error(self,widget):
        self.error_label.clear()
        widget.setStyleSheet('')


