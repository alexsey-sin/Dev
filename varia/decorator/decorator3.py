'''
Напишите декоратор, оптимизирующий работу декорируемой функции.
Декоратор должен сохранять результат работы функции на ближайшие 3 запуска
и вместо выполнения функции возвращать сохранённый результат.
'''

def cache3(func):
    count = {'num': 3, 'rez': 0}
    def wrapper():
        if count['num'] == 3:
            count['rez'] = func()
        count['num'] -= 1
        if count['num'] == 0:
            count['num'] = 3
        return count['rez']
    return wrapper


@cache3
def heavy():
    print('Сложные вычисления')
    return 1


print(heavy())
# Сложные вычисления
# 1
print(heavy())
# 1
print(heavy())
# 1

# Опять кеш устарел, надо вычислять заново
print(heavy())
# Сложные вычисления
# 1
print(heavy())
print(heavy())
print(heavy())
print(heavy())
print(heavy())
print(heavy())
print(heavy())
