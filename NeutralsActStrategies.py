import random


def get_around_cells(cell, dist, height, width):
    res = set()
    for d in range(1, dist + 1):
        for i in range(-d, d + 1):
            res.add((cell[0] + i, cell[1] + d))
            res.add((cell[0] + i, cell[1] - d))
            res.add((cell[0] + d, cell[1] + i))
            res.add((cell[0] - d, cell[1] - i))
    new_res = []
    for elem in res:
        if 0 <= elem[0] and elem[0] < height and 0 <= elem[1] and elem[1] < width:
            new_res.append(elem)
    return new_res


class NormalCalmNeutralsActStrategy:
    def __init__(self):
        pass

    def get_action_cell(self, unit, board):
        options = []
        if random.randint(1, 10) > 1:
            # attack
            for cell in get_around_cells(unit.cell, unit.attack_dist, len(board.units_array), len(board.units_array[0])):
                if not board.units_array[cell[0]][cell[1]] is None \
                        and board.units_array[cell[0]][cell[1]].owner.name != 'Neutrals':
                    options.append(cell)
        else:
            # move
            for cell in get_around_cells(unit.cell, unit.speed, len(board.units_array), len(board.units_array[0])):
                if board.units_array[cell[0]][cell[1]] is None:
                    options.append(cell)
        return random.choice(options) if len(options) > 0 else unit.cell
