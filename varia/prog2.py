#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import stdin, stdout

def Check_underscore(s: str) -> bool:
    if s[:2] == '__' and s[-2:] == '__':
        return False
    return True

if __name__ == '__main__':
    pass

    # print((0.25).as_integer_ratio())


    my_list = list(filter(Check_underscore, dir(stdin)))
    row = ' '.join(my_list)

    with open('out_row.txt', 'w') as f:
        f.write(row + "\n")

    # a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    # b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    # print(set(a) & set(b))

    # my_dict = {'a':500, 'b':5874, 'c': 560,'d':400, 'e':5874, 'f': 20}
    # he_dict = sorted(my_dict, key=my_dict.get, reverse=True)[:3]
    # print(he_dict)
# https://pictures.s3.yandex.net/frontend-developer/free-course/mountains.jpg
 # https://unsplash.com/, где работы фотографов свободны к распространению.


    # while(1):
        # my_str = input('enter pthrase: ')
        # if my_str == 'q':
            # break
        # if my_str == my_str[::-1]:
            # print('polinom')
        # else:
            # print('no')







