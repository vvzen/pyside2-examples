from PySide2 import QtWidgets as qtw
from PySide2 import QtGui as qtg
import qdarkstyle

class Panel(qtw.QWidget):
    def __init__(self):
        super(Panel, self).__init__()

        button = qtw.QPushButton('Close')
        # Connect the clicked signal to the close function
        button.clicked.connect(self.close)

        self.line = qtw.QLineEdit()
        self.line_2 = qtw.QLineEdit()
        
        # Connect the textChange signal to a custom function
        self.line.textChanged.connect(self.update_char_count)

        # A QBUttonGroup is not a UI element, but it's useful to apply general rules
        # to a set of buttons. In this case, a set of checkboxes
        self.checkbox_group = qtw.QButtonGroup()
        
        # Create 5 checkboxes
        for i in range(5):
            c = qtw.QCheckBox('C{}'.format(i))
            c.clicked.connect(self.who_clicked) # connect to a custom function
            self.checkbox_group.addButton(c)

        # Only one button in the group can be clicked at one time
        self.checkbox_group.setExclusive(True)

        self.main_layout = qtw.QHBoxLayout()
        
        # Add the checkboxes to the layout
        for c in self.checkbox_group.buttons():
            self.main_layout.addWidget(c)
        
        # Add widgets, the second argument is for their relative sizes
        self.main_layout.addWidget(self.line, 4)
        self.main_layout.addWidget(self.line_2, 1)
        
        self.main_layout.addWidget(button)
        self.setLayout(self.main_layout)

    def update_char_count(self):
        char_count = str(len(self.line.text()))
        self.line_2.setText(char_count)

    def who_clicked(self):
        sender = self.sender()
        print 'checkbox {}, {} sent a signal'.format(sender, sender.text())
                

app = qtw.QApplication()
# setup stylesheet
# app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
panel = Panel()
panel.show()
app.exec_()