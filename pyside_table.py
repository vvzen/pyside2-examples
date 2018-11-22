from PySide2 import QtWidgets as qtw
from PySide2 import QtGui as qtg
from PySide2 import QtCore as qtc
import qdarkstyle

class MyTableWidget(qtw.QTableWidget):

    def __init__(self):
        super(MyTableWidget, self).__init__()

        data = self.get_data()
        
        self.setRowCount(len(data.keys()))
        self.setColumnCount(4)
        # Set the column names
        self.setHorizontalHeaderItem(0, qtw.QTableWidgetItem('Name'))
        self.setHorizontalHeaderItem(1, qtw.QTableWidgetItem('Gender'))
        self.setHorizontalHeaderItem(2, qtw.QTableWidgetItem('Age'))
        self.setHorizontalHeaderItem(3, qtw.QTableWidgetItem('Married'))
        
        # Make the last column follow the dimensions of the window
        self.horizontalHeader().setStretchLastSection(True)

        # Set it to be read only (doesn't work with the checkbox, see it's related code)
        self.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)

        # Let user select rows
        self.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)

        # Set the row values
        for i, name in enumerate(data):            
            for j, key in enumerate(data[name].keys()):
                
                print '{}, {}, {}, {}'.format(i, j, key, str(data[name][key]))

                if j == 0:
                    cell_widget = qtw.QTableWidgetItem(name)
                    cell_widget.setFlags(cell_widget.flags() ^ qtc.Qt.ItemIsEditable)
                    self.setItem(i, j, cell_widget)
                
                if key == 'gender':
                    cell_widget = qtw.QTableWidgetItem(data[name][key])
                    self.setItem(i, j+1, cell_widget)
                
                elif key == 'age':
                    cell_widget = qtw.QTableWidgetItem(str(data[name][key]))
                    self.setItem(i, j+1, cell_widget)

                elif key == 'married':
                    cell_widget = qtw.QCheckBox()
                    cell_widget.setChecked(data[name][key])
                    cell_widget.setEnabled(False)
                    self.setCellWidget(i, j+1, cell_widget)
    
    def get_data(self):
        return {
            'pippo' : {
                'gender' : 'male',
                'age' : 27,
                'married': False
            },
            'topolino' : {
                'gender' : 'male',
                'age' : 24,
                'married': True
            },
            'minnie' : {
                'gender' : 'female',
                'age' : 24,
                'married': True
            }
        }

app = qtw.QApplication()
# setup stylesheet
# app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
table = MyTableWidget()
table.show()
app.exec_()