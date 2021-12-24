import random
from math import factorial
from typing import List, Union


class Thing:
    def __init__(self,
                 name: str,
                 hp_buff: float,
                 atk_buff: float,
                 def_buff: float) -> None:
        self.name = name
        self.hp_buff = hp_buff
        self.atk_buff = atk_buff
        self.def_buff = def_buff

    def get_stat(self, stat_name: str) -> Union[float, str]:
        stats = {
            'name': self.name,
            'hp_buff': self.hp_buff,
            'atk_buff': self.atk_buff,
            'def_buff': self.def_buff
        }
        return stats[stat_name]

    def add_word_to_name(self, word: str) -> None:
        self.name = self.name + word


class Ring(Thing):
    def __init__(self,
                 name: str,
                 hp_buff: float,
                 atk_buff: float,
                 def_buff: float) -> None:
        super().__init__(atk_buff=atk_buff,
                         hp_buff=hp_buff*2,
                         def_buff=def_buff*0,
                         name=name)
        self.name = f'Кольцо {name}'


class Helmet(Thing):
    def __init__(self,
                 name: str,
                 hp_buff: float,
                 atk_buff: float,
                 def_buff: float) -> None:
        super().__init__(hp_buff=hp_buff*0.5,
                         atk_buff=atk_buff*0,
                         def_buff=def_buff*0.5,
                         name=name)
        self.name = f'Шлем {name}'


class Armor(Thing):
    def __init__(self,
                 name: str,
                 hp_buff: float,
                 atk_buff: float,
                 def_buff: float) -> None:
        super().__init__(hp_buff=hp_buff,
                         atk_buff=atk_buff*0.1,
                         def_buff=def_buff*2,
                         name=name)
        self.name = f'Доспех {name}'


class Weapon(Thing):
    weapon_type_list = ['Меч',
                        'Топор',
                        'Лук',
                        'Копье',
                        'Кинжал']

    def __init__(self,
                 name: str,
                 hp_buff: float,
                 atk_buff: float,
                 def_buff: float) -> None:

        super().__init__(hp_buff=hp_buff*0,
                         atk_buff=atk_buff*2,
                         def_buff=def_buff*0,
                         name=name)
        self.name = f'{random.choice(self.weapon_type_list)} {name}'

    # Для рассчета максимального количества названий предметов
    @staticmethod
    def get_weapon_type_number() -> int:
        return len(Weapon.weapon_type_list)


class Person:
    def __init__(self,
                 name: str = 'Noname',
                 hitpoints: float = 1000,
                 attack: float = 100,
                 defence: float = 10) -> None:
        self.name = name
        self.hitpoints = hitpoints
        self.attack = attack
        self.defence = defence
        self.things_list = []
        # Нужно для того, чтобы хитпоинты просчитывались только один раз
        self.check = False

    def set_things(self, thing: 'Thing') -> None:
        self.things_list.append(thing)
        self.check = False

    def get_things(self) -> List['Thing']:
        return self.things_list

    def get_stat(self, stat_name: str) -> Union[str, float]:
        stats = {'name': self.name,
                 'hitpoints': self.hitpoints,
                 'attack': self.attack,
                 'defence': self.defence}
        return stats[stat_name]

    def get_hitpoints_final(self) -> float:
        if not self.check:
            self.check = True
            if len(self.things_list) == 0:
                return self.hitpoints
            return sum([thing.hp_buff for thing in self.get_things()],
                       self.hitpoints)
        return self.hitpoints

    def get_attack_final(self) -> float:
        if len(self.things_list) == 0:
            return self.attack
        return sum([thing.atk_buff for thing in self.get_things()],
                   self.attack)

    def get_defence_final(self) -> float:
        if len(self.things_list) == 0:
            return self.defence
        return sum([thing.def_buff for thing in self.get_things()],
                   self.defence)

    def attacked(self, attack_damage: float) -> float:
        absorbed_damage = attack_damage*(self.get_defence_final()*0.01)
        if absorbed_damage > attack_damage:
            final_damage = 5
        else:
            final_damage = attack_damage - absorbed_damage
        self.hitpoints = self.get_hitpoints_final() - final_damage
        return final_damage


