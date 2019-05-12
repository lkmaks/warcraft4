import random


class NormalRandomNeutralsGenerateStrategy:
    def __init__(self):
        pass

    def generate_unit_names_array(self, units_array, is_spawn1, is_spawn2, names):
        names_list = list(names)
        res = [[None] * len(units_array[i]) for i in range(len(units_array))]
        for i in range(len(units_array)):
            for j in range(len(units_array[i])):
                if not is_spawn1[i][j] and not is_spawn2[i][j]:
                    if random.randint(0, 30) == 0:
                        res[i][j] = random.choice(names_list)
        return res
