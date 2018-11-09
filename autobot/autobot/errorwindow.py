#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QDialog, QLabel, QPushButton, QApplication,
                             QVBoxLayout, QDesktopWidget)
from PyQt5.QtCore import Qt, QPoint, QCoreApplication


class ErrorWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.center()

        self.warning_ = QLabel("This is a warning")
        self.warning_.setMargin(30)
        quit_ = QPushButton("Quit")

        layout = QVBoxLayout()
        layout.addWidget(self.warning_)
        layout.addWidget(quit_)

        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)

        quit_.clicked.connect(QCoreApplication.instance().quit)

    def set_warning(self, text):
        self.warning_.setText(text)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, e):
        self.oldPos = e.globalPos()

    def mouseMoveEvent(self, e):
        delta = QPoint(e.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = e.globalPos()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ex = ErrorWindow()
    ex.show()
    sys.exit(app.exec_())
