import json

with open('fix_address.json', 'r', encoding='utf-8') as f:
    dkt = json.load(f)


for row in dkt:
    print(row)