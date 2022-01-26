import re

s = 'Интернет 30 503Мбит/с с ТВ'

dig = re.search(r'\d{3,}', s)
if dig: print('dig', dig.group().strip())

tv = re.search(r'ТВ', s)
print('ТВ', tv)

