import random
from copy import copy
from math import exp
from typing import List


def swap_elements(array) -> List[int]:
    i1, i2 = random.sample(range(0, len(array) - 1), k=2)
    array[i1], array[i2] = array[i2], array[i1]

    return array


def conflicts(queens: List[int]) -> int:
    # todo скорее всего работает неправильно
    s = 0
    for i in range(len(queens)):
        d = 1
        for j in range(i):
            if abs(i - j) == abs(queens[i] - queens[j]):
                d = 0
        s += d

    return s


class Controller:
    def __init__(self):
        self.reset(3, 1)

    def reset(self, queens_count: int, temperature: float):
        self.__queens = list(range(queens_count))
        random.shuffle(self.__queens)
        self.__temperature = temperature
        self.__conflicts = conflicts(self.__queens)

    @property
    def queens(self) -> List[int]:
        return self.__queens

    @property
    def conflicts(self):
        return self.__conflicts

    @property
    def temperature(self):
        return self.__temperature

    def step(self):
        new_state = swap_elements(self.__queens)
        new_result = conflicts(new_state)

        if new_result < self.conflicts or self._transition_available(new_result, self.conflicts, self.temperature):
            self.__queens, self.__conflicts = new_state, new_result

        self.__temperature *= 0.5

    class Memento:
        def __init__(self, queens, temperature):
            self.__queens = copy(queens)
            self.__temperature = temperature

        @property
        def queens(self):
            return self.__queens

        @property
        def temperature(self):
            return self.__temperature

    def save(self) -> Memento:
        return self.Memento(self.queens, self.temperature)

    def restore(self, memento: Memento):
        self.__queens = memento.queens
        self.__temperature = memento.temperature
        self.__conflicts = conflicts(self.__queens)

    @staticmethod
    def _transition_available(new: int, previous: int, temperature: float) -> bool:
        p = 100 * exp(-(new - previous) / temperature)
        threshold = random.randint(0, 80)

        return p > threshold


class HistoryStorage:
    def __init__(self, controller: Controller):
        self.__controller = controller
        self.__history = ArrayList()
        self.__history.push_forward(self.__controller.save())

    @property
    def history(self) -> List[Controller.Memento]:
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
