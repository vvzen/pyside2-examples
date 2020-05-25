from PySide2 import QtWidgets as qtw
from PySide2 import QtGui as qtg


class Panel(qtw.QWidget):
    def __init__(self):
        super(Panel, self).__init__()

        table = qtw.QTabWidget()

        layout_1 = qtw.QHBoxLayout()
        layout_2 = qtw.QHBoxLayout()
        layout_3 = qtw.QHBoxLayout()

        for i in range(6):
            layout_1.addWidget(qtw.QPushButton("button {}".format(i)))

        for i in range(6):
            layout_2.addWidget(qtw.QCheckBox())

        for i in range(6):
            le = qtw.QLineEdit()
            le.setPlaceholderText("insert some text")
            layout_3.addWidget(le)

        tab_1 = qtw.QWidget()
        tab_1.setLayout(layout_1)

        tab_2 = qtw.QWidget()
        tab_2.setLayout(layout_2)

        tab_3 = qtw.QWidget()
        tab_3.setLayout(layout_3)

        table.addTab(tab_1, "push")
        table.addTab(tab_2, "checkbox")
        table.addTab(tab_3, "lineedit")

        master_layout = qtw.QVBoxLayout()
        master_layout.addWidget(table)
        self.setLayout(master_layout)


app = qtw.QApplication()

panel = Panel()
panel.show()
app.exec_()
