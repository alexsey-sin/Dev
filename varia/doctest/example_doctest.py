"""
Принимает список неотрицательных целых чисел и строк
и возвращает новый список с отфильтрованными строками.

Например:
>>> filter_list([1, 2, 'a', 'b'])
[1, 2]
>>> filter_list([1, 'a', 'b', 0, 15])
[1, 0, 15]
>>> filter_list([1, 2, 'aasf', '1', '123', 123])
[1, 2, 123]
"""

def filter_list(in_list):
	out_list = []
	for var_str in in_list:
		if (type(var_str) == int or type(var_str) == float) and var_str not in out_list: out_list.append(var_str)
	return out_list

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    