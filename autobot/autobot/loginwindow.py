import os
from PyQt5.QtWidgets import (QWidget, QDialog, QDesktopWidget,
                             QLabel, QPushButton, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import Qt, QPoint
from autobot.ui.loginwindow_ui import Ui_LoginForm


class LoginWindow(QWidget, Ui_LoginForm):

    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.center()

        self.__username = None
        self.__password = None
        self.__ssid24 = None
        self.__pass24 = None
        self.__ssid5 = None
        self.__pass5 = None

        if self.is_pwdsaved():
            log_data = self.read_file()
            self.update_fields(log_data)

        self.login_btn.clicked.connect(self.login_auth)

        self.show()

    # ########### WINDOW MOVEMENT ############
    # center window
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

    def mouseReleaseEvent(self, event):

        # close event
        if event.button() == Qt.RightButton:
            self.close()

    # ########### WINDOW MOVEMENT ############

    def is_pwdsaved(self):
        current_dir = os.getcwd()
        return os.path.isfile('{0}/login.txt'.format(current_dir))

    def update_fields(self, log_data):
        self.__username = log_data[0]
        self.__password = log_data[1]
        self.__ssid24 = log_data[2]
        self.__pass24 = log_data[3]
        self.__ssid5 = log_data[4]
        self.__pass5 = log_data[5]

        self.usrText.setText(self.__username)
        self.pwd_text.setText(self.__password)
        self.ssid24Text.setText(self.__ssid24)
        self.pass24Text.setText(self.__pass24)
        self.ssid5Text.setText(self.__ssid5)
        self.pass5Text.setText(self.__pass5)

    def login_auth(self):
        """create login confirm modal"""

        self.usr_tmp = self.usrText.text()
        self.pwd_tmp = self.pwd_text.text()
        self.ssid24_tmp = self.ssid24Text.text()
        self.pass24_tmp = self.pass24Text.text()
        self.ssid5_tmp = self.ssid5Text.text()
        self.pass5_tmp = self.pass5Text.text()

        self.dialog = Form()
        self.dialog.show()

        self.dialog.yes_btn.clicked.connect(self.set_login_info)

        # dialog = QMessageBox(self)
        # dialog.setText('Are you sure?')
        # dialog.setContentsMargins(15, 15, 15, 15)

        # dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # dialog.buttonClicked.connect(self.set_login_info)
        # dialog.show()

    def set_login_info(self):
        """Set login and password"""

        self.__username = self.usr_tmp
        self.__password = self.pwd_tmp
        self.__ssid24 = self.ssid24_tmp
        self.__pass24 = self.pass24_tmp
        self.__ssid5 = self.ssid5_tmp
        self.__pass5 = self.pass5_tmp
        self.write_file()
        self.dialog.close()
        self.close()

    def write_file(self):
        with open("login.txt", "w") as login:
            login.write('{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n'.format(
                self.__username, self.__password, self.__ssid24,
                self.__pass24, self.__ssid5, self.__pass5))

    def read_file(self):
        with open("login.txt", "r") as login:
            output = [line.strip() for line in login.readlines()]

        return output

    def get_info(self):
        login = dict([('username', self.__username),
                      ('password', self.__password),
                      ('ssid_2.4', self.__ssid24),
                      ('pass_2.4', self.__pass24),
                      ('ssid_5', self.__ssid5),
                      ('pass_5', self.__pass5)])
        return login


class Form(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setModal(True)

        self.message = QLabel("Are you sure?")
        self.message.setMargin(30)

        self.yes_btn = QPushButton("Yes")
        self.yes_btn.setObjectName("&Yes")
        self.no_btn = QPushButton("No")
        hbox = QHBoxLayout()
        hbox.addWidget(self.yes_btn)
        hbox.addWidget(self.no_btn)

        vbox = QVBoxLayout()
        vbox.addWidget(self.message)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.no_btn.clicked.connect(self.close)
