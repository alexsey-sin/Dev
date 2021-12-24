import json

with open('obl.txt', 'r', encoding='utf-8') as f:
    region = f.read().splitlines()

with open('cit.txt', 'r', encoding='utf-8') as f:
    city = f.read().splitlines()

with open('str.txt', 'r', encoding='utf-8') as f:
    street = f.read().splitlines()

with open('hus.txt', 'r', encoding='utf-8') as f:
    house = f.read().splitlines()

ln = len(region)
if ln != len(city): print('error len city')
if ln != len(street): print('error len street')
if ln != len(house): print('error len house')


out_lst = []
for i in range(ln):
    dkt = {
        'region': region[i],
        'city': city[i],
        'street': street[i],
        'house': house[i]
    }
    out_lst.append(dkt)

with open('fix_address.json', 'w') as f:
    f.write(json.dumps(out_lst))

    