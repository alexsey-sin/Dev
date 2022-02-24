import re

# s = 'Интернет 30 503Мбит/с с ТВ'

# dig = re.search(r'\d{3,}', s)
# if dig: print('dig', dig.group().strip())

# tv = re.search(r'ТВ', s)
# print('ТВ', tv)

# Убираем ненужные слова
exclude_frase = [
    'имени',
]
street = 'имени 40-летия Победы имени'
for es in exclude_frase:
    # reg_exp = fr"'{re.escape(es)}\s'"
    # e = street.replace(reg_exp, '')
    street = street.replace(es, '').strip()


print(street)
# print(e)




