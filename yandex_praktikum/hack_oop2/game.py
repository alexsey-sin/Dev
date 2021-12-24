import random
from colorama import init, Fore


names = ['Берси', 'Бо', 'Болли', 'Бранд', 'Калле', 'Карл', 'Клаус', 'Оддманд',
         'Ойвинд', 'Ойстейн', 'Торольв', 'Торгейр', 'Торгисл', 'Тормод', 'Фридрик',
         'Фроди', 'Фридмунд', 'Хакон', 'Халлстеинн', 'Хальфсен', 'Хаук', 'Эйольв',
         'Эйвинд', 'Эймунд']

things_name = ['палица', 'булава', 'шестопер', 'кистень', 'дубина', 'шлем',
               'доспехи', 'меч', 'сабля', 'копье', 'рогатина', 'топор', 'лук', 'кольца']


class Thing:
    def __init__(self, name, defense, attack, life):
        self.name = name
        self.defense = defense
        self.attack = attack
        self.life = life


class Person:
    things = []

    def __init__(self, name, lifes, base_attack, base_defense):
        self.name = name
        self.lifes = lifes
        self.base_attack = base_attack
        self.base_defense = base_defense

    def setThings(self, thing: Thing):
        self.lifes += thing.life
        self.base_attack += thing.attack
        self.base_defense += thing.defense

    def setLife(self, attack):
        self.lifes -= attack


class Paladin(Person):
    def __init__(self, name, lifes, base_attack, base_defense):
        super().__init__(name, lifes, base_attack, base_defense)
        self.lifes = lifes * 2
        self.base_defense = base_defense * 2


class Warrior(Person):
    def __init__(self, name, lifes, base_attack, base_defense):
        super().__init__(name, lifes, base_attack, base_defense)
        self.base_attack = base_attack * 2


def CreatePerson():
    n = random.randint(1, 2)
    if n == 1:
        return Paladin(name=random.choice(names), lifes=random.randint(5, 10),
            base_attack=random.randint(3, 10), base_defense=random.randint(3, 10)/100)
    else:
        return Warrior(name=random.choice(names), lifes=random.randint(5, 10),
            base_attack=random.randint(3, 10), base_defense=random.randint(3, 10)/100)


if __name__ == '__main__':
    init()
    # 1 Генерим список вещей
    things = sorted([Thing(name=random.choice(things_name), defense=random.randint(1, 10)/100,
        attack=random.randint(1, 10), life=random.randint(1, 10)) for _ in range(40)
        ], key=lambda x: x.defense)

    # 2 Создаем персонажей
    mob = [CreatePerson() for _ in range(10)]

    # Комплектуемся
    for per in mob:
        n = random.randint(1, 4)
        for _ in range(n):
            if len(things) > 0:
                per.setThings(things.pop(random.randrange(len(things))))

    # выходим на арену
    while True:
        # Выбираем нападающего
        if len(mob) > 1:
            id_s = random.randrange(len(mob))
            id_d = random.randrange(len(mob))
        else:
            print(Fore.GREEN + 'Победил: {}'.format( mob[0].name))
            break

        attack_damage = mob[id_s].base_attack - mob[id_s].base_attack * mob[id_d].base_defense
        mob[id_d].setLife(attack_damage)
        print(Fore.YELLOW + '{}'.format(mob[id_s].name),
            Fore.WHITE + 'наносит удар по',
            Fore.YELLOW + '{}'.format(mob[id_d].name),
            Fore.WHITE + 'на {:.3f} урона.'.format(attack_damage))
        if mob[id_d].lifes <= 0:
            mob.pop(id_d)


