"""More complex example showing a possible annotation tool
"""

import sys

import PySide2.QtCore as qtc
import PySide2.QtWidgets as qtw
import PySide2.QtGui as qtg


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

        self.saveAsActs = []

        self.scribble_widget = ScribbleWidget()
        self.setCentralWidget(self.scribble_widget)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Scribble")
        self.resize(500, 500)

    def keyPressEvent(self, event):
        self.scribble_widget.current_text += event.text()
        print 'self.current_text: %s' % self.scribble_widget.current_text
        # self.scribble_widget.draw_text()

        if event.key() == qtc.Qt.Key_Return or event.key() == qtc.Qt.Key_Enter:
            print 'Pressed Enter!'
            self.current_text = ""
        event.accept()

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def open(self):
        if self.maybeSave():
            fileName,_ = qtw.QFileDialog.getOpenFileName(self, "Open File", qtc.QDir.currentPath())
            if fileName:
                self.scribble_widget.openImage(fileName)

    def save(self):
        action = self.sender()
        file_format = action.data()
        self.saveFile(file_format)

    def penColor(self):
        newColor = qtw.QColorDialog.getColor(self.scribble_widget.penColor())
        if newColor.isValid():
            self.scribble_widget.setPenColor(newColor)

    def penWidth(self):
        newWidth, ok = qtw.QInputDialog.getInt(self, "Scribble",
                "Select pen width:", self.scribble_widget.penWidth(), 1, 50, 1)
        if ok:
            self.scribble_widget.setPenWidth(newWidth)

    def about(self):
        qtw.QMessageBox.about(self, "About Scribble",
                "<p>The <b>Scribble</b> example shows how to use "
                "QMainWindow as the base widget for an application, and how "
                "to reimplement some of QWidget's event handlers to receive "
                "the events generated for the application's widgets:</p>"
                "<p> We reimplement the mouse event handlers to facilitate "
                "drawing, the paint event handler to update the application "
                "and the resize event handler to optimize the application's "
                "appearance. In addition we reimplement the close event "
                "handler to intercept the close events before terminating "
                "the application.</p>"
                "<p> The example also demonstrates how to use QPainter to "
                "draw an image in real time, as well as to repaint "
                "widgets.</p>")

    def createActions(self):
        self.openAct = qtw.QAction("&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)

        for format in qtg.QImageWriter.supportedImageFormats():
            text = str(format.toUpper() + "...")

            action = qtw.QAction(text, self, triggered=self.save)
            action.setData(format)
            self.saveAsActs.append(action)

        self.exitAct = qtw.QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.penColorAct = qtw.QAction("&Pen Color...", self,
                triggered=self.penColor)

        self.penWidthAct = qtw.QAction("Pen &Width...", self,
                triggered=self.penWidth)

        self.clearScreenAct = qtw.QAction("&Clear Screen", self,
                shortcut="Ctrl+L", triggered=self.scribble_widget.clearImage)

        self.aboutAct = qtw.QAction("&About", self, triggered=self.about)

        self.aboutQtAct = qtw.QAction("About &Qt", self,
                triggered=qtg.qApp.aboutQt)

    def createMenus(self):
        self.saveAsMenu = qtw.QMenu("&Save As", self)
        for action in self.saveAsActs:
            self.saveAsMenu.addAction(action)

        fileMenu = qtw.QMenu("&File", self)
        fileMenu.addAction(self.openAct)
        fileMenu.addMenu(self.saveAsMenu)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        optionMenu = qtw.QMenu("&Options", self)
        optionMenu.addAction(self.penColorAct)
        optionMenu.addAction(self.penWidthAct)
        optionMenu.addSeparator()
        optionMenu.addAction(self.clearScreenAct)

        helpMenu = qtw.QMenu("&Help", self)
        helpMenu.addAction(self.aboutAct)
        helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(fileMenu)
        self.menuBar().addMenu(optionMenu)
        self.menuBar().addMenu(helpMenu)

    def maybeSave(self):
        if self.scribble_widget.isModified():
            ret = qtw.QMessageBox.warning(self, "Scribble",
                        "The image has been modified.\n"
                        "Do you want to save your changes?",
                        qtw.QMessageBox.Save | qtw.QMessageBox.Discard |
                        qtw.QMessageBox.Cancel)
            if ret == qtw.QMessageBox.Save:
                return self.saveFile('png')
            elif ret == qtw.QMessageBox.Cancel:
                return False

        return True

    def saveFile(self, file_format):
        initialPath = qtc.QDir.currentPath() + '/untitled.' + file_format

        file_name,_ = qtw.QFileDialog.getSaveFileName(self, "Save As",
                initialPath,
                "%s Files (*.%s);;All Files (*)" % (str(file_format).upper(), file_format))

        if file_name:
            return self.scribble_widget.save_image(file_name, file_format)

        return False

def main():
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()