# www.hackerrank.com
# alexey-sin@yandex.ru
# 15071971
# =============================================================================
# a, b, c, d = map(int, input().split())
# print(pow(a, b) + pow(c, d))
# =============================================================================
# import numpy as np
# np.set_printoptions(legacy='1.13')

# d = input().split()
# n = int(d[0])
# m = int(d[1])

# lst_n = []
# for i in range(n):
    # r = input().split()
    # lst_n.append(list(map(int, r)))

# arr_n = np.array(lst_n)

# lst_m = []
# for i in range(n):
    # h = input().split()
    # lst_m.append(list(map(int, h)))

# arr_m = np.array(lst_m)

# print(arr_n + arr_m)
# print(arr_n - arr_m)
# print(arr_n * arr_m)
# print(arr_n // arr_m)
# print(arr_n % arr_m)
# print(arr_n ** arr_m)

# =============================================================================
# 1.1 2.2 3.3 4.4 5.5 6.6 7.7 8.8 9.9

# import numpy as np
# np.set_printoptions(legacy='1.13')

# arr = np.array(list(map(float, input().split())))
# print(np.floor(arr))
# print(np.ceil(arr))
# print(np.rint(arr))
# =============================================================================
# Sum and Prod
# import numpy as np
# np.set_printoptions(legacy='1.13')

# n, m = map(int, input().split())
# lst_n = []
# for i in range(n):
    # r = input().split()
    # lst_n.append(list(map(int, r)))
# arr_n = np.array(lst_n)
# arr_m = np.array(np.sum(arr_n, axis = 0))
# print(np.prod(arr_m))
# =============================================================================
# # Min and Max
# import numpy as np
# np.set_printoptions(legacy='1.13')

# n, m = map(int, input().split())
# lst_n = []
# for i in range(n):
    # r = input().split()
    # lst_n.append(list(map(int, r)))
# arr_n = np.array(lst_n)
# arr_m = np.array(np.min(arr_n, axis = 1))
# print(np.max(arr_m))
# =============================================================================
# # Mean, Var, and Std
# import numpy as np

# n, m = map(int, input().split())
# lst_n = []
# for i in range(n):
    # r = input().split()
    # lst_n.append(list(map(int, r)))
# arr_n = np.array(lst_n)
# print(np.mean(arr_n, axis = 1))
# print(np.var(arr_n, axis = 0))
# print(round(np.std(arr_n, axis = None), 11))
# =============================================================================
# Dot and Cross
# import numpy as np

# n = int(input())
# lst_n = []
# for i in range(n):
    # r = input().split()
    # lst_n.append(list(map(int, r)))
# arr_n = np.array(lst_n)
# lst_m = []
# for i in range(n):
    # r = input().split()
    # lst_m.append(list(map(int, r)))
# arr_m = np.array(lst_m)

# print(np.dot(arr_n, arr_m))
# =============================================================================
# Inner and Outer
# import numpy as np
# arr_n = np.array(list(map(int, input().split())))
# arr_m = np.array(list(map(int, input().split())))

# print(np.inner(arr_n, arr_m))
# print(np.outer(arr_n, arr_m))
# =============================================================================
# # Polynomials
# import numpy as np

# lst_n = list(map(float, input().split()))
# x = int(input())
# print(np.polyval(lst_n, x))
# =============================================================================
# # Linear Algebra
# import numpy as np

# n = int(input())
# lst_n = []
# for i in range(n):
    # r = input().split()
    # lst_n.append(list(map(float, r)))
# arr_n = np.array(lst_n)

# print(round(np.linalg.det(arr_n), 2))
# =============================================================================
# DefaultDict Tutorial
# from collections import defaultdict

# Это моё решение. Но оно часть тестов не проходит
# возможно что код для больших данных требует много ресурсов
# Я сохранял весь входной поток а потом обрабатывал
# n, m = map(int, input().split())
# lst_n = []
# for i in range(n):
    # lst_n.append(input())

# d = defaultdict(list)
# for i in range(m):
    # d[input()].append(-1)

# for k, v in d.items():
    # if k in lst_n:
        # v.clear()
        # for i in range(len(lst_n)):
            # if k == lst_n[i]:
                # v.append(i+1)

# for v in d.values():
    # lst_i = list(map(str, v))
    # print(' '.join(lst_i))

