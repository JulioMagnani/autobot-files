# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/designer/progwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProgForm(object):
    def setupUi(self, ProgForm):
        ProgForm.setObjectName("ProgForm")
        ProgForm.setWindowModality(QtCore.Qt.NonModal)
        ProgForm.resize(640, 480)
        ProgForm.setStyleSheet("QWidget#Form{ background-color: rgb(255, 255, 255); }")
        self.verticalLayout = QtWidgets.QVBoxLayout(ProgForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.progLabel = QtWidgets.QLabel(ProgForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progLabel.sizePolicy().hasHeightForWidth())
        self.progLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        self.progLabel.setFont(font)
        self.progLabel.setObjectName("progLabel")
        self.verticalLayout.addWidget(self.progLabel)
        self.progText = QtWidgets.QPlainTextEdit(ProgForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progText.sizePolicy().hasHeightForWidth())
        self.progText.setSizePolicy(sizePolicy)
        self.progText.setObjectName("progText")
        self.verticalLayout.addWidget(self.progText)
        self.bottomLayout = QtWidgets.QHBoxLayout()
        self.bottomLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.bottomLayout.setObjectName("bottomLayout")
        spacerItem = QtWidgets.QSpacerItem(340, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.bottomLayout.addItem(spacerItem)
        self.quitBtn = QtWidgets.QPushButton(ProgForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quitBtn.sizePolicy().hasHeightForWidth())
        self.quitBtn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.quitBtn.setFont(font)
        self.quitBtn.setStyleSheet("QPushButton#quitBtn { background-color: rgb(0, 104, 255);  color: rgb(255, 255, 255); border: None}")
        self.quitBtn.setObjectName("quitBtn")
        self.bottomLayout.addWidget(self.quitBtn)
        self.verticalLayout.addLayout(self.bottomLayout)

        self.retranslateUi(ProgForm)
        QtCore.QMetaObject.connectSlotsByName(ProgForm)

    def retranslateUi(self, ProgForm):
        _translate = QtCore.QCoreApplication.translate
        ProgForm.setWindowTitle(_translate("ProgForm", "Form"))
        self.progLabel.setText(_translate("ProgForm", "Progress"))
        self.quitBtn.setText(_translate("ProgForm", "Quit"))

