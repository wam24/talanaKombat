from abc import ABC


class PersonageBase(ABC):
    def __init__(self, name, life):
        self.name = name
        self.life = life

    def attack(self, action):
        damage = 1
        if 'P' == action:
            return damage, 'Puño'
        elif 'K' == action:
            return damage, 'Patada'

    def special_attack_1(self):
        pass

    def special_attack_2(self):
        pass

    def attack_combination(self, move, action):
        pass


class PersonagePlayer1(PersonageBase):

    def __init__(self):
        super().__init__(name="Tonyn Stallone", life=6)

    def special_attack_1(self):
        damage = 3
        name_attack = 'Taladoken'
        return damage, name_attack

    def special_attack_2(self):
        damage = 2
        name_attack = 'Remuyuken'
        return damage, name_attack

    def attack_combination(self, move, action):
        if move.endswith('DSD') and action == 'P':
            return self.special_attack_1()
        elif move.endswith('SD') and action == 'K':
            return self.special_attack_2()
        elif action == 'P' or action == 'K':
            return self.attack(action)
        else:
            return 0, ''


class PersonagePlayer2(PersonageBase):

    def __init__(self):
        super().__init__(name="Arnaldor Shuatseneguer", life=6)

    def special_attack_1(self):
        damage = 3
        name_attack = 'Remuyuken'
        return damage, name_attack

    def special_attack_2(self):
        damage = 2
        name_attack = 'Taladoken'
        return damage, name_attack

    def attack_combination(self, move, action):

        if move.endswith('SA') and action == 'K':
            return self.special_attack_1()
        elif move.endswith('ASA') and action == 'P':
            return self.special_attack_2()
        elif action == 'P' or action == 'K':
            return self.attack(action)
        else:
            return 0, ''