# нашел такое решение: очень удачное.
# чел сохранял в словарь сразу индексы
# а потом выводил
# from collections import defaultdict
# d = defaultdict(list)

# n, m = map(int, input().split())

# for i in range(n):
    # d[input()].append(str(i+1))
    
# for i in range(m):
    # print (' '.join(d[input()]) or -1)
# =============================================================================
# collections.namedtuple()
# from collections import namedtuple
# в итоге решить задачу оказалось проще просто через списки

# marks, n, i = 0, int(input()), input().split().index('MARKS')
# for t in range(n):
    # marks += int(input().split()[i])
# print(round(marks/n, 2))
# =============================================================================
# Collections.OrderedDict()
# from collections import OrderedDict

# od = OrderedDict()
# n = int(input())
# for t in range(n):
    # k, v = input().rsplit(maxsplit=1)
    # p = int(v)
    # if k in od:
        # od[k] = od[k] + p
    # else:
        # od[k] = p

# for k, v in od.items():
    # print(k, v)

# У вас есть список N товаров с указанием их цен, которые потребители купили в определенный день.
# Ваша задача - распечатать каждое item_name и net_price в порядке их первого появления.
# item_name = Название предмета 
# net_price = Количество проданного товара, умноженное на цену каждого товара. 

# =============================================================================
# Collections.deque()
# from collections import deque

# d = deque()
# n = int(input())
# for t in range(n):
    # c = input().split()
    # if len(c) == 2:
        # a = c[1]
    # else:
        # a = ''
    # com = 'd.{}({})'.format(c[0], a)
    # exec(com)
# print(' '.join(list(map(str, list(d)))))
# =============================================================================
# List Comprehensions

# x = int(input())
# y = int(input())
# z = int(input())
# n = int(input())

# i = j = k = 0
# lst = []
# while 1:
    # ls = [i, j, k]
    # if sum(ls) != n:
        # lst.append(ls)
    # k += 1
    # if k > z:
        # k = 0
        # j += 1
    # if j > y:
        # j = 0
        # i += 1
    # if i > x:
        # break
    
# print(lst)    
# =============================================================================
# Find the Runner-Up Score!
# n = int(input())
# arr = list(map(int, input().split()))
# arr.sort(reverse=True)
# for a in arr:
    # if a < arr[0]:
        # print(a)
        # break
# =============================================================================
# Nested Lists
# n = int(input())
# arr = []
# for i in range(n):
    # k = input()
    # v = float(input())
    # arr.append([k, v])

# arr.sort(key=lambda i: i[1])
# sec = 0.0
# for a in arr:
    # if a[1] > arr[0][1]:
        # sec = a[1]
        # break
# arr2 = []
# for a in arr:
    # if a[1] == sec:
        # arr2.append(a[0])

# arr2.sort()
# print('\n'.join(arr2))
# =============================================================================
# Finding the percentage
# if __name__ == '__main__':
    # n = int(input())
    # student_marks = {}
    # for _ in range(n):
        # name, *line = input().split()
        # scores = list(map(float, line))
        # student_marks[name] = scores
    # query_name = input()
    
    # lst = student_marks[query_name]
    # ss = sum(lst) / len(lst)
    # print('{:.2f}'.format(ss))
# =============================================================================
# Calendar Module
# import calendar
# arr = list(map(int, input().split()))
# d = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
# print(d[calendar.weekday(arr[2], arr[0], arr[1])])
# =============================================================================
# Designer Door Mat
# 9 27

# n, m = map(int, input().split())
# c = n // 2
# b = '.|.'
# for i in range(c):
    # s = b * i * 2 + b
    # print(s.center(m, '-'))
# print('WELCOME'.center(m, '-'))
# for i in reversed(range(c)):
    # s = b * i * 2 + b
    # print(s.center(m, '-'))
# # А вот более элегантное решение
# n, m = map(int,input().split())
# pattern = [('.|.'*(2*i + 1)).center(m, '-') for i in range(n//2)]
# print('\n'.join(pattern + ['WELCOME'.center(m, '-')] + pattern[::-1]))
# =============================================================================
# String Formatting

# n = int(input())
# l = len('{0:b}'.format(n))
# rep = ('{:d}', '{:o}', '{:X}', '{:b}')
# for i in range(1, n+1):
    # print(' '.join(s.format(i).rjust(l) for s in rep))
