from PyQt5 import QtWidgets
import sys
from loguru import logger
import design
import hfsstokicad


class Converter(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.BtnOpen.clicked.connect(self.open_file)

    def open_file(self):
        openfilename = QtWidgets.QFileDialog.getOpenFileName(self, 'open_file', "")[0]
        if openfilename:
            res, status = hfsstokicad.main(openfilename)
            if res:
                info_message(status)
            else:
                error_message(status)


def error_message(text):
    error = QtWidgets.QMessageBox()
    error.setIcon(QtWidgets.QMessageBox.Critical)
    error.setText(text)
    error.setWindowTitle('Error')
    error.setStandardButtons(QtWidgets.QMessageBox.Ok)
    error.exec_()


def info_message(text):
    error = QtWidgets.QMessageBox()
    error.setIcon(QtWidgets.QMessageBox.Information)
    error.setText(text)
    error.setWindowTitle('Success')
    error.setStandardButtons(QtWidgets.QMessageBox.Ok)
    error.exec_()


def initiate_exception_logging():
    # generating our hook
    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook

    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        logger.exception(f"{exctype}, {value}, {traceback}")
        # Call the normal Exception hook after
        # noinspection PyProtectedMember
        sys._excepthook(exctype, value, traceback)
        # sys.exit(1)

    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook


@logger.catch
def main():
    initiate_exception_logging()
    app = QtWidgets.QApplication(sys.argv)
    window = Converter()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
