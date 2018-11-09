from PyQt5.QtWidgets import (QMainWindow, QListWidgetItem, QPushButton,
                             QDesktopWidget)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QPoint
from autobot.tests.loader import Test
from autobot.ui.mainwindow_ui import Ui_MainWindow
from autobot.loginwindow import LoginWindow
from autobot.floatingmodal import FloatingModal
from autobot.errorwindow import ErrorWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.center()
        self.setWindowTitle("Autobot v5.0")

        self.__added_tests = []

        # load test data
        self.test_data = None
        try:
            self.test_data = Test()
            self.tests = self.test_data.get_tests_db()
        except Exception as error:
            msg = str(error)
            self.error_window = ErrorWindow()
            self.error_window.set_warning(msg)
            self.error_window.setModal(True)
            self.error_window.show()

        self.init_floating_modals(self)
        self.load_sidebar()  # event handlers for side bar

    # center window
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # mouse press listener
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            element = self.childAt(e.pos())
            if element.objectName() == 'add_all_icon':
                self.add_all_tests()
            elif element.objectName() == 'rm_all_icon':
                self.remove_all_tests()
            elif element.objectName() == 'login_menu':
                self.login_info = LoginWindow()
            elif element.objectName() == 'quit_menu':
                self.close()
        self.oldPos = e.globalPos()

    def mouseMoveEvent(self, e):
        delta = QPoint(e.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = e.globalPos()

    @property
    def added_tests(self):
        return self.__added_tests

    def load_sidebar(self):
        self.ui_icon.clicked.connect(lambda: self.load_selector_items(
                                                      select='User Interface'))
        self.dhcp_icon.clicked.connect(lambda: self.load_selector_items(
                                                      select='DHCP'))
        self.wifi24_icon.clicked.connect(lambda: self.load_selector_items(
                                                      select='Wifi 2.4 GHZ'))
        self.wifi5_icon.clicked.connect(lambda: self.load_selector_items(
                                                      select='Wifi 5.0 GHZ'))
        self.ipv6_icon.clicked.connect(lambda: self.load_selector_items(
                                                      select='IPV6'))

    def show_modal(self):
        self.sel_modal.show()
        self.fix_modal.show()

    def load_selector_items(self, select=None):
        """Fill test selector list items"""

        self.sel_modal.list.clear()  # clear widget list

        try:
            suite = self.test_data.get_suite(select)
            if suite:
                self.sel_modal.modal_id.setText(select)  # set selct list label
                self.sel_modal.layout.adjustSize()

                # create test items to fill test selector
                test_labels = self.test_data.get_test_labels(select)
                for label in test_labels:
                    self.create_list_item(label, modal='selector list')

            self.show_modal()
        except AttributeError as error:
            msg = str(error)
            self.error_window = ErrorWindow()
            self.error_window.set_warning(msg)
            self.error_window.show()

    def add_test(self):
        """Add single tests to the test runner"""

        item = self.sel_modal.list.currentItem().text()
        if item not in self.__added_tests:
            self.create_list_item(item, modal='runner list')
            self.__added_tests.append(item)

    def add_all_tests(self):
        """Add all tests in test selector to the test runner"""

        ls_len = self.sel_modal.list.count()
        sel_lst = [self.sel_modal.list.item(it).text() for it in range(ls_len)]
        for item in sel_lst:
            if item not in self.__added_tests:
                self.create_list_item(item, modal='runner list')
                self.__added_tests.append(item)

    def create_list_item(self, item, modal=None):
        new_item = QListWidgetItem()
        new_item.setText(item)

        icon = QIcon()
        if modal == 'runner list':
            icon.addPixmap(QPixmap(':/icons/src/icons/remove-icon.png'))
            new_item.setIcon(icon)
            self.fix_modal.list.addItem(new_item)
        elif modal == 'selector list':
            icon.addPixmap(QPixmap(':/icons/src/icons/add-icon-.png'))
            new_item.setIcon(icon)
            self.sel_modal.list.addItem(new_item)

    def remove_test(self):
        """remove an item from runner modal and added tests list"""

        fixture_list = self.fix_modal.list
        current_item = fixture_list.currentItem().text()
        self.__added_tests.remove(current_item)
        fixture_list.takeItem(fixture_list.currentRow())

    def remove_all_tests(self):
        """clear all items added"""
        self.__added_tests = []
        self.fix_modal.list.clear()

    def init_floating_modals(self, parent):

        # test selector modal
        self.sel_modal = FloatingModal(parent)
        self.sel_modal.list.setObjectName("test_selector")
        self.sel_modal.icon.setPixmap(
            QPixmap(':/icons/src/icons/add-icon-.png'))
        self.sel_modal.icon.setObjectName("add_all_icon")

        # fixture modal
        self.fix_modal = FloatingModal(parent)
        self.fix_modal.list.setObjectName("test_fixer")
        self.fix_modal.modal_id.setText("Fixture")
        self.fix_modal.icon.setPixmap(
            QPixmap(":/icons/src/icons/remove-icon.png"))
        self.fix_modal.icon.setObjectName("rm_all_icon")

        # add run tests button to fixture modal
        self.runner_btn = QPushButton(self.fix_modal)
        self.runner_btn.setGeometry(240, 455, 100, 35)
        font = QFont()
        font.setPointSize(14)
        self.runner_btn.setFont(font)
        self.runner_btn.setStyleSheet("background-color:rgb(0, 123, 255);"
                                      "border:none;color:rgb(255, 255, 255);")
        self.runner_btn.setFlat(True)
        self.runner_btn.setText('Run Tests')
        self.runner_btn.setObjectName("runner_btn")

        self.fix_modal.move(540, 80)
        self.sel_modal.hide()
        self.fix_modal.hide()

        self.sel_modal.list.itemClicked.connect(self.add_test)
        self.fix_modal.list.itemClicked.connect(self.remove_test)
