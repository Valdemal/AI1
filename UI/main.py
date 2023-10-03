from typing import Tuple

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from Controller import Solver, HistoryStorage
from .panel import Panel
from .views import Table, Graphic


class MainWidget(QWidget):
    def __init__(self, title: str, size: Tuple[int, int], n_queens: int, temperature: float):
        super().__init__()
        self.resize(*size)
        self.setWindowTitle(title)

        self.__solver = Solver(n_queens, temperature)
        self.__storage = HistoryStorage(self.__solver)

        self.__table = Table(self.width() // 2, self.__solver)
        self.__graphic = Graphic(self.__storage)
        self.__panel = Panel(self, self.__solver, self.__storage)

        self.__create_layout()

    def reset(self, n_queens: int, temperature: float):
        self.__solver.reset(n_queens, temperature)
        self.__storage.clear_history()
        self.__graphic.clear_graphics()

    def __create_layout(self):
        main_layout = QVBoxLayout()
        top = QWidget(self)
        top.setLayout(QHBoxLayout())

        top.layout().addWidget(self.__table)
        top.layout().addWidget(self.__graphic)

        main_layout.addWidget(top)
        main_layout.addWidget(self.__panel)

        self.setLayout(main_layout)
