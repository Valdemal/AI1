import random
from copy import copy
from math import exp
from typing import List


def swap_elements(array) -> List[int]:
    i1, i2 = random.sample(range(0, len(array) - 1), k=2)
    array[i1], array[i2] = array[i2], array[i1]

    return array


def compute_conflicts(queens: List[int]) -> int:
    # todo скорее всего работает неправильно
    s = 0
    for i in range(len(queens)):
        d = 1
        for j in range(i):
            if abs(i - j) == abs(queens[i] - queens[j]):
                d = 0
        s += d

    return s


class Solver:
    def __init__(self, queens_count: int, temperature: float):
        self.__queens = list(range(queens_count))
        random.shuffle(self.__queens)
        self.__temperature = temperature
        self.__conflicts = compute_conflicts(self.__queens)

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
        new_result = compute_conflicts(new_state)

        if new_result < self.conflicts or self._transition_available(new_result, self.conflicts, self.temperature):
            self.__queens, self.__conflicts = new_state, new_result

        self.__temperature *= 0.5

    class Memento:
        def __init__(self, queens, temperature, conflicts):
            self.__queens = copy(queens)
            self.__temperature = temperature
            self.__conflicts = conflicts

        @property
        def queens(self) -> List[int]:
            return self.__queens

        @property
        def temperature(self) -> float:
            return self.__temperature

        @property
        def conflicts(self) -> int:
            return self.__conflicts

    def save(self) -> Memento:
        return self.Memento(self.queens, self.temperature, self.conflicts)

    def restore(self, memento: Memento):
        self.__queens = memento.queens
        self.__temperature = memento.temperature
        self.__conflicts = compute_conflicts(self.__queens)

    @staticmethod
    def _transition_available(new: int, previous: int, temperature: float) -> bool:
        p = 100 * exp(-(new - previous) / temperature)
        threshold = random.randint(0, 80)

        return p > threshold

