import sys

from PySide2 import QtWidgets as qtw
from PySide2 import QtGui as qtg

# A simple Panel class with some basic widgets


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

        # A QCompleter helps users by giving autocompletion
        self.user_line = qtw.QLineEdit()
        self.users = ['harry', 'hermione', 'ron', 'hagrid']
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


def main():
    app = qtw.QApplication(sys.argv)
    panel = Panel()
    panel.show()
    app.exec_()

if __name__ == '__main__':
    main()
