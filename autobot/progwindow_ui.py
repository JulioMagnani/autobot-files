from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget
from autobot.ui.progwindow_ui import Ui_ProgForm


class ProgressWindow(QWidget, Ui_ProgForm):

    def __init__(self, parent=None):
        super(ProgressWindow, self).__init__(parent)

        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.center()

        self.quitBtn.clicked.connect(self.close)

    def set_text(self, text):
        self.progText.setPlainText(str(text))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # mouse press listener
    def mousePressEvent(self, e):
        self.oldPos = e.globalPos()

    def mouseMoveEvent(self, e):
        delta = QPoint(e.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = e.globalPos()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = ProgressWindow()
    window.show()
    sys.exit(app.exec_())