class Warrior(Person):
    def __init__(self,
                 name: str = 'Noname',
                 hitpoints: float = 1000,
                 attack: float = 100,
                 defence: float = 10) -> None:
        super().__init__(name=name,
                         hitpoints=hitpoints,
                         attack=attack,
                         defence=defence)
        self.name = f'Воин {name}'
        self.attack *= 2


class Paladin(Person):
    def __init__(self,
                 name: str = 'Noname',
                 hitpoints: float = 1000,
                 attack: float = 100,
                 defence: float = 10) -> None:
        super().__init__(name=name,
                         hitpoints=hitpoints,
                         attack=attack,
                         defence=defence)
        self.name = f'Паладин {name}'
        # Паладины слишком часто побеждают при повышении в 2 раза
        self.hitpoints *= 1.5
        self.defence *= 1.5


def generate_things():
    list_of_things = []
    list_of_existing_names = []
    amount_of_things = random.randint(1, 20)
    items_added = 0
    list_of_types = [Ring, Helmet, Armor, Weapon]
    random_additions = [
        'Тьмы',
        'Света',
        'Хаоса',
        'Порядка',
        'Силы',
        'Мощи',
        'Богов'
    ]
    # В зависимости от длины списка random_additions и количества класcов
    # предметов (и отдельна для оружий - видов оружий) меняется максимальное
    # возможное количество комбинаций слов для составления имен.
    # Сочетание без повторений = n!/(m!(n-m)!) , где m < n
    # А может это и не сочетание без повторений и я это зря считаю :/
    number_of_types = (len(list_of_types) +
                       Weapon.get_weapon_type_number() - 1)
    # Чтобы было проще читать
    n = number_of_types
    m = len(random_additions)
    max_number_of_items = factorial(n) / (factorial(m) * factorial(n-m))
    if amount_of_things > max_number_of_items:
        amount_of_things = max_number_of_items
    while items_added < amount_of_things:
        item_to_add = random.choice(list_of_types)(
                                    name=random.choice(random_additions),
                                    hp_buff=random.randint(10, 100),
                                    atk_buff=random.randint(10, 100),
                                    def_buff=random.randint(1, 10)
                                )
        if item_to_add.get_stat('name') not in list_of_existing_names:
            list_of_existing_names.append(item_to_add.get_stat('name'))
            list_of_things.append(item_to_add)
            items_added += 1
    list_of_things = sorted(list_of_things, key=lambda x: x.def_buff)
    return list_of_things


