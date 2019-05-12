
class BattleAction:
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest

    def log(self):
        print(type(self).__name__ + " from {} to {}".format(self.source.name, self.dest.name))


class NormalUnitAttack(BattleAction):
    def __init__(self, damage, damage_type, source, dest):
        super().__init__(source, dest)
        self.damage = damage
        self.damage_type = damage_type


class PriestHeal(BattleAction):
    def __init__(self, heal, source, dest):
        super().__init__(source, dest)
        self.heal = heal


class BomberDetonation(BattleAction):
    def __init__(self, damage, radius, source):
        super().__init__(source, source)
        self.damage = damage
        self.radius = radius
