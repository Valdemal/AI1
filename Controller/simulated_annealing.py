import random
from abc import ABC, abstractmethod
from math import exp
from typing import Any, Callable

# Типы для аннотации
State = Any
Temperature = Any
Step = int
Result = Any


class BehaviorManager(ABC):
    @abstractmethod
    def update_state(self, state, step: int) -> State:
        pass

    @abstractmethod
    def compare_results(self, new: Result, previous: Result) -> bool:
        """Переименовать"""
        pass

    @abstractmethod
    def modify_temperature(self, temperature: Temperature, step: int) -> Temperature:
        pass


class TransitionManager(ABC):
    @abstractmethod
    def transition_available(self, new: Result, previous: Result, temperature: Temperature) -> bool:
        pass


class SimulatedAnnealing:
    def __init__(
            self,
            initial_state: State,
            target: Callable[[State], Result],
            temperature: Temperature,
            behavior_manager: BehaviorManager,
            transition_manager: TransitionManager,
    ):
        self.__state = initial_state
        self.__temperature = temperature
        self.__target = target

        self.__behavior_manager = behavior_manager
        self.__transition_manager = transition_manager

        self.__result = self.__target(self.__state)

    def __call__(self, steps_count: int, *args, **kwargs):
        while steps_count > 0:
            self.step(steps_count)
            steps_count -= 1

        return self.__result

    @property
    def result(self):
        return self.__result

    @property
    def state(self):
        return self.__state

    @property
    def temperature(self):
        return self.__temperature

    def step(self, step_num: int):
        new_state = self.__behavior_manager.update_state(self.__state, step_num)
        new_result = self.__target(new_state)

        if self.__behavior_manager.compare_results(new_result, self.__result) \
                or \
                self.__transition_manager.transition_available(new_result, self.__result, self.__temperature):

            self.__state, self.__result = new_state, new_result

        self.__temperature = self.__behavior_manager.modify_temperature(self.__temperature, step_num)


class GibbsDistributionTransitionManager(TransitionManager):
    def __init__(self, max_threshold: int):
        self.__max_threshold = max_threshold

    def transition_available(self, new: Result, previous: Result, temperature: Temperature) -> bool:
        p = 100 * exp(-(new - previous) / temperature)
        threshold = random.randint(0, self.__max_threshold)

        return p > threshold