# =============================================================================
# Alphabet Rangoli
# def print_rangoli(size):
    # ab = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        # 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
    # m = (2 * size - 1) * 2 - 1
    # pattern = ['-'.join(ab[size-1:i:-1] + ab[i:size]).center(m, '-') for i in range(size)]
    # print('\n'.join(pattern[-1:0:-1] + pattern))

# if __name__ == '__main__':
    # n = int(input())
    # print_rangoli(n)
# =============================================================================
# Capitalize
# import re

# def solve(s):
    # for x in s.split():
        # s = s.replace(x, x.capitalize())
    # return(s)

# if __name__ == '__main__':
    # n = input()
    # print(solve(n))
# =============================================================================
# Lists
# if __name__ == '__main__':
    # N = int(input())
    # base_list = []
    # for _ in range(N):
        # lst = input().split()
        # if len(lst) == 1:
            # sub = ''
            # if lst[0] == 'print':
                # com = 'print(base_list)'
            # else:
                # com = 'base_list.{}()'.format(lst[0])
        # else:
            # com = 'base_list.{}({})'.format(lst[0], ', '.join(lst[1:]))
        # exec(com)
# =============================================================================
# Tuples
# if __name__ == '__main__':
    # n = int(input())
    # integer_list = map(int, input().split())
    # t = tuple(integer_list)
    # print(hash(t))
# =============================================================================
# sWAP cASE
# def swap_case(s):
    # return(s.swapcase())

# if __name__ == '__main__':
    # s = input()
    # result = swap_case(s)
    # print(result)
# =============================================================================
# String Split and Join
# def split_and_join(line):
    # return('-'.join(line.split()))

# if __name__ == '__main__':
    # line = input()
    # result = split_and_join(line)
    # print(result)
# =============================================================================
# What's Your Name?
# def print_full_name(a, b):
    # print("Hello {} {}! You just delved into python.".format(a, b))

# if __name__ == '__main__':
    # first_name = input()
    # last_name = input()
    # print_full_name(first_name, last_name)
# =============================================================================
# Mutations
# def mutate_string(string, position, character):
    # lst = list(string)
    # lst[position] = character
    # return(''.join(lst))


# if __name__ == '__main__':
    # s = input()
    # i, c = input().split()
    # s_new = mutate_string(s, int(i), c)
    # print(s_new)
# =============================================================================
# Find a string
# def count_substring(string, sub_string):
    # cnt = 0
    # i = 0
    # while i != -1:
        # i = string.find(sub_string, i)
        # if i != -1:
            # cnt += 1
            # i += 1
    # return(cnt)

# if __name__ == '__main__':
    # string = input().strip()
    # sub_string = input().strip()
    
    # count = count_substring(string, sub_string)
    # print(count)
# =============================================================================
# String Validators
# if __name__ == '__main__':
    # isaln = isalp = isdig = islow = isupp = False
    # s = input()
    # for ch in s:
        # if ch.isalnum():
            # isaln = True
        # if ch.isalpha():
            # isalp = True
        # if ch.isdigit():
            # isdig = True
        # if ch.islower():
            # islow = True
        # if ch.isupper():
            # isupp = True
    # print(isaln)
    # print(isalp)
    # print(isdig)
    # print(islow)
    # print(isupp)

# =============================================================================
# Text Alignment
#Replace all ______ with rjust, ljust or center. 

# thickness = int(input()) #This must be an odd number
# c = 'H'

# #Top Cone
# for i in range(thickness):
    # print((c*i).rjust(thickness-1)+c+(c*i).ljust(thickness-1))

# #Top Pillars
# for i in range(thickness+1):
    # print((c*thickness).center(thickness*2)+(c*thickness).center(thickness*6))

# #Middle Belt
# for i in range((thickness+1)//2):
    # print((c*thickness*5).center(thickness*6))    

# #Bottom Pillars
# for i in range(thickness+1):
    # print((c*thickness).center(thickness*2)+(c*thickness).center(thickness*6))    

# #Bottom Cone
# for i in range(thickness):
    # print(((c*(thickness-i-1)).rjust(thickness)+c+(c*(thickness-i-1)).ljust(thickness)).rjust(thickness*6))
# =============================================================================
# Text Wrap
# import textwrap

# def wrap(string, max_width):
    # return(textwrap.fill(string, width=max_width))

# if __name__ == '__main__':
    # string, max_width = input(), int(input())
    # result = wrap(string, max_width)
    # print(result)
