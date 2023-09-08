import random

from simulated_annealing import SimulatedAnnealing, BehaviorManager, Temperature, Result, State, GibbsDistributionTransitionManager

graph = [
    [0, 19, 41, 39, 27, 20],
    [19, 0, 24, 31, 35, 13],
    [41, 24, 0, 20, 41, 22],
    [39, 31, 20, 0, 26, 20],
    [27, 35, 41, 26, 0, 23],
    [20, 13, 22, 20, 23, 0]
]


class TSPBehaviorManager(BehaviorManager):
    def update_state(self, state, step: int) -> State:
        i1, i2 = random.sample(range(1, len(state) - 2), k=2)
        print(f"Перетасовались {i1}, {i2}")
        state[i1], state[i2] = state[i2], state[i1]

        return state

    def compare_results(self, new: Result, previous: Result) -> bool:
        return new < previous

    def modify_temperature(self, temperature: Temperature, step: int) -> Temperature:
        return temperature * 0.5


def path_len(path: list):
    res = 0
    for i in range(len(path)):
        start = path[i - 1]
        end = path[i]
        res += graph[start - 1][end - 1]

    return res


if __name__ == '__main__':
    annealing = SimulatedAnnealing(
        [1, 4, 3, 5, 6, 2, 1], path_len, 80,
        TSPBehaviorManager(), GibbsDistributionTransitionManager(100)
    )

    while True:
        print("Путь:", annealing.state)
        print("Длина:", annealing.result)
        print("Температура:", annealing.temperature)
        inp = input("Далее...")
        print()

        if inp == 'n':
            break

        annealing.step(0)
        # print(path_len())
