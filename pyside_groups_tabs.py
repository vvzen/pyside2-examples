from PySide2 import QtWidgets as qtw
from PySide2 import QtGui as qtg
import qdarkstyle

class Panel(qtw.QWidget):
    def __init__(self):
        super(Panel, self).__init__()

        group_1 = qtw.QGroupBox('checkbox')
        group_1_layout = qtw.QHBoxLayout()
        group_1.setLayout(group_1_layout)

        group_1.setEnabled(False)

        for _ in range(5):
            group_1_layout.addWidget(qtw.QCheckBox())

        group_2 = qtw.QGroupBox('line edit')
        group_2_layout = qtw.QHBoxLayout()
        group_2.setLayout(group_2_layout)

        for _ in range(5):
            group_2_layout.addWidget(qtw.QLineEdit())

        master_layour = qtw.QVBoxLayout()
        master_layour.addWidget(group_1)
        master_layour.addWidget(group_2)
        self.setLayout(master_layour)

app = qtw.QApplication()
# setup stylesheet
app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
panel = Panel()
panel.show()
app.exec_()