# =============================================================================
# itertools.product() генерирует декартовое произведение
# from itertools import product

# a = list(map(int,input().split()))
# b = list(map(int,input().split()))
# d = map(str,product(a, b))
# print(' '.join(list(d)))
# =============================================================================
# itertools.permutations() генерирует все возможные перестановки элементов списка
# from itertools import permutations
# s, k = input().split()
# lst = sorted(list(map(''.join, permutations(s, int(k)))))
# print('\n'.join(lst))
# =============================================================================
# itertools.combinations() генерирует подпоследовательности элементов из итерируемого входа
# from itertools import combinations
# s, k = input().split()
# s = sorted(s)
# lst = []
# for v in range(1, int(k) + 1):
    # lst.extend(sorted(list(map(''.join, combinations(s, v)))))
# print('\n'.join(lst))
# =============================================================================
# itertools.combinations_with_replacement()
# from itertools import combinations_with_replacement
# s, k = input().split()
# s = sorted(s)
# lst = sorted(list(map(''.join, combinations_with_replacement(s, int(k)))))
# print('\n'.join(lst))
# =============================================================================
# collections.Counter()
# from collections import Counter

# k = input()
# sizes = list(map(int, input().split()))
# con_sizes = Counter(sizes)
# c = int(input())
# sum = 0
# for _ in range(c):
    # s, p = map(int,input().split())
    # if s in con_sizes:
        # con_sizes[s] -= 1
        # sum += p
        # if con_sizes[s] == 0:
            # con_sizes.pop(s)
# print(sum)
# =============================================================================
# Polar Coordinates
# from cmath import phase
# cx = input()
# print(round(abs(complex(cx)), 3))
# print(round(phase(complex(cx)), 3))
# =============================================================================
# Introduction to Sets
# def average(array):
    # s = set(array)
    # return(sum(s)/len(s))

# if __name__ == '__main__':
    # # n = int(input())
    # arr = list(map(int, input().split()))
    # result = average(arr)
    # print(result)
# =============================================================================
# Symmetric Difference
# _ = input()
# s1 = set(map(int, input().split()))
# _ = input()
# s2 = set(map(int, input().split()))
# s3 = sorted(list(s1.symmetric_difference(s2)))
# lst = map(str, s3)
# print('\n'.join(lst))
# =============================================================================
# Exceptions

# n = int(input())
# for _ in range(n):
    # try:
        # a, b = map(int,input().split())
        # print(int(a/b))
    # except ZeroDivisionError as e:
        # print('Error Code: integer division or modulo by zero')
    # except ValueError as e:
        # print('Error Code:', e)
# =============================================================================
# Incorrect Regex
# import re
# for d in range(int(input())):
    # res = True
    # try:
        # reg = re.compile(input())
    # except re.error:
        # res = False
    # print(res)
# =============================================================================
# Set .add()
# d = set()
# for _ in range(int(input())):
    # d.add(input())
# print(len(d))
# =============================================================================
# Set .discard(), .remove() & .pop()

# _ = int(input())
# s = set(map(int, input().split()))
# n = int(input())

# for _ in range(n):
    # c = input().split()
    # if len(c) == 2:
        # a = int(c[1])
    # else:
        # a = ''
    # com = 's.{}({})'.format(c[0], a)
    # exec(com)
# print(sum(s))
# =============================================================================
# Set .union() Operation
# _ = input()
# sa = set(map(int, input().split()))
# _ = input()
# sb = set(map(int, input().split()))
# sc = sa | sb
# print(len(sc))
# =============================================================================
# Set .intersection() Operation
# _ = input()
# sa = set(map(int, input().split()))
# _ = input()
# sb = set(map(int, input().split()))
# sc = sa & sb
# print(len(sc))
# =============================================================================
# Set .difference() Operation
# _ = input()
# sa = set(map(int, input().split()))
# _ = input()
# sb = set(map(int, input().split()))
# sc = sa & sb
# print(len(sc))
# =============================================================================
# Set .symmetric_difference() Operation
# _ = input()
# sa = set(map(int, input().split()))
# _ = input()
# sb = set(map(int, input().split()))
# sc = sa ^ sb
# print(len(sc))
# =============================================================================
# Set Mutations
# _ = input()
# sa = set(map(int, input().split()))
# n = int(input())
# for _ in range(n):
    # c = input().split()
    # sb = set(map(int, input().split()))

    # com = 'sa.{}(sb)'.format(c[0])
    # exec(com)
