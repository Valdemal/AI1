from typing import Tuple

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGridLayout, QLabel, QLineEdit

from Controller import Controller, HistoryStorage
from .views import Table, Graphic


class Panel(QWidget):
    def __init__(self, mediator: 'MainWidget', controller: Controller, storage: HistoryStorage, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=mediator)

        self.__mediator = mediator
        self.__controller = controller
        self.__storage = storage
        self.__in_process = False

        self.__conflicts_label = QLabel(f"Конфликты: {self.__controller.conflicts}", parent=self)

        self.__queens_count_input = QLineEdit(str(len(self.__controller.queens)))
        self.__temperature_input = QLineEdit(str(self.__controller.temperature))

        self.__step_solution_button = QPushButton('Пошаговое решение')
        self.__instance_solution_button = QPushButton('Мгновенное решение')
        self.__step_forward_button = QPushButton("Шаг вперед", parent=self)
        self.__step_back_button = QPushButton("Шаг назад", parent=self)
        self.__reset_button = QPushButton("Сбросить решение")

        self.resize(self.parent().width(), self.parent().height() // 3)

        self.__create_layout()
        self.__attach_events()
        self.__disable()

    def _step_forward(self):
        self.__storage.do()
        self.__step_back_button.setEnabled(True)
        self._update()

    def _step_back(self):
        self.__storage.undo()

        if self.__storage.on_start():
            self.__step_back_button.setEnabled(False)

        self._update()

    def _update(self):
        self.__temperature_input.setText(str(self.__controller.temperature))
        self.__conflicts_label.setText(f"Конфликты: {self.__controller.conflicts}")
        self.__mediator.update()

    def _step_solution(self):
        self.__enable()
        self.__mediator.update()

    def _instance_solution(self):
        self.__enable()
        self.__mediator.update()

    def _reset_solution(self):
        self.__disable()
        self.__mediator.update()

    def __disable(self):
        self.__in_process = False

        self.__queens_count_input.setEnabled(True)
        self.__temperature_input.setEnabled(True)
        self.__step_forward_button.setEnabled(False)
        self.__step_back_button.setEnabled(False)

        self.__step_solution_button.setVisible(True)
        self.__instance_solution_button.setVisible(True)
        self.__reset_button.setVisible(False)

    def __enable(self):
        self.__in_process = True

        self.__controller.reset(int(self.__queens_count_input.text()), float(self.__temperature_input.text()))
        self.__queens_count_input.setEnabled(False)
        self.__temperature_input.setEnabled(False)
        self.__step_forward_button.setEnabled(True)

        self.__step_solution_button.setVisible(False)
        self.__instance_solution_button.setVisible(False)
        self.__reset_button.setVisible(True)

    def __attach_events(self):
        self.__step_forward_button.clicked.connect(self._step_forward)
        self.__step_back_button.clicked.connect(self._step_back)
        self.__step_solution_button.clicked.connect(self._step_solution)
        self.__instance_solution_button.clicked.connect(self._instance_solution)
        self.__reset_button.clicked.connect(self._reset_solution)

    def __create_layout(self):
        self.setLayout(QGridLayout())
        self.layout().addWidget(QLabel("Количество ферзей: "), 0, 0)
        self.layout().addWidget(self.__queens_count_input, 0, 1)
        self.layout().addWidget(self.__step_solution_button, 1, 0, )
        self.layout().addWidget(self.__instance_solution_button, 1, 1)
        self.layout().addWidget(self.__step_forward_button, 0, 2)
        self.layout().addWidget(self.__step_back_button, 1, 2)
        self.layout().addWidget(QLabel("Температура: "), 0, 3)
        self.layout().addWidget(self.__conflicts_label, 1, 3)
        self.layout().addWidget(self.__temperature_input, 0, 4)

        self.layout().addWidget(self.__step_solution_button, 1, 0)
        self.layout().addWidget(self.__instance_solution_button, 1, 1)
        self.layout().addWidget(self.__reset_button, 1, 0, 1, 2)


class MainWidget(QWidget):
    def __init__(self, title: str, size: Tuple[int, int]):
        super().__init__()
        self.resize(*size)
        self.setWindowTitle(title)

        controller = Controller()
        storage = HistoryStorage(controller)

        self.__table = Table(self.width() // 2, controller)
        self.__graphic = Graphic(storage)
        self.__panel = Panel(self, controller, storage)

        self.__create_layout()

    def update_view(self):
        self.__table.repaint()
        # self.__graphic.repaint()

    def __create_layout(self):
        main_layout = QVBoxLayout()
        top = QWidget(self)
        top.setLayout(QHBoxLayout())

        top.layout().addWidget(self.__table)
        top.layout().addWidget(self.__graphic)

        main_layout.addWidget(top)
        main_layout.addWidget(self.__panel)

        self.setLayout(main_layout)
