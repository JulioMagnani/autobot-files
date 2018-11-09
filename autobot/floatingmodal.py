from PyQt5.QtWidgets import (QWidget, QListWidget, QListView,
                             QAbstractItemView, QHBoxLayout, QLabel)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QRect
from autobot.ui.roundedwindow import RoundedWindow, ItemDelegate


class FloatingModal(RoundedWindow):

    def __init__(self, parent):
        super(FloatingModal, self).__init__(parent)

        # create list widget for modal
        self.list = QListWidget(self)
        self.list.setGeometry(QRect(20, 70, 320, 380))
        self.list.setStyleSheet(
            "QListView::item{"
            "color: black;"
            "border: 0px;"
            "padding: 2px 20px }"
            "QListView::item:active{"
            "border: none;"
            "background-color: white;}")
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list.setViewMode(QListView.ListMode)

        # horizontal layout for label and add icon
        self.layout = QWidget(self)
        self.layout.setGeometry(QRect(20, 30, 209, 33))
        self.layout.setObjectName("horizontalLayout")
        self.label = QHBoxLayout(self.layout)
        self.label.setContentsMargins(0, 0, 0, 0)
        self.label.setObjectName("modalLabel")
        self.modal_id = QLabel(self.layout)
        font = QFont(":/icons/src/fonts/Montserrat-Bold.ttf")
        font.setPointSize(18)
        self.modal_id.setFont(font)
        self.label.addWidget(self.modal_id)
        self.icon = QLabel(self.layout)
        self.icon.setText("")
        self.label.addWidget(self.icon)

        # set icons in list widget items to the right
        delegate = ItemDelegate()
        self.list.setItemDelegate(delegate)
