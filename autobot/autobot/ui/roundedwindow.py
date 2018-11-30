#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QSizeGrip,
                             QApplication, QStyledItemDelegate,
                             QStyleOptionViewItem, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QColor, QPainter


def hex2QColor(c):
    """Convert Hex color to QColor"""
    r=int(c[0:2],16)
    g=int(c[2:4],16)
    b=int(c[4:6],16)
    return QColor(r,g,b)


class ItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.decorationPosition = QStyleOptionViewItem.Right
        super(ItemDelegate, self).paint(painter, option, index)


class RoundedWindow(QWidget):
    def __init__(self, parent=None):
        super(RoundedWindow, self).__init__(parent)

        # make the window frameless
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        shadow_fx = QGraphicsDropShadowEffect()
        shadow_fx.setBlurRadius(8)
        shadow_fx.setXOffset(5)

        self.backgroundColor = hex2QColor("ffffff")
        self.foregroundColor = hex2QColor("707070")
        self.borderRadius = 1
        self.draggable = False
        self.__mousePressPos = None
        self.__mouseMovePos = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setGeometry(QRect(150, 80, 362, 500))
        self.setGraphicsEffect(shadow_fx)

    def paintEvent(self, event):
        # get current window size
        s = self.size()
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setPen(self.foregroundColor)
        qp.setBrush(self.backgroundColor)
        qp.drawRoundedRect(0, 0, s.width(), s.height(),
                           self.borderRadius, self.borderRadius)
        qp.end()

    def mousePressEvent(self, event):
        if self.draggable and event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()                # global
            self.__mouseMovePos = event.globalPos() - self.pos()    # local
        super(RoundedWindow, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() & Qt.LeftButton:
            globalPos = event.globalPos()
            moved = globalPos - self.__mousePressPos
            if moved.manhattanLength() > self.dragging_threshould:
                # move when user drag window more than dragging_threshould
                diff = globalPos - self.__mouseMovePos
                self.move(diff)
                self.__mouseMovePos = globalPos - self.pos()
        super(RoundedWindow, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            if event.button() == Qt.LeftButton:
                moved = event.globalPos() - self.__mousePressPos
                if moved.manhattanLength() > self.dragging_threshould:
                    # do not call click event or so on
                    event.ignore()
                self.__mousePressPos = None
        super(RoundedWindow, self).mouseReleaseEvent(event)

        # close event
        if event.button() == Qt.RightButton:
            self.close()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main = RoundedWindow()
    main.show()
    sys.exit(app.exec_())
