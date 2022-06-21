lst_deal = []
# lst_deal.append({'ID': '157942', 'num': '1100298394828'})
lst_deal.append({'ID': '157942', 'num': '1100298314608'})
lst_deal.append({'ID': '157942', 'num': None})
lst_deal.append({'ID': '157942', 'num': 1254})

for deal in lst_deal:
    num_deal = deal.get('num', 'Не определен')
    if type(num_deal) != str: num_deal = str(num_deal)
    num_deal = num_deal[:50]
    print(num_deal)