# print(sum(sa))
# =============================================================================
# The Captain's Room
# k = int(input())
# lst = list(map(int, input().split()))
# s = set(lst)
# t = ((sum(s)*k)-(sum(lst)))//(k-1)
# print(t)
# =============================================================================
# Check Subset
# k = int(input())
# for t in range(k):
    # _ = int(input())
    # sa = set(map(int, input().split()))
    # _ = int(input())
    # sb = set(map(int, input().split()))
    # print(sa <= sb)
# =============================================================================
# Check Strict Superset
# rez = True
# sa = set(map(int, input().split()))
# k = int(input())
# for _ in range(k):
    # sb = set(map(int, input().split()))
    # if sa.issuperset(sb) == False:
        # rez = False
# print(rez)
# =============================================================================
# Decorators 2 - Name Directory
# Давайте воспользуемся декораторами для создания каталога имен!
# Вам дана некоторая информация о людях C. У каждого человека есть имя, фамилия,
# возраст и пол. Выведите их имена в определенном формате, отсортированные
# по возрасту в возрастающем порядке, то есть имя самого молодого человека
# должно быть напечатано первым. Для двух людей одного возраста распечатайте
# их в порядке ввода.

# проходит не все тесты. 3 из 13 завалены
# import operator

# def person_lister(f):
    # def inner(people):
        # return map(f, sorted(people, key=operator.itemgetter(2)))
    # return inner

# @person_lister
# def name_format(person):
    # return ("Mr. " if person[3] == "M" else "Ms. ") + person[0] + " " + person[1]

# if __name__ == '__main__':
    # people = [input().split() for i in range(int(input()))]
    # print(*name_format(people), sep='\n')
# ===========================================================================
# Class 2 - Find the Torsional Angle
'''
Даны 4 точки A, B, C и D в трехмерной системе координат.
Вычислите угол образованный плоскостями, образованные точками
A, B, C и  B, C, D в градусах. Пусть угол будет PHI.
Cos(PHI) = (X.Y)/|X||Y| где X = AB * BC и Y = BC * CD
Где X.Y означает скалярное произведение X и Y, 
а AB * BC - перекрестное произведение векторов.
Также AB = B - A.
Входные данные: четыре строки, каждая содержит пробелами разделенные
значения X,Y,Z с плавающей запятой точек A, B, C и D
0 4 5
1 7 6
0 5 9
1 7 2

Выходной формат:
Выведите правильный угол с точностью до двух десятичных знаков.
8.19
'''
'''
# Вариант вполне рабочий но по условию требуется класс
import numpy as np

A = np.array(list(map(float, input().split())))
B = np.array(list(map(float, input().split())))
C = np.array(list(map(float, input().split())))
D = np.array(list(map(float, input().split())))

AB = B - A
BC = C - B
CD = D - C
X = np.cross(AB, BC)
Y = np.cross(BC, CD)
up = np.dot(X, Y)
down = np.linalg.norm(X) * np.linalg.norm(Y)
ang = np.degrees(np.arccos(up / down))
print('{:0.2f}'.format(ang))
'''
# import math

# class Points(object):
    # def __init__(self, x, y, z):
        # self.x = x
        # self.y = y
        # self.z = z

    # def __sub__(self, no):
        # x = self.x - no.x
        # y = self.y - no.y
        # z = self.z - no.z
        # return Points(x, y, z)

    # def dot(self, no):
        # return self.x * no.x + self.y * no.y + self.z * no.z

    # def cross(self, no):
        # x = self.y * no.z - self.z * no.y
        # y = self.z * no.x - self.x * no.z
        # z = self.x * no.y - self.y * no.x
        # return Points(x, y, z)
        
    # def absolute(self):
        # return pow((self.x ** 2 + self.y ** 2 + self.z ** 2), 0.5)

# if __name__ == '__main__':
    # points = list()
    # for i in range(4):
        # a = list(map(float, input().split()))
        # points.append(a)

    # a, b, c, d = Points(*points[0]), Points(*points[1]), Points(*points[2]), Points(*points[3])
    # x = (b - a).cross(c - b)
    # y = (c - b).cross(d - c)
    # angle = math.acos(x.dot(y) / (x.absolute() * y.absolute()))

    # print("%.2f" % math.degrees(angle))
