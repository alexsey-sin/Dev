from datetime import datetime as dt
import time as t


def timeit(st):
    def owner(func):
        print(st)

        def wrapper(*args, **kwargs):
            start = dt.now()
            result = func(*args, **kwargs)
            # t.sleep(0.1)
            delta = dt.now() - start
            print(delta)
            return result
        return wrapper
    return owner


@timeit('d')
def one(n):
    lst = []
    # t.sleep(0.1)
    for i in range(n):
        if i % 2 == 0:
            lst.append(i)
    return lst


@timeit('dgggg')
def two(n):
    lst = [x for x in range(n) if x % 2 == 0]
    return lst


# print(one(300000))
# print(two(300000))
# print(t.time_ns())
one(300000)
two(300000)
