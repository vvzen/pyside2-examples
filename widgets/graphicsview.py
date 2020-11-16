import sys

import PySide2.QtCore as qtc
import PySide2.QtWidgets as qtw
import PySide2.QtGui as qtg

class MainWindow(qtw.QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("QGraphic View Example")
        self.setGeometry(300, 300, 640, 520)

        self.populate_view()

        master_layout = qtw.QVBoxLayout()
        master_layout.addWidget(self.view)
        self.setLayout(master_layout)


    def populate_view(self):
        self.scene = qtw.QGraphicsScene(self)

        green_brush = qtg.QBrush(qtc.Qt.green)
        blue_brush = qtg.QBrush(qtc.Qt.blue)

        pen = qtg.QPen(qtc.Qt.black)
        pen.setWidth(5)

        self.scene.addEllipse(10, 10, 200, 200, pen, green_brush)
        self.scene.addRect(-100, -100, 200, 200, pen, blue_brush)

        self.view = qtw.QGraphicsView(self.scene)
        self.view.setGeometry(0, 0, 640, 440)


def main():
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
