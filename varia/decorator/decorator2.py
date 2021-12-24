'''
Напишите функцию-декоратор, которая сохранит (закеширует) значение декорируемой функции.
Если декорируемая функция будет вызвана повторно с теми же параметрами — декоратор должен вернуть сохранённый результат, не выполняя функцию.
'''
import time


def time_check(func):
    def wrapper(*args):
        start_time = time.time()
        result = func(*args)
        execution_time = round(time.time() - start_time, 1)
        print(f'Время выполнения функции: {execution_time} с.')
        return result
    return wrapper


def cache_args(func):
    # Здесь код декоратора
    cache = {}
    def wrapper(*args):
        if args not in cache.keys():
            cache[args] = func(*args)
        return cache[args]
    return wrapper


@time_check
@cache_args
def long_heavy(num):
    time.sleep(1)
    return num * 2


print(long_heavy(1))
# Время выполнения функции: 1.0 с.
# 2
print(long_heavy(1))
# Время выполнения функции: 0.0 с.
# 2
print(long_heavy(2))
# Время выполнения функции: 1.0 с.
# 4
print(long_heavy(2))
# Время выполнения функции: 0.0 с.
# 4
print(long_heavy(2))
# Время выполнения функции: 0.0 с.
# 4