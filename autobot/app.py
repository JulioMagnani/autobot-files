# -*- coding: utf-8 -*-

import sys
from threading import Thread
from PyQt5.QtWidgets import QApplication
from autobot.mainwindow import MainWindow
from autobot.testrunner import TestRunner
from autobot.progwindow_ui import ProgressWindow
from autobot.log import Output


class App():

    def run(self):
        app = QApplication(sys.argv)
        self.init_mainwindow()
        sys.exit(app.exec_())

    def init_mainwindow(self):
        self.main_window = MainWindow()

        # open progress window and initiate test runner
        self.main_window.runner_btn.clicked.connect(self.init_prog_window)
        self.main_window.runner_btn.clicked.connect(self.run_tests)
        self.main_window.show()

    def init_prog_window(self):
        self.prog_window = ProgressWindow()
        self.prog_window.show()

    def run_tests(self):
            """"Test Runner"""

            self.login_info = self.main_window.login_info.get_info()
            test_list = self.main_window.added_tests
            runner = TestRunner(test_list)
            fixture = runner.load_tests(self.login_info)

            # q = Queue(maxsize=0)
            # q.put(fixture)

            t = Thread(target=lambda: runner.run_suite(fixture))
            t.setDaemon(True)
            t.start()

            # self.init_prog_window()
            # self.update_progress()

    def update_progress(self):
        message = Output().read()
        self.prog_window.set_text(message)


if __name__ == '__main__':
    App.run()
