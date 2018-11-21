from PySide2 import QtWidgets as qtw
from PySide2 import QtGui as qtg
import qdarkstyle


class Panel(qtw.QWidget):
    def __init__(self):
        # call super
        super(Panel, self).__init__()

        self.label = qtw.QLabel('Username')

        self.button = qtw.QPushButton('Start')
        self.button.setIcon(qtg.QIcon('example_icon.png'))
        self.button.setToolTip('shortcut: u')
        self.button.setShortcut('u')

        self.checkbox = qtw.QCheckBox('agree to GDPR')
        self.checkbox.setChecked(True)

        self.user_line = qtw.QLineEdit()
        self.users = ['valerio', 'edoardo', 'gaia', 'rami']
        self.completer_line = qtw.QCompleter(self.users)
        self.user_line.setCompleter(self.completer_line)
        self.user_line.setPlaceholderText('enter you name here..')

        self.combobox = qtw.QComboBox()
        self.permissions_combobox = ['r', 'w', 'rx', 'rw', 'rwx']
        self.combobox.addItems(self.permissions_combobox)

        self.vlayout = qtw.QVBoxLayout()
        self.vlayout.addWidget(self.label)
        self.vlayout.addWidget(self.user_line)
        self.vlayout.addWidget(self.checkbox)
        self.vlayout.addWidget(self.combobox)
        self.vlayout.addSpacing(25)
        self.vlayout.addWidget(self.button)

        self.setLayout(self.vlayout)


app = qtw.QApplication()
# setup stylesheet
app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

panel = Panel()
panel.show()

app.exec_()