def create_combatant(list_of_things: List[Thing]) -> List[Union[Person,
                                                                List[Thing]]]:
    right_choice = False
    things_copy = list_of_things
    print('Выберите класс:')
    # Да, тут будет много принтов если много классов
    print('Воин: Атака повышается в 2 раза')
    print('Паладин: Здоровье и защита повышаются в 1.5 раз')
    dict_of_classes = {
        'Паладин': Paladin,
        'Воин': Warrior
    }
    while not right_choice:
        chosen_class = input('Введите название выбранного класса (или '
                             'оставьте пустым для выбора случайного класса) ')
        if chosen_class in dict_of_classes.keys():
            confirm = input(f'Вы выбрали класс {chosen_class}, продолжить? '
                            'Если хотите сменить класс, введите -,'
                            'иначе введите + ')
            if confirm == '+':
                chosen_class = dict_of_classes[chosen_class]
                right_choice = True
        elif chosen_class == '':
            chosen_class = random.choice(list(dict_of_classes.keys()))
            confirm = input(f'Случайно выбран {chosen_class}, продолжить? '
                            'Если хотите сменить класс, введите -,'
                            'иначе введите + ')
            if confirm == '+':
                chosen_class = dict_of_classes[chosen_class]
                right_choice = True
        else:
            print('Такого класса нет, попробуйте снова.')
    right_choice = False
    while not right_choice:
        chosen_name = input('Введите имя воина ')
        confirm = input(f'Вы ввели имя {chosen_name}, продолжить?'
                        'Если хотите сменить имя, введите -,'
                        'иначе введите + ')
        if confirm == '+':
            right_choice = True
    right_choice = False
    attribute_points_fixed = random.randint(250, 500)
    attribute_points = attribute_points_fixed
    default_hitpoints = 550
    default_attack = 115
    default_defence = 7
    hitpoints_points = default_hitpoints  # мда
    attack_points = default_attack
    defence_points = default_defence
    attribute_dict = {
        '1': 'Здоровью',
        '2': 'Атаке',
        '3': 'Защите'
    }
    while not right_choice:
        print(f'У вас {attribute_points} очков. Куда хотите их потратить?')
        print('Ваши текущие характеристики (без учета классового бонуса):')
        print(f'1) Здоровье: {hitpoints_points} '
              '(1 очко + 1 к характеристике)')
        print(f'2) Атака: {attack_points} '
              '(1 очко + 0.5 к характеристике)')
        print(f'3) Защита: {defence_points} '
              '(1 очко + 0.05 к характеристике)')
        chosen_attribute = input('Введите цифру атрибута для добавления '
                                 'очков, введите + для перехода к '
                                 'следующему шагу, - для сброса ')
        # Тут может быть ошибка, тогда просто заменить if 1 then if 2 then
        if chosen_attribute in attribute_dict:
            how_much_to_add = int(input(
                'Прибавить к '
                f'{attribute_dict[chosen_attribute]} '))
            if int(how_much_to_add) <= attribute_points:
                if chosen_attribute == '1':
                    hitpoints_points += how_much_to_add
                elif chosen_attribute == '2':
                    attack_points += how_much_to_add*0.5
                else:
                    defence_points += how_much_to_add*0.05
                attribute_points -= how_much_to_add
        elif chosen_attribute == '-':
            hitpoints_points = default_hitpoints
            attack_points = default_attack
            defence_points = default_defence
            attribute_points = attribute_points_fixed
        elif chosen_attribute == '+':
            right_choice = True
    right_choice = False
    combatant = chosen_class(
        name=chosen_name,
        hitpoints=hitpoints_points,
        attack=attack_points,
        defence=defence_points
    )
    allowed_items = random.randint(0, 3)
    if allowed_items == 0:
        return [combatant, things_copy]
    while not right_choice:
        print(f'Вы можете взять {allowed_items} предметов из списка: ')
        print('------------')
        for item in things_copy:
            print(f'Название предмета: {item.get_stat("name")}')
            print('Характеристики')
            print(f'Бонус к здоровью: {item.get_stat("hp_buff")}')
            print(f'Бонус к атаке: {item.get_stat("atk_buff")}')
            print(f'Бонус к защите: {item.get_stat("def_buff")}')
            print('------------')
        chosen_item = input('Введите название предмета чтобы подобрать '
                            'его, введите + чтобы продолжить ')
        if chosen_item in [thing.get_stat('name') for thing in things_copy]:
            chosen_item = [item for item in things_copy
                           if item.get_stat('name') == chosen_item][0]
            combatant.set_things(chosen_item)
            things_copy.remove(chosen_item)
            allowed_items -= 1
            if allowed_items == 0:
                right_choice = True
        elif chosen_item == '+':
            right_choice = True
    return [combatant, things_copy]