# ===========================================================================
# HTML Parser - Part 1
# from html.parser import HTMLParser

# class MyHTMLParser(HTMLParser):
    # def handle_starttag(self, tag, attrs):
        # print('Start :', tag)
        # for attr in attrs:
            # print('->', attr[0], '>', attr[1])
    # def handle_endtag(self, tag):
        # print('End   :', tag)
    # def handle_startendtag(self, tag, attrs):
        # print('Empty :', tag)
        # for attr in attrs:
            # print('->', attr[0], '>', attr[1])

# buf = ''
# n = int(input())
# while n:
    # buf += input()
    # n -= 1

# parser = MyHTMLParser()
# parser.feed(buf)
# parser.close()
# ===========================================================================
# HTML Parser - Part 2
# from html.parser import HTMLParser

# class MyHTMLParser(HTMLParser):
    # def handle_comment(self, data):
        # if '\n' in data:
            # print('>>> Multi-line Comment')
            # print(data.strip())
        # else:
            # print('>>> Single-line Comment')
            # print(data.strip())
    # def handle_data(self, data):
        # if data.strip() != '':
            # print('>>> Data')
            # print(data)
  
# html = ''       
# for i in range(int(input())):
    # html += input().rstrip()
    # html += '\n'
    
# parser = MyHTMLParser()
# parser.feed(html)
# parser.close()
# ===========================================================================
# Detect HTML Tags, Attributes and Attribute Values
# from html.parser import HTMLParser

# class MyHTMLParser(HTMLParser):
    # def handle_starttag(self, tag, attrs):
        # print(tag)
        # for attr in attrs:
            # print('->', attr[0], '>', attr[1])

# buf = ''
# n = int(input())
# while n:
    # buf += input()
    # n -= 1

# parser = MyHTMLParser()
# parser.feed(buf)
# parser.close()
# ===========================================================================
# Validating UID
'''
Компания ABCXYZ имеет до 100 сотрудников.
Компания решает создать уникальный идентификационный номер (UID) для каждого из своих сотрудников.
Компания поручила вам проверить все случайно сгенерированные UID.
Действительный UID должен соответствовать следующим правилам: 

Он должен содержать не менее 2 заглавных букв английского алфавита.
Он должен содержать не менее 3 цифр (0-9).
Он должен содержать только буквенно-цифровые символы (a-z, A-Z & 0-9).
Ни один символ не должен повторяться.
Должно быть точно 10 символов в допустимом UID. 
'''
# string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
# string.ascii_letters  # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
# string.digits  # 0123456789

# import string
# def is_valid(uid) -> bool:
    # check = True
    # if len(uid) != 10:
        # check = False
    # if len(tuple(uid)) != len(set(uid)):
        # check = False
    
    # upp = 0
    # num = 0
    # for ch in uid:
        # if ch in string.ascii_uppercase:
            # upp += 1
        # elif ch in string.digits:
            # num += 1
        # else:
            # if ch not in string.ascii_lowercase:
                # return False

    # if upp < 2:
        # check = False
    # if num < 3:
        # check = False
    # return check

# n = int(input())
# while n:
    # if is_valid(input().strip()):
        # print('Valid')
    # else:
        # print('Invalid')
    
    # n -= 1
# ===========================================================================
# Zipped!
# Моё решение
# s, n = map(int, input().split())
# lst = [0 for _ in range(s)]
# for i in range(n):
    # d = list(map(float, input().split()))
    # for j in range(s):
        # lst[j] += d[j]

# for i in range(s):
    # av = lst[i] / n
    # print('{:.1f}'.format(av))

# Вот лучшее решение через zip
# n, x = map(int, input().split()) 

# sheet = []
# for _ in range(x):
    # sheet.append(map(float, input().split())) 

# for i in zip(*sheet): 
    # print('{:.1f}'.format(sum(i)/len(i)))
# ===========================================================================
# Input()
# x, k = input().split()
# ex = 'int(k) == ' + input().replace('x', x)
# print(eval(ex))
# ===========================================================================
# Python Evaluation
# eval(input())
# ===========================================================================
# Any or All
# _, sequence = input(), input().split()
# print(all(list(map(lambda x: int(x) > 0, sequence))) and any(list(map(lambda x: x == x[::-1], sequence))))
# ===========================================================================
# Detect Floating Point Number
# n = int(input())
# for _ in range(n):
    # s = input()
    # if len(s) < 2 and '.' not in s:
        # print('False')
        # continue
    # try:
        # f = float(s)
    # except:
        # print('False')
        # continue
    # print('True')    
