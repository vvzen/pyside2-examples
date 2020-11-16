import math
import time
import sys

from PySide2 import QtWidgets as qtw
from PySide2 import QtCore as qtc
from PySide2 import QtGui as qtg


class MyRunnableSignals(qtc.QObject):
    # We can choose any name that we want since we will manually emit them
    # from our own QRunnable
    started = qtc.Signal()
    completed = qtc.Signal((int, bool))
    progress = qtc.Signal(int)
    failed = qtc.Signal(str)


class MyRunnable(qtc.QRunnable):
    """A Runnable is a simpler version of a QThread, with a similar interface.
    A QRunnable doesn't have an
    It doesn't offer signals by default, that's why we're creating our own.
    For easy stuff, a runnable it's more than enough!
    """
    def __init__(self, my_number):
        super(MyRunnable, self).__init__()

        self.my_number = my_number
        self.signals = MyRunnableSignals()

    def run(self):
        """This will be automatically called when it's time!
        """

        self.signals.started.emit()

        try:
            # Let's check if a num is a square of 2
            decimals, integer = math.modf(math.log(self.my_number, 2))

            # A heavy and long calculation could happen here
            for i in range(100):
                self.signals.progress.emit(i)
                time.sleep(0.05)

            if decimals == 0.0:
                # We can send different variable types from our signals
                # Check the signal definition in MyRunnableSignals
                self.signals.completed.emit(self.my_number, True)
            else:
                self.signals.completed.emit(self.my_number, False)

        except Exception as err:
            print 'error: %s' % err
            self.signals.failed.emit('QRunnable error: %s' % err)


# A simple Panel class with some basic widgets that how to call a runnable
class Panel(qtw.QWidget):
    def __init__(self):
        super(Panel, self).__init__()

        self.progress_dialog = None

        self.label = qtw.QLabel('Number: -1')
        self.current_number = -1

        self.button = qtw.QPushButton('Start')
        self.button.setToolTip('shortcut: s')
        self.button.setShortcut('s')
        self.button.clicked.connect(self.start_long_calculation)

        self.calculation_result = qtw.QLabel('')

        self.number_slider = qtw.QSlider(qtc.Qt.Orientation.Horizontal)
        self.number_slider.sliderMoved.connect(self.on_slider_changed)

        self.vlayout = qtw.QVBoxLayout()
        self.vlayout.addWidget(self.label)
        self.vlayout.addWidget(self.number_slider)
        self.vlayout.addWidget(self.button)
        self.vlayout.addSpacing(25)
        self.vlayout.addWidget(self.calculation_result)

        self.setLayout(self.vlayout)

    def on_slider_changed(self, value):
        self.current_number = value
        self.label.setText('Number: %s' % value)

    def start_long_calculation(self):
        # We create an instance of our QRunnable
        my_runnable = MyRunnable(self.current_number)
        my_runnable.signals.started.connect(self.on_calculation_start)
        my_runnable.signals.progress.connect(self.on_calculation_progress)
        my_runnable.signals.completed.connect(self.on_calculation_success)
        my_runnable.signals.failed.connect(self.on_calculation_fail)

        # We grab the preexisting threadpool and use it to "queue"
        # the execution of our runnable
        # For more info on QThreadPool, see https://doc.qt.io/qt-5/qthreadpool.html
        qtc.QThreadPool.globalInstance().start(my_runnable)

        self.progress_dialog = qtw.QProgressDialog("Crunching numbers..",
                                                   "Abort", 0, 100, self)

        self.progress_dialog.setWindowModality(qtc.Qt.WindowModal)
        self.progress_dialog.setCancelButton(None)
        self.progress_dialog.show()

    def on_calculation_start(self):
        sys.stdout.write('Calculation started.. crunching numbers.. '
                         'it will take a while...\n')
        sys.stdout.flush()

    def on_calculation_progress(self, value):
        self.progress_dialog.setValue(value)

    def on_calculation_success(self, number, result):
        message = 'Calculation succeded! Is %s a square of 2? %s\n' % (number,
                                                                       result)
        sys.stdout.write(message)
        sys.stdout.flush()
        self.progress_dialog.close()
        self.calculation_result.setText(message)

    def on_calculation_fail(self, message):
        sys.stderr.write('Calculation failed. %s\n' % message)
        sys.stderr.flush()
        self.progress_dialog.close()
        self.calculation_result.setText(message)


def main():
    app = qtw.QApplication()

    panel = Panel()
    panel.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
