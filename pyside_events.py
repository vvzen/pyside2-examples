from PySide2 import QtWidgets as qtw
from PySide2 import QtGui as qtg
import qdarkstyle

class MyLineEdit(qtw.QLineEdit):
    def __init__(self):
        super(MyLineEdit, self).__init__()

    def enterEvent(self, event):
        self.setText('mouse is in')
    
    def leaveEvent(self, event):
        self.setText('mouse is out')

class Panel(qtw.QWidget):
    def __init__(self):
        super(Panel, self).__init__()

        self.label = qtw.QLabel('Click me')

        # Add a custom linedit with a custom event handler
        self.line_edit = MyLineEdit()

        self.main_layout = qtw.QHBoxLayout()
        
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.line_edit)

        self.setLayout(self.main_layout)

    def mousePressEvent(self, event):
        self.label.setText('{}, {}'.format(event.pos().x(), event.pos().y()))

    def keyPressEvent(self, event):
        print event.text()

app = qtw.QApplication()
# setup stylesheet
app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
panel = Panel()
panel.show()
app.exec_()