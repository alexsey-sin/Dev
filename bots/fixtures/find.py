import json

def check_equality_citys(lst: list, in_str: str):  # Поиск вхождения фразы в списке фраз
    '''
        Поиск вхождения фразы в списке фраз
        Поиск ведется последовательно начиная с первой буквы in_str
        - назовем её подстрока. Если таких вхождений в списке много,
        2 и более добавляем следующую букву к подстроке.
        Поиск завершен если вхождений только одно.
        Возвращаем индекс фразы в списке и саму фразу.
        Если нет вхождений - возвращаем "-1"
    '''
    # Преобразуем входные данные к нижнему регистру
    in_str = in_str.lower().replace('ё', 'е')
    in_lst = [s.lower().replace('ё', 'е') for s in lst]
    
    ret_ind = -1
    ret_phrase = ''
    # поиск с циклом по набиранию подстроки
    for i_s in range(len(in_str)):
        sub_str = in_str[0:i_s+1]
        cnt_phr = 0
        # просмотрим список на вхождение
        for i_lst in range(len(in_lst)):
            if in_lst[i_lst].find(sub_str) >= 0:
                cnt_phr += 1
                ret_ind = i_lst
        if cnt_phr > 1:
            ret_ind = -1
        else:
            break
    if ret_ind >= 0: return [ret_ind,]  # похожая фраза найдена и она в единственной строке
    
    # просмотрим список на полное совпадение
    ret_ind = -1
    cnt_phr = 0
    for i_lst in range(len(in_lst)):
        if in_lst[i_lst] == in_str:
            cnt_phr += 1
            ret_ind = i_lst
    if cnt_phr == 1: return [ret_ind,]

    # просмотрим список на полное совпадение как самостоятельного слова
    # ret_ind = -1
    # cnt_phr = 0
    ln_sb = len(in_str)
    rez_lst = []
    for i_lst in range(len(in_lst)):
        ln_str = len(in_lst[i_lst])
        i = in_lst[i_lst].find(in_str)
        if i >= 0:
            if in_str == 'омск':
                rez_lst.append(i_lst)
                break
            # фраза найдена
            # проверим букву перед фразой
            if i > 0:
                if in_lst[i_lst][i - 1].isalpha():  #не повезло - буква
                    continue
            # проверим букву после фразы
            if i + ln_sb < ln_str:
                if in_lst[i_lst][i + ln_sb].isalpha():  #не повезло - буква
                    continue
            if i + ln_sb == ln_str and in_str == 'кострома':
                rez_lst.append(i_lst)
                break
            rez_lst.append(i_lst)
            
        
    return rez_lst


def ordering_street(in_street: str):  # Преобразование строки улица
    '''
        разбиваем строку по запятым, и каждый фрагмент проверяем на
        изветсный тип улицы
        выдаем список [тип_улицы, название]
        если известный тип не найден - возвращаем пустой список
    '''
    lst_type_street = [
        'улица',
        'проспект',
        'переулок',
        'бульвар',
        'шоссе',
        'аллея',
        'тупик',
        'проезд',
        'набережная',
        'площадь',
    ]
    out_cort = []
    lst = in_street.split(',')
    for sub in lst:
        rez = False
        for ts in lst_type_street:
            if sub.find(ts) >= 0:
                rez = True
                out_cort.append(ts)
                out_cort.append(sub.replace(ts, '').strip())
                break
        if rez: break
    return out_cort





with open('fix_address.json', 'r', encoding='utf-8') as f:
    dkt_address = json.load(f)
# with open('beeline_nas_punkt.json', 'r', encoding='utf-8') as f:
    # lst_nas_punkt = json.load(f)




for adr in dkt_address:
    street = adr['street']
    ll = ordering_street(street)
    if ll: print(ll[0], ll[1])
    # print(street)

# for nas in lst_nas_punkt:
    # print(nas)

# for adr in dkt_address:
    # print(adr['region'], adr['city'])

# rez_ok = 0
# rez_fail = 0
# rez_empty = 0
# # проход по каждому адресу
# # cnt = 100
# for adr in dkt_address:
    # city = adr['city']
    # region = adr['region']
    # # просматриваем список на постепенное вхождение названия города
    # lst_cheq = check_equality_citys(lst_nas_punkt, city)
    # if len(lst_cheq) == 0:
        # rez_empty += 1
    # elif len(lst_cheq) == 1:
        # rez_ok += 1
    # else:
        # # print(city)
        # rez_fail += 1
    
    # if city == 'Кострома':
        # print(lst_cheq)
    # # i_cheq = check_equality_citys(lst_nas_punkt, city)
    # # if i_cheq >= 0:
        # # 
    # # else:
        # # # # просмотрим на точное совпадение
        # # # i_cheq = check_equality_citys(lst_nas_punkt, city)
        # # # if i_cheq >= 0:
            # # # rez_ok += 1
        # # # else:
        # # rez_fail += 1
        # # print(city)
    # # cnt -= 1
    # # if cnt == 0: break
# print('rez_ok: ', rez_ok, '   rez_empty: ', rez_empty, '   rez_fail: ', rez_fail)