# лучшее решение
# import re
# for _ in range(int(input())):
	# print(bool(re.match(r'^[-+]?[0-9]*\.[0-9]+$', input())))
# ===========================================================================
# Re.split()
# regex_pattern = r"[\.\,]"	# Do not delete 'r'.

# import re
# print("\n".join(re.split(regex_pattern, input())))
# ===========================================================================
# Group(), Groups() & Groupdict()
# import re
# m = re.search(r"([0-9A-Za-z]{1,1})\1+", input())
# print(m.group(1) if m else -1)
# ===========================================================================
# Re.findall() & Re.finditer()
# не все тесты проходит
# import re
# v = 'aeiou'
# c = 'qwrtypsdfghjklzxcvbnm'
# m = re.findall(r'[' + c + ']([' + v + ']{2,})[' + c + ']', input(), re.I)
# print('\n'.join(g for g in m) if m else -1)

# лучшее решение
# import re
# v = 'aeiou'
# c = 'qwrtypsdfghjklzxcvbnm'
# m = re.findall(r'(?<=[%s])([%s]{2,})[%s]' %(c, v, c), input(), re.I)
# print('\n'.join(g for g in m) if m else -1)
# ===========================================================================
# Re.start() & Re.end()
# import re
# s = input()
# pattern = re.compile(input())
# r = pattern.search(s)
# if not r: print('(-1, -1)')
# while r:
    # print('({0}, {1})'.format(r.start(), r.end() - 1))
    # r = pattern.search(s,r.start() + 1)
# ===========================================================================
# Map and Lambda Function
# n = int(input())
# cube = lambda x: x**3
# def fibonacci(n):
    # lst = []
    # for i in range(n):
        # if i == 0: t = 0
        # elif i == 1: t = 1
        # else:
            # t = lst[i - 1] + lst[i - 2]
        # lst.append(t)
    # return lst
# print(list(map(cube, fibonacci(n))))

# формулы фибоначчи на всякий случай
# M = {0: 0, 1: 1}
# def fib(n):
    # if n in M:
        # return M[n]
    # M[n] = fib(n - 1) + fib(n - 2)
    # return M[n]

# def fib(n):
    # a = 0
    # b = 1
    # for __ in range(n):
        # a, b = b, a + b
    # return a

# fib = lambda i: fib[i - 1] + fib[i - 2] if i > 2 else 1
# ===========================================================================
# Validating Roman Numerals
# римские цифры
# I (1), V (5), X (10), L (50), C (100), D (500), M (1000)
# regex_pattern = r"M{0,3}(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[VX]|V?I{0,3})$"	# Do not delete 'r'.

# import re
# print(str(bool(re.match(regex_pattern, raw_input()))))
# ===========================================================================
# Validating phone numbers
# import re
# pattern = r'^[789]\d{9}$'
# for _ in range(int(input())):
    # in_str = input()
    # print('YES' if re.search(pattern, in_str) else 'NO')
# ===========================================================================
# Validating and Parsing Email Addresses
# import email.utils
# import re

# pattern = r'^[a-z][0-9a-z-_\.]{1,}@[a-z]+\.[a-z]{1,3}$'

# for _ in range(int(input())):
    # par_addr = email.utils.parseaddr(input())
    # if re.search(pattern, par_addr[1]):
        # print(email.utils.formataddr(par_addr))
# ===========================================================================
# Hex Color Code
# import re

# pattern = r'((#[0-9a-f]{3}[^0-9a-f])|(#[0-9a-f]{6}[^0-9a-f]))+'
# block = False

# for _ in range(int(input())):
    # try: in_str = input()
    # except: continue
    # if '}' in in_str:
        # block = False
        # continue
    # if '{' in in_str:
        # block = True
        # continue
    # if block:
        # m = re.findall(pattern, in_str, re.I)
        # if m:
            # print('\n'.join(g[0][:-1] for g in m))

# лучший вариант
# import re
# pattern = r'(?<!^)(#(?:[\da-f]{3}){1,2})'
    #
# for _ in range(int(input())):
    # in_str = input()
    # m = re.findall(pattern, in_str, re.I)
    # if m:
        # print('\n'.join(g for g in m))

# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================


















