import os

def mapgen(is_gold, spawn1, spawn2):
    arr = None
    with open(os.path.dirname(os.path.abspath(__file__)) + '/map.txt') as file:
        for s in file:
            s = s.strip()
            if s == "is_gold":
                arr = is_gold
            elif s == "spawn1":
                arr = spawn1
            elif s == "spawn2":
                arr = spawn2
            else:
                x, y = map(int, s.split())
                arr[x][y] = True

