# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/designer/errorwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ErrorWindow(object):
    def setupUi(self, ErrorWindow):
        ErrorWindow.setObjectName("ErrorWindow")
        ErrorWindow.resize(320, 240)
        ErrorWindow.setStyleSheet("QWidget#ErrorWindow { background-color: rgb(255, 255, 255); }")
        self.verticalLayout = QtWidgets.QVBoxLayout(ErrorWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.error_label = QtWidgets.QLabel(ErrorWindow)
        self.error_label.setText("")
        self.error_label.setObjectName("error_label")
        self.verticalLayout.addWidget(self.error_label)
        self.quit_btn = QtWidgets.QPushButton(ErrorWindow)
        self.quit_btn.setObjectName("quit_btn")
        self.verticalLayout.addWidget(self.quit_btn)

        self.retranslateUi(ErrorWindow)
        QtCore.QMetaObject.connectSlotsByName(ErrorWindow)

    def retranslateUi(self, ErrorWindow):
        _translate = QtCore.QCoreApplication.translate
        ErrorWindow.setWindowTitle(_translate("ErrorWindow", "Form"))
        self.quit_btn.setText(_translate("ErrorWindow", "OK"))

