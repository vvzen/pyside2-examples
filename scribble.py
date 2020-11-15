#!/usr/bin/env python
import PySide2.QtCore as qtc
import PySide2.QtWidgets as qtw
import PySide2.QtGui as qtg


class ScribbleArea(qtw.QWidget):
    def __init__(self, parent=None):
        super(ScribbleArea, self).__init__(parent)

        self.setAttribute(qtc.Qt.WA_StaticContents)
        self.modified = False
        self.scribbling = False
        self.myPenWidth = 2
        self.myPenColor = qtc.Qt.blue
        self.image = qtg.QImage()
        self.lastPoint = qtc.QPoint()

    def openImage(self, fileName):
        loadedImage = qtg.QImage()
        if not loadedImage.load(fileName):
            return False

        newSize = loadedImage.size().expandedTo(self.size())
        self.resizeImage(loadedImage, newSize)
        self.image = loadedImage
        self.modified = False
        self.update()
        return True

    def saveImage(self, fileName, fileFormat):
        visibleImage = self.image
        self.resizeImage(visibleImage, self.size())

        if visibleImage.save(fileName, fileFormat):
            self.modified = False
            return True
        else:
            return False

    def setPenColor(self, newColor):
        self.myPenColor = newColor

    def setPenWidth(self, newWidth):
        self.myPenWidth = newWidth

    def clearImage(self):
        self.image.fill(qtg.qRgb(255, 255, 255))
        self.modified = True
        self.update()

    def keyPressEvent(self, event):
        print 'here!'
        if event.key() == qtc.Qt.Key_Enter:
            painter = qtg.QPainter(self.image)
            painter.setPen(qtg.QColor(168, 34, 3))
            painter.setFont(qtg.QFont('Decorative', 10))
            painter.drawText(event.rect(), qtc.Qt.AlignCenter, self.text)
        event.accept()


    def mousePressEvent(self, event):
        if event.button() == qtc.Qt.LeftButton:
            self.lastPoint = event.pos()
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

    def resizeEvent(self, event):
        if self.width() > self.image.width() or self.height() > self.image.height():
            newWidth = max(self.width() + 128, self.image.width())
            newHeight = max(self.height() + 128, self.image.height())
            self.resizeImage(self.image, qtc.QSize(newWidth, newHeight))
            self.update()

        super(ScribbleArea, self).resizeEvent(event)

    def drawLineTo(self, endPoint):
        painter = qtg.QPainter(self.image)
        painter.setPen(qtg.QPen(self.myPenColor, self.myPenWidth,
                qtc.Qt.SolidLine, qtc.Qt.RoundCap, qtc.Qt.RoundJoin))
        painter.drawLine(self.lastPoint, endPoint)
        self.modified = True

        rad = self.myPenWidth / 2 + 2
        self.update(qtc.QRect(self.lastPoint, endPoint).normalized().adjusted(-rad, -rad, +rad, +rad))
        self.lastPoint = qtc.QPoint(endPoint)

    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            return

        newImage = qtg.QImage(newSize, qtg.QImage.Format_RGB32)
        newImage.fill(qtg.qRgb(255, 255, 255))
        painter = qtg.QPainter(newImage)
        painter.drawImage(qtc.QPoint(0, 0), image)
        self.image = newImage

    def isModified(self):
        return self.modified

    def penColor(self):
        return self.myPenColor

    def penWidth(self):
        return self.myPenWidth


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.saveAsActs = []

        self.scribbleArea = ScribbleArea()
        self.setCentralWidget(self.scribbleArea)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Scribble")
        self.resize(500, 500)

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def open(self):
        if self.maybeSave():
            fileName,_ = qtw.QFileDialog.getOpenFileName(self, "Open File",
                    qtc.QDir.currentPath())
            if fileName:
                self.scribbleArea.openImage(fileName)

    def save(self):
        action = self.sender()
        fileFormat = action.data()
        self.saveFile(fileFormat)

    def penColor(self):
        newColor = qtw.QColorDialog.getColor(self.scribbleArea.penColor())
        if newColor.isValid():
            self.scribbleArea.setPenColor(newColor)

    def penWidth(self):
        newWidth, ok = qtw.QInputDialog.getInt(self, "Scribble",
                "Select pen width:", self.scribbleArea.penWidth(), 1, 50, 1)
        if ok:
            self.scribbleArea.setPenWidth(newWidth)

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
                shortcut="Ctrl+L", triggered=self.scribbleArea.clearImage)

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
        if self.scribbleArea.isModified():
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

    def saveFile(self, fileFormat):
        initialPath = qtc.QDir.currentPath() + '/untitled.' + fileFormat

        fileName,_ = qtw.QFileDialog.getSaveFileName(self, "Save As",
                initialPath,
                "%s Files (*.%s);;All Files (*)" % (str(fileFormat).upper(), fileFormat))
        if fileName:
            return self.scribbleArea.saveImage(fileName, fileFormat)

        return False


if __name__ == '__main__':

    import sys

    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())