def generate_combatants() -> List[Person]:
    list_of_combatants = []
    list_of_existing_names = []
    list_of_types = [Warrior, Paladin]
    combatants_added = 0
    # Искал список фентезийных имен, нашел список скандинавских имен. Таким
    # образом мы доказали, что скандинавов не существует.
    random_names = [
        'Арнвид',
        'Асбьёрн',
        'Бьёргольв',
        'Бродди',
        'Вестар',
        'Грани',
        'Гисли',
        'Ингвар',
        'Квельдульв'
    ]
    number_of_types = len(list_of_types)
    # Опять использую формулу выше, потому опять привожу к n и m для удобства
    n = len(random_names)
    m = number_of_types
    max_number_combatants = factorial(n) / (factorial(m) * factorial(n-m))
    amount_of_combatants = random.randint(5, 15)
    if amount_of_combatants > max_number_combatants:
        amount_of_combatants = max_number_combatants
    while combatants_added < amount_of_combatants:
        combatant_to_add = random.choice(list_of_types)(
            name=random.choice(random_names),
            hitpoints=random.randint(500, 1000),
            attack=random.randint(100, 150),
            defence=random.randint(5, 15)
        )
        if combatant_to_add.get_stat('name') not in list_of_existing_names:
            list_of_existing_names.append(combatant_to_add.get_stat('name'))
            list_of_combatants.append(combatant_to_add)
            combatants_added += 1
    return list_of_combatants


def give_items_to_combatants(items: List[Thing],
                             combatants: List[Person]) -> List[Person]:
    items_list = items
    combatants_list = combatants
    items_number = len(items_list)
    if items_number <= 0:
        return combatants_list
    for combatant in combatants_list:
        items_number = len(items_list)
        if items_number == 0:
            break
        elif items_number < 3:
            number_of_items_to_give = random.randint(0, items_number)
        else:
            number_of_items_to_give = random.randint(0, 3)
        # Вообще стоит проверять что дают, чтобы не вышло 4 шлема, но это уже
        # потом как-нибудь
        items_to_give = random.sample(items_list, number_of_items_to_give)
        for item in items_to_give:
            combatant.set_things(item)
            items_list.remove(item)
    return combatants_list


def battle(attacker: Person, defender: Person) -> bool:
    attacker_name = attacker.get_stat('name')
    defender_name = defender.get_stat('name')
    print(f'{attacker_name} нападает на {defender_name}')
    attack_damage = attacker.get_attack_final()
    hp_lost = round(defender.attacked(attack_damage), 3)
    print(f'{attacker_name} наносит удар по {defender_name} '
          f'на {hp_lost} урона!')
    print(f'У {defender_name} осталось '
          f'{round(defender.get_hitpoints_final(), 2)} hp')
    print('')
    if defender.get_hitpoints_final() <= 0:
        return True
    return False


def arena(character_list: List[Person]) -> None:
    is_it_over = False
    on_arena = character_list  # Список тех, кто все еще на арене (меняется)
    battle_number = 0
    while not is_it_over:
        print(f'Раунд {battle_number}')
        battle_participants = random.sample(on_arena, 2)
        # Если после боя есть победитель
        if battle(battle_participants[0], battle_participants[1]):
            attacker_name = battle_participants[0].get_stat('name')
            defender_name = battle_participants[1].get_stat('name')
            print(f'{attacker_name} победил {defender_name}!')
            on_arena.remove(battle_participants[1])
        if len(on_arena) == 1:
            is_it_over = True
        battle_number += 1
    winner_name = on_arena[0].get_stat('name')
    print(f'На арене не осталось никого, кроме {winner_name}! '
          'Он - победитель!')


list_of_things = generate_things()
list_of_combatants = generate_combatants()
choice = input('Хотите создать персонажа? Введите + для создания ')
if choice == '+':
    player_and_items = create_combatant(list_of_things)
    list_of_combatants.append(player_and_items[0])
    list_of_things = player_and_items[1]
list_of_combatants = give_items_to_combatants(list_of_things,
                                              list_of_combatants)
arena(list_of_combatants)