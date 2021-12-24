def counter(func):
    """Cчитает и печатает количество вызовов декорируемой функции."""
    count = {}
    # Создаем запись в словаре с ключом в виде имени декорируемой функции
    # В качестве ключа используем имя функции, полученное 
    # из магического метода
    count[func.__name__] = 0

    def wrapper(*args, **kwargs):
        # При вызове добавили к счётчику единицу и напечатали результат
        count[func.__name__] += 1
        print(f'Количество вызовов {func.__name__}: {count[func.__name__]}')
        return func(*args, **kwargs)
    return wrapper


def dealer(func):
    """Делает что-то полезное до и после вызова декорируемой функции."""
    def wrapper(*args, **kwargs):
        print('Полезная работа декоратора до вызова функции')
        result = func(*args, **kwargs)
        print('Полезная работа декоратора после вызова функции')
        return result
    return wrapper


def logger(func):
    """Печатает аргументы, переданные в декорируемую функцию."""
    def wrapper(*args, **kwargs):
        print(f'{func.__name__} вызвана с аргументами: {args} {kwargs}')
        return func(*args, **kwargs)
    return wrapper


# @dealer
# @counter
# def first():
    # pass


# first()
# first()


@logger
@counter
def second(variable):
    pass


second('Параметр')
second({'Ключ': 'Значение'})


