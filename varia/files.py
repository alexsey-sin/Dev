# Сохраняем в файл словарь gt_catalog отформатированный с отступами
with open('catalog.txt', 'w', encoding='utf-8') as of:
    json.dump(gt_catalog, of, ensure_ascii=False, indent=4)
    
# with open('out.txt', 'w', encoding='utf-8') as outfile:
    # outfile.write(dd)

