# import this
# print('Hello world')


def validate_anagram(word1: str, word2: str) -> bool:
    result = True
    for char in word1:
        if char not in word2:
            result = False
    return result


def fizzbuzz(in_list: list) -> list:
    for i in range(len(in_list)):
        if in_list[i] % 3 == 0 and in_list[i] % 5 == 0:
            in_list[i] = 'Fizz'
        elif in_list[i] % 5 == 0:
            in_list[i] = 'Buzz'
        elif in_list[i] % 3 == 0:
            in_list[i] = 'FizzBuzz'
    return in_list


def check_brackets(my_str) -> bool:
    start = ['[', '{', '(']
    stop = [']', '}', ')']
    stack = []

    for i in my_str:
        if i in start:
            stack.append(i)
        elif i in stop:
            pos = stop.index(i)
            pair = start[pos]
            if len(stack) == 0 or pair not in stack or stack[-1] != pair:
                return False
            stack.pop()

    if len(stack) == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    # print(validate_anagram('abs', 'bas'))
    # print(validate_anagram('foo', 'bar'))

    # list_num = [x for x in range(1, 101)]
    # print(fizzbuzz(list_num))

    # print(check_brackets('(1+1)[2-2]'))
    # print(check_brackets('{(2 * (3+2) - [(23+4)]}'))
    # print(check_brackets('(1-1 [23 + 89)]'))
    # print(check_brackets(')13-34 + [4-5] {23*2})'))
    # print(check_brackets('(a [ foo, bar: buzz qux] {} )()'))
    pass



    # for i in range(1,int(input())):
        # print(i + sum((10**c * i) for c in range(1, i)))
        # print(i + sum((pow(10,c) * i) for c in range(1, i)))
        # print(i + sum(list(map(lambda c: pow(10,c)*i, range(1, i)))))
    import numpy as np
    np.set_printoptions(legacy='1.13')
    
    d = input().split()
    n = int(d[0])
    m = int(d[1])
    
    lst_n = []
    for i in range(n):
        d = input().split()
        lst_n.append(list(map(lambda x: int(x), d)))
    
    arr_n = np.array(lst_n)
 
    lst_m = []
    for i in range(m):
        d = input().split()
        lst_m.append(list(map(lambda x: int(x), d)))
    
    arr_m = np.array(lst_m)

    print(arr_n + arr_m)
    print(arr_n - arr_m)
    print(arr_n * arr_m)
    print(arr_n // arr_m)
    print(arr_n % arr_m)
    print(arr_n ** arr_m)


    
# 3   3

# 5 4 2 
# 8 2 4
# 6 7 1

# 5 7 3
# 5 9 6
# 2 2 1


