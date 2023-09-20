from typing import List

from Controller import Solver


class HistoryStorage:
    def __init__(self, controller: Solver):
        self.__controller = controller
        self.__history = ArrayList()
        self.__history.push_forward(self.__controller.save())

    @property
    def history(self) -> List[Solver.Memento]:
        return self.__history.values

    def on_start(self) -> bool:
        return self.__history.on_start()

    def undo(self):
        self.__history.step_back()
        self.__controller.restore(self.__history.current)

    def do(self):
        if self.__history.on_end():
            self.__controller.step()
            self.__history.push_forward(self.__controller.save())
            self.__history.step_forward()
        else:
            self.__history.step_forward()
            self.__controller.restore(self.__history.current)


class ArrayList:
    def __init__(self):
        self.__values = []
        self.__pos = 0

    @property
    def values(self) -> list:
        return self.__values

    @property
    def current(self):
        return self.__values[self.__pos]

    def push_forward(self, value):
        self.__values.append(value)

    def step_back(self):
        if not self.on_start():
            self.__pos -= 1

    def step_forward(self):
        if not self.on_end():
            self.__pos += 1

    def on_start(self) -> bool:
        return self.__pos == 0

    def on_end(self) -> bool:
        return self.__pos == len(self.__values) - 1
