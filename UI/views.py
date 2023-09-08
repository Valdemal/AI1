from itertools import product

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSizeF, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtWidgets import QWidget

from Controller import Controller


class Table(QWidget):
    def __init__(self, size: int, controller: Controller):
        super().__init__()
        self._controller = controller
        self.setMaximumSize(size, size)
        self.setMinimumSize(size, size)
        self.resize(size, size)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.__paint_border(painter)
        self.__paint_squares(painter)
        self.__paint_queens(painter)

        painter.end()

    def __paint_border(self, painter: QPainter):
        painter.setPen(QPen(Qt.black, 3))
        painter.drawRect(self.rect())

    def __paint_queens(self, painter: QPainter):
        painter.setPen(QPen(Qt.yellow, 3))

        n = len(self._controller.queens)
        a = self.width() / n

        for i in range(n):
            x1 = int(self.rect().x() + self._controller.queens[i] * a)
            y1 = int(self.rect().y() + i * a)
            painter.drawLine(
                x1, y1, x1 + int(a), y1 + int(a)
            )

    def __paint_squares(self, painter: QPainter):
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(QBrush(Qt.darkGray))

        n = len(self._controller.queens)
        a = self.width() / n
        size = QSizeF(a, a)

        for i, j in product(range(n), range(n)):
            if (i + j) % 2 == 0:
                top_left = QPointF(self.rect().x() + j * a, self.rect().y() + i * a)
                draw_rect = QRectF(top_left, size)
                painter.drawRect(draw_rect)
