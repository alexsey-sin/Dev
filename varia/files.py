import json

# Сохраняем в файл словарь gt_catalog отформатированный с отступами
with open('catalog.txt', 'w', encoding='utf-8') as out_file:
    json.dump(gt_catalog, out_file, ensure_ascii=False, indent=4)
    


# with open('out.txt', 'w', encoding='utf-8') as outfile:
    # outfile.write(dd)

# Чтение из файла с преобразованием в json
with open('time_token.json', 'r', encoding='utf-8') as file:
    js = json.load(file)
dt_old_str = js.get('time_create')




print(json.dumps(lst_deal, sort_keys=True, indent=2, ensure_ascii=False))



