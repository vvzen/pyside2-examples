from PySide2 import QtWidgets as qtw
from PySide2 import QtGui as qtg
import qdarkstyle

class Panel(qtw.QWidget):
    def __init__(self):
        super(Panel, self).__init__()

        list_widget = qtw.QListWidget()
        shots = ['004', '001', '003', '002', '005']

        for i, shot in enumerate(shots):
            item = qtw.QListWidgetItem(shot)
            item.setToolTip('shot {}'.format(i))
            item.setIcon(qtg.QIcon('shot.png'))
            
            item.setBackgroundColor(qtg.QColor(152, 106, 232))
            list_widget.addItem(item)

        # we can sort stuff
        list_widget.sortItems()
        list_widget.setAlternatingRowColors(True)
        list_widget.setSelectionMode(qtw.QAbstractItemView.ExtendedSelection)

        master_layour = qtw.QVBoxLayout()
        master_layour.addWidget(list_widget)
        self.setLayout(master_layour)

app = qtw.QApplication()
# setup stylesheet
app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
panel = Panel()
panel.show()
app.exec_()