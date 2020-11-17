"""Slightly more involved example showing a possible annotation tool
using 2 overlapping QGraphicsView widgets
"""

import os
import sys

import PySide2.QtCore as qtc
import PySide2.QtWidgets as qtw
import PySide2.QtGui as qtg

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

class ScribbleWidget(qtw.QWidget):
    def __init__(self, parent=None):
        super(ScribbleWidget, self).__init__(parent)

        self.setAttribute(qtc.Qt.WA_StaticContents)
        self.modified = False
        self.scribbling = False
        self.pen_width = 2
        self.pen_color = qtc.Qt.blue
        self.image = qtg.QImage()
        self.text_image = qtg.QImage()
        self.last_point = qtc.QPoint()
        self.current_text = ""
        self.previous_text = ""

    def openImage(self, fileName):
        loaded_image = qtg.QImage()
        if not loaded_image.load(fileName):
            return False

        new_size = loaded_image.size().expandedTo(self.size())
        self.resizeImage(loaded_image, new_size)
        self.image = loaded_image
        self.modified = False
        self.update()
        return True

    def saveImage(self, fileName, file_format):
        visibleImage = self.image
        self.resizeImage(visibleImage, self.size())

        if visibleImage.save(fileName, file_format):
            self.modified = False
            return True
        else:
            return False

    def setPenColor(self, newColor):
        self.pen_color = newColor

    def setPenWidth(self, newWidth):
        self.pen_width = newWidth

    def clearImage(self):
        self.image.fill(qtg.qRgb(255, 255, 255))
        self.modified = True
        self.update()

    def draw_text(self):

        painter = qtg.QPainter(self.text_image)
        painter.setPen(qtg.QColor(0, 0, 0))
        # Don't use setFont since it makes the perfomance super slow,
        # see https://bugreports.qt.io/browse/QTBUG-54180
        # painter.setFont(qtg.QFont('Decorative', 10))

        self.text_image.fill(qtg.qRgb(255, 255, 255))
        painter.drawText(self.last_point, self.current_text)

        self.modified = True
        self.update()

    def mousePressEvent(self, event):
        if event.button() == qtc.Qt.LeftButton:
            self.last_point = event.pos()
            self.scribbling = True

    def mouseMoveEvent(self, event):
        if (event.buttons() & qtc.Qt.LeftButton) and self.scribbling:
            self.drawLineTo(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == qtc.Qt.LeftButton and self.scribbling:
            self.drawLineTo(event.pos())
            self.scribbling = False

    def paintEvent(self, event):
        painter = qtg.QPainter(self)
        painter.drawImage(qtc.QPoint(0, 0), self.image)

        if self.current_text != self.previous_text:
            painter.drawText(self.last_point, self.current_text)
        self.previous_text = self.current_text

        # painter.drawImage(qtc.QPoint(0, 0), self.text_image)

    def resizeEvent(self, event):
        if self.width() > self.image.width() or self.height() > self.image.height():
            newWidth = max(self.width() + 128, self.image.width())
            newHeight = max(self.height() + 128, self.image.height())
            self.resizeImage(self.image, qtc.QSize(newWidth, newHeight))
            self.resizeImage(self.text_image, qtc.QSize(newWidth, newHeight))
            self.update()

        super(ScribbleWidget, self).resizeEvent(event)

    def drawLineTo(self, endPoint):
        painter = qtg.QPainter(self.image)
        painter.setPen(qtg.QPen(self.pen_color, self.pen_width,
                qtc.Qt.SolidLine, qtc.Qt.RoundCap, qtc.Qt.RoundJoin))
        painter.drawLine(self.last_point, endPoint)
        self.modified = True

        rad = self.pen_width / 2 + 2
        self.update(qtc.QRect(self.last_point, endPoint).normalized().adjusted(-rad, -rad, +rad, +rad))
        self.last_point = qtc.QPoint(endPoint)

    def resizeImage(self, image, new_size):
        if image.size() == new_size:
            return

        newImage = qtg.QImage(new_size, qtg.QImage.Format_RGB32)
        newImage.fill(qtg.qRgb(255, 255, 255))
        painter = qtg.QPainter(newImage)
        painter.drawImage(qtc.QPoint(0, 0), image)
        self.image = newImage

    def isModified(self):
        return self.modified

    def penColor(self):
        return self.pen_color

    def penWidth(self):
        return self.pen_width


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.window = qtw.QWidget()

        self.scribble_scene = qtw.QGraphicsScene(self)
        self.text_scene = qtw.QGraphicsScene(self)
        self.scribble_view = qtw.QGraphicsView(self.scribble_scene, parent=self.window)
        self.text_view = qtw.QGraphicsView(self.text_scene, parent=self.window)
        self.text_view.setStyleSheet("background: transparent")

        # self.scribble_widget = ScribbleWidget()

        self.setWindowTitle("Annotate")
        self.resize(500, 500)

        self.test_views()

        self.main_layout = qtw.QVBoxLayout()

        # self.main_layout.addWidget(self.scribble_widget)

        # self.spacer = qtw.QSpacerItem(20, 40, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)
        # self.main_layout.addSpacerItem(self.spacer)

        self.scribble_widget = qtw.QWidget()

        # self.main_layout.addWidget(self.scribble_view)
        # self.main_layout.addWidget(self.text_view)

        self.window.setLayout(self.main_layout)
        self.setCentralWidget(self.window)


    def test_views(self):
        green_brush = qtg.QBrush(qtc.Qt.green)
        blue_brush = qtg.QBrush(qtc.Qt.blue)

        pen = qtg.QPen(qtc.Qt.black)
        pen.setWidth(5)

        ellipse = self.scribble_scene.addEllipse(10, 10, 200, 200, pen, green_brush)
        rect = self.scribble_scene.addRect(-100, -100, 200, 200, pen, blue_brush)

        text = self.text_scene.addText("Some text")

        self.scribble_view.setGeometry(0, 0, self.width(), self.height())
        self.text_view.setGeometry(self.scribble_view.x(), self.scribble_view.y(), self.scribble_view.width(), self.scribble_view.height())

        # self.scribble_view.show()
        # self.text_view.show()

    # --------------------------------------------------------------------------
    def keyPressEvent(self, event):
        if event.key() == qtc.Qt.Key_Return or event.key() == qtc.Qt.Key_Enter:
            print 'Pressed Enter!'
        event.accept()

    def resizeEvent(self, event):
        self.scribble_view.setGeometry(0, 0, self.width(), self.height())
        self.text_view.setGeometry(self.scribble_view.x(), self.scribble_view.y(), self.scribble_view.width(), self.scribble_view.height())

        super(MainWindow, self).resizeEvent(event)


def main():
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()