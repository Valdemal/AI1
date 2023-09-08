from abc import abstractmethod
from typing import Tuple

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGridLayout, QLabel, QTextEdit, QLineEdit

from Controller import Controller
from .views import Table


class Mediator(QWidget):
    @abstractmethod
    def notify(self, event: str):
        pass


class Panel(QWidget):
    def __init__(self, mediator: Mediator, controller: Controller, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=mediator)

        self.__mediator = mediator
        self.__controller = controller
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
        self.__controller.make_step()
        self.__mediator.notify('step_forward')

    def _step_solution(self):
        self.__enable()

    def _instance_solution(self):
        self.__enable()

    def _reset_solution(self):
        self.__disable()
    #
    # def _step_back(self):
    #     self.__controller.step_back()
    #     self.__mediator.notify('step_back')

    def __disable(self):
        self.__in_process = False

        self.__queens_count_input.setEnabled(True)
        self.__step_forward_button.setEnabled(False)
        self.__step_back_button.setEnabled(False)

        self.__step_solution_button.setVisible(True)
        self.__instance_solution_button.setVisible(True)
        self.__reset_button.setVisible(False)

    def __enable(self):
        self.__in_process = True

        self.__queens_count_input.setEnabled(False)
        self.__step_forward_button.setEnabled(True)
        self.__step_back_button.setEnabled(True)

        self.__step_solution_button.setVisible(False)
        self.__instance_solution_button.setVisible(False)
        self.__reset_button.setVisible(True)

    def __attach_events(self):
        self.__step_forward_button.clicked.connect(self._step_forward)
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




class MainWidget(Mediator):
    def __init__(self, title: str, size: Tuple[int, int]):
        super().__init__()
        self.resize(*size)
        self.setWindowTitle(title)

        controller = Controller()

        self.__table = Table(self.width() // 2, controller)
        self.__graphic = QPushButton("График")
        self.__panel = Panel(self, controller)

        self.__create_layout()

    def notify(self, event: str):
        if event == 'step_forward':
            self._update_view()

    def _update_view(self):
        self.__table.repaint()

    def __create_layout(self):
        main_layout = QVBoxLayout()
        top = QWidget(self)
        top.setLayout(QHBoxLayout())
        top.layout().addWidget(self.__table)
        top.layout().addWidget(self.__graphic)

        main_layout.addWidget(top)
        main_layout.addWidget(self.__panel)

        self.setLayout(main_layout)
