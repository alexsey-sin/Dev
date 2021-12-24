'''
Цель этого упражнения - преобразовать строку в новую строку,
где каждый символ в новой строке равен "(", если этот символ появляется только один раз в исходной строке,
или ")", если этот символ встречается более одного раза в исходной строке строка.
Игнорируйте использование заглавных букв при определении того, является ли символ дубликатом.
В сообщениях с утверждениями может быть неясно, что они отображают на некоторых языках.
Если вы читаете «... Он должен кодировать XXX», «XXX» - это ожидаемый результат, а не ввод! 

Например:
>>> duplicate_encode("din")
'((('
>>> duplicate_encode("recede")
'()()()'
>>> duplicate_encode("Success")
')())())'
>>> duplicate_encode("(( @")
'))(('
'''
def duplicate_encode(word):
    word = word.lower()
    out = ''
    for ch in word:
        if word.count(ch) == 1:
            out += '('
        else:
            out += ')'
    return out

if __name__ == "__main__":
    import doctest
    doctest.testmod()

# def duplicate_encode(word):
    # return "".join(["(" if word.lower().count(c) == 1 else ")" for c in word.lower()])
