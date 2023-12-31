from itertools import product

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSizeF, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen, QBrush, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from pyqtgraph import PlotWidget, mkPen

from Controller import Solver, HistoryStorage


class Table(QWidget):
    def __init__(self, size: int, solver: Solver):
        super().__init__()
        self._solver = solver
        self.setMaximumSize(size, size)
        self.setMinimumSize(size, size)
        self.resize(size, size)

        self.pixmap = QPixmap()
        self.pixmap.load("static/queen.png")

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        n = len(self._solver.queens)
        a = self.width() / n
        size = QSizeF(a, a)

        self.__paint_border(painter)
        self.__paint_squares(painter, n, size)
        self.__paint_queens(painter, size)

        painter.end()

    def __paint_border(self, painter: QPainter):
        painter.setPen(QPen(Qt.black, 3))
        painter.drawRect(self.rect())

    def __paint_queens(self, painter: QPainter, size: QSizeF):
        pixmap = self.pixmap.scaled(size.toSize())

        for i in range(len(self._solver.queens)):
            painter.drawPixmap(
                QPointF(size.width() * i, size.height() * self._solver.queens[i]),
                pixmap
            )

    def __paint_squares(self, painter: QPainter, n: int, size: QSizeF):
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(QBrush(Qt.darkGray))

        for i, j in product(range(n), range(n)):
            if (i + j) % 2 == 0:
                top_left = QPointF(self.rect().x() + j * size.width(), self.rect().y() + i * size.width())
                draw_rect = QRectF(top_left, size)
                painter.drawRect(draw_rect)


class Graphic(QWidget):
    TEMPERATURE_PEN = mkPen(color='red')
    CONFLICTS_PEN = mkPen(color='blue')

    def __init__(self, storage: HistoryStorage):
        super().__init__()
        self.__storage = storage

        self.__temperature_graphic = PlotWidget(self)
        self.__conflicts_graphic = PlotWidget(self)

        self.__customise_graphics()
        self.__create_layout()

    def paintEvent(self, ev):
        super().paintEvent(ev)
        self._make_plot()

    def clear_graphics(self):
        self.__conflicts_graphic.clear()
        self.__temperature_graphic.clear()

    def _make_plot(self):
        x = range(len(self.__storage.history))
        temperature = [item.temperature for item in self.__storage.history]
        conflicts = [item.conflicts for item in self.__storage.history]
        self.__temperature_graphic.plot(x, temperature, pen=self.TEMPERATURE_PEN)
        self.__conflicts_graphic.plot(x, conflicts, pen=self.CONFLICTS_PEN)

    def __customise_graphics(self):
        self.__temperature_graphic.setBackground('w')
        self.__temperature_graphic.setLabel('left', 'Температура')
        self.__temperature_graphic.setLabel('bottom', 'Шаг')

        self.__conflicts_graphic.setBackground('w')
        self.__conflicts_graphic.setLabel('left', 'Количество конфликтов')
        self.__conflicts_graphic.setLabel('bottom', 'Шаг')

    def __create_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.__temperature_graphic)
        layout.addWidget(self.__conflicts_graphic)
        self.setLayout(layout)
