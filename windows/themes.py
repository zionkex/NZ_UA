from PyQt6.QtGui import QPalette, QColor

def main_theme(window):
    window.setStyleSheet("""
        QWidget{
            font-family: 'Verdana';
            font-size: 16px;}
        QLineEdit, QComboBox {
            border-radius: 5px;
            padding: 10px;
        }
        QPushButton {
            border-radius: 5px;
            padding: 10px;
        }
        
    """)        

def apply_light_theme(window):
    window.setStyleSheet(window.styleSheet() + """
        QWidget {
            background-color: #fff;
            color: #000;
        }  
        QPushButton {
            color: #fff;
            background-color: #6850FA;
            }  
        QPushButton:hover {
            background-color: #5842DC;
        }
        QPushButton:pressed {
            background-color: #5741DE;
        }
        QLineEdit,QComboBox {
            border: 1px solid #6850FA;
        }              
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px; 
            border-left: 1px solid #6850FA; 
        }
        QComboBox::down-arrow {
            image: url(main/images/light_down.png); 
            width: 10px;
            height: 10px;
        }
        QComboBox QAbstractItemView {
            font-size:12px;
            border: 1px solid #6850FA;
            background-color: #fff;
            color: #000;
        }
        
        QComboBox::item:selected {
        background-color: lightgray;
    }
        

    """)

def apply_dark_theme(window):
    window.setStyleSheet(window.styleSheet() + """
        QWidget {
            background-color: #1E1E1E;
            color: #fff;
        }
        QLineEdit {
            background-color: #fff;
            color : #000;
            border: 1px solid #000;
            }
        QPushButton {
            color: #fff;
            background-color: #6850FA;
            }  
        QPushButton:hover {
            background-color: #5842DC;
        }
        QPushButton:pressed {
            background-color: #5741DE;
        }
        QComboBox {
            border: 1px solid #6850FA;
        }  
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px; 
            border-left: 1px solid #6850FA;
        }
        QComboBox::down-arrow {
            image: url(main/images/dark_down.png);
            width: 10px;
            height: 10px;
        }
        QComboBox QAbstractItemView {
            font-size:12px;
            border: 1px solid #6850FA;
            background-color: #000;
            color: #fff;
        }
    QComboBox::item:selected {
        background-color: gray;
    }    
        
    """)
    # set_placeholder_text_color(window.input_login, QColor("#000"))
    # set_placeholder_text_color(window.input_password, QColor("#000"))

def set_placeholder_text_color(widget, color):
    palette = widget.palette()
    palette.setColor(QPalette.ColorRole.PlaceholderText, color)
    widget.setPalette(palette)
