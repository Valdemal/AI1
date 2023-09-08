import random
from typing import List

from Controller.simulated_annealing import Temperature, Result, State, TransitionManager
from .simulated_annealing import SimulatedAnnealing, BehaviorManager, GibbsDistributionTransitionManager


class NQueensBehaviorManager(BehaviorManager):

    def update_state(self, state, step: int) -> State:
        i1, i2 = random.sample(range(0, len(state) - 1), k=2)
        state[i1], state[i2] = state[i2], state[i1]

        return state

    def compare_results(self, new: Result, previous: Result) -> bool:
        return new < previous

    def modify_temperature(self, temperature: Temperature, step: int) -> Temperature:
        return temperature * 0.5


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


class NQueensTask(SimulatedAnnealing):
    def __init__(self, initial_state: State, temperature: Temperature, transition_manager: TransitionManager):
        super().__init__(initial_state, conflicts, temperature, NQueensBehaviorManager(), transition_manager)


class Controller:
    def __init__(self):
        self.__transition_manager = GibbsDistributionTransitionManager(100)
        self.__model = NQueensTask(
            [1], 80, self.__transition_manager
        )
        self.__history: List[Controller.Memento] = [self._save()]

    def reset(self, queens_count: int, temperature: float):
        self.__model = NQueensTask(queens_count, temperature, self.__transition_manager)

    @property
    def queens(self) -> List[int]:
        return self.__model.state

    @property
    def conflicts(self):
        return self.__model.result

    @property
    def temperature(self):
        return self.__model.temperature

    @property
    def history(self) -> List['Memento']:
        return self.__history

    def make_step(self):
        self.__model.step(len(self.__history))
        self.__history.append(self._save())

    class Memento:
        def __init__(self, state, temperature):
            self.__state = state
            self.__temperature = temperature

        @property
        def state(self):
            return self.__state

        @property
        def temperature(self):
            return self.__temperature

    def _save(self) -> Memento:
        return self.Memento(self.__model.state, self.__model.temperature)

    def _restore(self, memento: Memento):
        self.__model = NQueensTask(memento.state, memento.temperature, self.__transition_manager)

