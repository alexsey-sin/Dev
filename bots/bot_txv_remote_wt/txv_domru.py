import os, time, json, requests  # pip install requests
from datetime import datetime
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'
opsos = 'ДомРу'
pv_code = 2

def find_string_to_substrs(lst: list, substr: str):  # Поиск вхождения подстрок в списке фраз с названиями тарифов, адресов
    '''
        Поиск вхождения подстрок в списке фраз
        Поиск ведется без учера регистра (все приводится к нижнему регистру)
        и проверяется является ли слово самостоятельным.
        Т.е. если подстрока входит в слово частично - поиск неудачен
        На входе список строк lst.
        И строка substr содержащая группу подстрок разделенных ;
        либо просто одна подстрока без разделителей
        Если в списке найдены строки в которых присутствуют
        все подстроки из substr то собирается список кортежей с индексами и фразами
        Если спиок из более 1 значения то перебираем его и выбираем самую
        короткую фразу по длине
        на выходе индекс этой строки в списке
        Если нет вхождения всех подстрок то на выходе -1
    '''
    substr = substr.split(';')
    sub_lst = []
    for x in substr:
        x = x.lower().strip()
        if x != '': sub_lst.append(x)
    
    in_lst = [x.lower().strip() for x in lst]
    
    rez_lst = []
    for i in range(len(in_lst)):  # цикл по списку фраз
        f_ok = True
        for s_sub in sub_lst:  # цикл по подстрокам
            f_sub_ok = False
            i_s = 0
            while 1:
                i_fnd = in_lst[i].find(s_sub, i_s, len(in_lst[i]))
                if i_fnd < 0:
                    f_ok = False
                    break
                else:
                    f_sub_ok_start = False  # Проверка символа перед подстроки
                    f_sub_ok_end = False  # роверка символа после подстроки
                    l_s_sub = i_fnd + len(s_sub)
                    if len(in_lst[i]) == l_s_sub:  # подстрока в конце строки
                        f_sub_ok_end = True
                    else:  # подстрока не в конце строки и следующий символ буква
                        if not in_lst[i][l_s_sub].isalpha():
                            f_sub_ok_end = True
                    if i_fnd == 0: f_sub_ok_start = True
                    elif not in_lst[i][i_fnd-1].isalpha(): f_sub_ok_start = True
                    if f_sub_ok_start and f_sub_ok_end:
                        f_sub_ok = True
                        break
                    
                i_s = i_fnd + len(s_sub)
            if f_sub_ok == False:
                f_ok = False
                break
                
        if f_ok: rez_lst.append((i, in_lst[i]))
    if len(rez_lst) == 1:
        return rez_lst[0][0]
    elif len(rez_lst) > 1:
        l_max = 10000
        i_max = 0
        for tup in rez_lst:
            l_tup = len(tup[1])
            if l_tup < l_max:
                l_max = l_tup
                i_max = tup[0]
        return i_max
    else: return -1

def find_short(f_lst):
    '''
        Поиск самой короткой фразы в списке и выдача её индекса
    '''
    l_min = 10000
    i_min = 0
    for i in range(len(f_lst)):
        l_phr = len(f_lst[i])
        if l_phr < l_min:
            l_min = l_phr
            i_min = i
    return i_min
    
def find_short_in_cort(f_lst):
    '''
        На входе список кортежей. (индекс, фраза)
        Поиск самой короткой фразы в списке кортежей и выдача её индекса
    '''
    l_min = 10000
    i_min = 0
    for i in range(len(f_lst)):
        l_phr = len(f_lst[i][1])
        if l_phr < l_min:
            l_min = l_phr
            i_min = f_lst[i][0]
    return i_min

def find_short_tup(f_lst):
    '''
        На входе список кортежей.
        в кортеже индекс фразы на странице и фраза
        Поиск самой короткой фразы в списке и выдача её индекса на странице
    '''
    l_min = 10000
    i_min = 0
    for i in range(len(f_lst)):
        l_phr = len(f_lst[i][1])
        if l_phr < l_min:
            l_min = l_phr
            i_min = i
    i_out = f_lst[i_min][0]
    return i_out

lst_off_city =[
    'Донецк',
    'Луганск',
    'Улан-Удэ',
]

def normalize_region(reg):
    dct_reg = {
        'Новгородская область': 'Нижний Новгород',
        'Ярославская область': 'Ярославль',
        'Томская область': 'Томск',
        'Омская область': 'Омск',
        'Ростовская область': 'Ростов-на-Дону',
        'Ленинградская область': 'Санкт-Петербург',
        'Курганская область': 'Курган',
        'Курская область': 'Курск',
        'Самарская область': 'Самара',
        'Саратовская область': 'Саратов',
        'Тульская область': 'Тула',
        'Тверская область': 'Тверь',
        'Пермский край': 'Пермь',
        'Пензенская область': 'Пенза',
        'Брянская область': 'Брянск',
        'Иркутская область': 'Иркутск',
        'Краснодарский край': 'Краснодар',
        'Челябинская область': 'Челябинск',
        'Волгоградская область': 'Волгоград',
        'Воронежская область': 'Воронеж',
    }
    
    if reg in dct_reg: return dct_reg[reg]
    else: return reg
    
def ordering_city(in_city: str):  # Преобразование строки город
    '''
        Проверяем на
        изветсный тип населенного пункта
        выдаем название без типа населенного пункта
        если известный тип не найден - возвращаем входную строку
    '''
    lst_type_city = [
        'рабочий поселок',
        'поселок городского типа',
        'поселок',
        'село',
        'деревня',
    ]

    for tp in lst_type_city:
        i = in_city.find(tp)
        if i >= 0:
            out_city = in_city[i+len(tp):].strip()
            return out_city

    return in_city

def ordering_street(in_street: str):  # Преобразование строки улица
    '''
        разбиваем строку по запятым, и каждый фрагмент проверяем на
        изветсный тип улицы
        выдаем список [тип_улицы, название]
        если известный тип не найден - возвращаем пустой список
        
        Список типов улицы имеет очередность в приоритете определения по убыванию
    '''
    lst_type_raion = [
        'микрорайон',
        'район',
        'станица',
        'поселок',
        'округ',
    ]
    dkt_type_street = {
        'улица': 'ул',
        'проспект': 'пр-кт',
        'переулок': 'пер',
        'бульвар': 'б-р',
        'шоссе': 'ш',
        'аллея': 'ал',
        'тупик': 'туп',
        'проезд': 'пр-д',
        'набережная': 'наб',
        'площадь': 'пл',
    }
    lst_street = in_street.split(',')
    if len(lst_street) == 0: return []

    # разобьем на известные типы районов, типы улиц, и просто выражения
    lst_tr = []
    lst_ts = []
    lst_em = []
    lst_tmp = []
    # Отделим известные типы районов
    for sub in lst_street:
        not_rez = True
        for ts in lst_type_raion:
            if sub.find(ts) >= 0:
                not_rez = False
                lst_tr.append((ts, sub.replace(ts, '').strip()))
                break
        if not_rez: lst_tmp.append(sub.strip())

    if len(lst_tmp) == 0:
        if len(lst_tr) == 1: return lst_tr[0][0], lst_tr[0][1]
        else: return []
    
    # Отделим известные типы улиц
    lst_tmp2 = []
    for sub in lst_tmp:
        not_rez = True
        for ts, sts in dkt_type_street.items():
            if sub.find(ts) >= 0:
                not_rez = False
                lst_ts.append((sts, sub.replace(ts, '').strip()))
                break
        if not_rez: lst_tmp2.append(sub.strip())

    if len(lst_tmp2) == 0:
        if len(lst_ts) == 1: return lst_ts[0][0], lst_ts[0][1]
        else: return []
    else: return '', ' '.join(lst_tmp2)

def ordering_house(in_house: str):  # Преобразование строки дом
    '''
        Варианты домов
        1 просто цифра          14
        2 цифра с буквой        30А
        3 цифра / цифра         31/41
        4 цифра буквы цифра     30 корп 3       (корп) вычленяем по "к"
        5 цифра буквы буква(ы)  12 лит А(АД)    вычленяем по "л"
        
        На входе строка с номером дома
        Заменяем двойные пробелы на одинарные и преобразуем в нижний регистр
        
        
        На выходе кортеж (N, str_num) где N первая цифра дома,
        а str_num преобразованный полный номер
        Если ошибка парсинга - ('', 'тип ошибки')
        
    '''
    in_house = in_house.replace('-', ' ')
    in_house = in_house.strip()
    if len(in_house) == 0: return ('', 'Не задан номер')
    if in_house.isdigit(): return (in_house, in_house)
    if len(in_house) < 2 and in_house[0].isalpha(): return ('', 'Номер из одной буквы')  # Номер дома не может быть из одной буквы
    # Проходим по строке и если цифры сливаются с буквами вставляем пробел
    n_house = ''
    lst_house = [in_house[0],]
    is_dig = False
    if in_house[0].isdigit(): is_dig = True
    for i in range(1, len(in_house)):
        if in_house[i].isdigit() and is_dig == False:
            is_dig = True
            lst_house.append(' ')
        if in_house[i].isalpha() and is_dig == True:
            is_dig = False
            lst_house.append(' ')
        if not in_house[i].isdigit() and not in_house[i].isalpha():
            lst_house.append(' ')
        lst_house.append(in_house[i])
    in_house = ''.join(lst_house)
    # Заменяем двойные пробелы на одинарные
    while '  ' in in_house:
        in_house = in_house.replace('  ', ' ')
    # Проверка на дробь
    lst_house = in_house.split('/')
    if len(lst_house) > 2: return ('', 'Много слешей')
    if len(lst_house) == 2: return (lst_house[0], in_house)
    # Остались корп, лит, буква
    lst_house = in_house.split(' ')
    if len(lst_house) == 1: return (lst_house[0], lst_house[0])
    if len(lst_house) > 3: return ('', 'В номере много позиций')
    if len(lst_house) == 2:  # значит буква - склеиваем как 30А
        lst_house[1] = lst_house[1].lower()
        return (lst_house[0], '/'.join(lst_house))
    # анализируем  корп, литер
    if lst_house[1].find('к') >= 0:
        lst_house[1] = '/'
        return (lst_house[0], ''.join(lst_house))
    if lst_house[1].find('л') >= 0:
        lst_house[1] = '/'
        return (lst_house[0], ''.join(lst_house))
    
    return ('', 'Номер не распознан')

def get_txv(data):
    driver = None
    try:
        base_url = 'https://internet-tv-dom.ru/operator'
        
        EXE_PATH = 'driver/chromedriver.exe'
        service = Service(EXE_PATH)
        driver = webdriver.Chrome(service=service)

        # EXE_PATH = r'c:/Dev/bot_opsos/driver/firefoxdriver.exe'
        # driver = webdriver.Firefox(executable_path=EXE_PATH)

        driver.implicitly_wait(1)
        driver.get(base_url)
        time.sleep(3)
        
        ###################### Страница ссылок городов ######################
        region = data.get('region', '')
        if region:
            region = region.replace('ё', 'е')
            region = normalize_region(region)
        city = data.get('city', '')
        if city:
            city = city.replace('ё', 'е')
            city = ordering_city(city)
        else: raise Exception('Ошибка город не задан.')
        
        # Проверим на города/регионы в отсутствующих для подключения
        off_ok = False
        for off_reg in lst_off_city:
            if city.find(off_reg) >= 0 or region.find(off_reg) >= 0: off_ok = True
        
        if off_ok:
            data['available_connect'] = 'В регионе нет ТхВ.'
            raise Exception('')
        
        els = driver.find_elements(By.XPATH, '//div[@id="b12356"]')
        if len(els) != 1: raise Exception('Ошибка нет блока городов')
        els_a = els[0].find_elements(By.TAG_NAME, 'a')
        if len(els_a) == 0: raise Exception('Ошибка нет городов')
        url_city = ''
        for el_a in els_a:
            if el_a.text == city or el_a.text == region:
                url_city = el_a.get_attribute('href')
                a_city = el_a
        if url_city:
            driver.get(url_city)
        else: raise Exception(f'Ошибка город {city} в списке городов не найден')
        time.sleep(5)

        ###################### Страница Логин/Пароль ######################
        els = driver.find_elements(By.XPATH, '//input[@name="login$c"]')
        if len(els) != 1: raise Exception('Ошибка Нет поля логин')
        login = data.get('login')
        try: 
            if login: els[0].send_keys(login)
            else: raise Exception('Ошибка не задан логин')
        except: raise Exception('Ошибка ввода логин')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@name="passwd$c"]')
        if len(els) != 1: raise Exception('Ошибка Нет поля пароль')
        password = data.get('password')
        try: 
            if password: els[0].send_keys(password)
            else: raise Exception('Ошибка не задан пароль')
        except: raise Exception('Ошибка ввода пароль')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@type="submit"]')
        if len(els) != 1: raise Exception('Ошибка Нет кнопки Войти')
        try: els[0].click()
        except: raise Exception('Ошибка клика войти')
        time.sleep(5)
        ###################### Страница Фреймы ######################
        # frame name="topframe"
        # frame name="leftframe"
        # frame name="mainFrame"
        # driver.switch_to_default_content()  # вернуться к родительскому кадру
        driver.switch_to.frame('leftframe')  # Загружаем фрейм
        time.sleep(3)
        f_ok = False
        els_a = driver.find_elements(By.TAG_NAME, 'a')
        for el_a in els_a:
            if el_a.text == 'Создать договор':
                f_ok = True
                try: el_a.click()
                except: raise Exception('Ошибка клика Создать договор')
                break
        if f_ok == False: raise Exception('Ошибка Нет ссылки Создать договор')
        time.sleep(3)
        
        driver.switch_to.default_content()  # Загружаем родительский фрейм
        time.sleep(1)
        driver.switch_to.frame('mainFrame')  # Загружаем фрейм
        time.sleep(3)
        
        # Жмем кнопку Далее
        els = driver.find_elements(By.XPATH, '//input[@id="dalee_id_button"]')
        if len(els) != 1: raise Exception('Ошибка Нет кнопки Далее')
        try: els[0].click()
        except: raise Exception('Ошибка клика кнопки Далее')
        time.sleep(5)
        ###################### Блок ввода адреса ######################
        els_addr = driver.find_elements(By.XPATH, '//div[@id="adress_content"]')
        if len(els_addr) != 1: raise Exception('Ошибка Нет блока адреса')
        el_addr = els_addr[0]
        
        # Вводим город
        els_city = el_addr.find_elements(By.XPATH, './/input[@id="city_area_name"]')
        if len(els_city) != 1: raise Exception('Ошибка Нет поля ввода город')
        el_city = els_city[0]
        # Удалим если что-то уже введено
        try:
            el_city.click()
            time.sleep(0.2)
            el_city.send_keys(Keys.CONTROL + 'a')
            time.sleep(0.2)
            el_city.send_keys(Keys.DELETE)
            time.sleep(0.2)
            el_city.send_keys(city)
        except: raise Exception('Ошибка ввода город')
        time.sleep(5)
        # отлавливаем подсказку
        f_ok = False
        f_str = []
        els_ul = driver.find_elements(By.TAG_NAME, 'ul')
        for el_ul in els_ul:
            str_class = el_ul.get_attribute('class')
            if str_class.find('display: none') >= 0: continue
            els_li = el_ul.find_elements(By.TAG_NAME, 'li')
            if len(els_li) > 0:
                for i in range(len(els_li)):
                    a_s = els_li[i].find_elements(By.TAG_NAME, 'a')
                    if len(a_s[0].text) > 0: f_str.append(a_s[0].text)
                if len(f_str) > 0:
                    f_ok = True
                    i_sh = find_short(f_str)
                    try: els_li[i_sh].click()
                    except: raise Exception('Ошибка клика выбора город')
                    time.sleep(5)
                
            if f_ok == True: break
        if f_ok == False: raise Exception(f'Ошибка Город: {city} не найден.')

        # Вводим улицу
        els_street = el_addr.find_elements(By.XPATH, './/input[@id="street_name"]')
        if len(els_street) != 1: raise Exception('Ошибка Нет поля ввода Улица')
        street = data.get('street')
        if street: street = street.replace('ё', 'е')
        else: raise Exception('Ошибка Не задано значение Улица')
        lst_street = ordering_street(street)
        # print(lst_street)
        if lst_street:  # если распознали по типу
            try: els_street[0].send_keys(lst_street[1])
            except: raise Exception('Ошибка ввода 7')
        else:  # если нет - вводим как есть
            try: els_street[0].send_keys(street)
            except: raise Exception('Ошибка ввода 8')
            lst_street = ('', street)

        time.sleep(5)
        
        # отлавливаем подсказку
        f_ok == False
        els_ul = driver.find_elements(By.TAG_NAME, 'ul')
        for el_ul in els_ul:
            str_style = el_ul.get_attribute('style')
            if str_style.find('display: none') >= 0: continue
            els_li = el_ul.find_elements(By.TAG_NAME, 'li')
            if len(els_li) == 0: continue
            f_str = []
            for i in range(len(els_li)):
                a_s = els_li[i].find_elements(By.TAG_NAME, 'a')
                if len(a_s) > 0:
                    txt = a_s[0].text
                    if txt.find(lst_street[1].lower()) >= 0: f_str.append((i, txt))
                    
            if len(f_str) == 0: raise Exception(f'Ошибка Улица: {street} не найдена.')
            elif len(f_str) == 1:
                try: els_li[f_str[0][0]].click()
                except: raise Exception('Ошибка действий 14')
                f_ok = True
            else:
                if lst_street[0] != '':
                    # Название попало во множественный выбор, проверим на тип улицы
                    f_str2 = []
                    for st in f_str:
                        if st[1].find(lst_street[0]) >= 0: f_str2.append(st)
                    if len(f_str2) == 0: f_str2 = f_str
                else:
                    f_str2 = f_str
                # тут 1 или более вариантов
                i_fnd = find_short_tup(f_str2)
                try: els_li[i_fnd].click()
                except: raise Exception('Ошибка действий 15')
                f_ok = True
            time.sleep(1)

        if f_ok == False: raise Exception(f'Ошибка Улица: {street} не найдена2.')
        
        # Вводим дом
        els_house = el_addr.find_elements(By.XPATH, './/input[@id="house_id"]')
        if len(els_house) != 1: raise Exception('Ошибка Нет поля ввода Дом')
        house = data.get('house')
        if house == None: raise Exception('Ошибка Не задано значение Дом')
        or_house = ordering_house(house)
        try: els_house[0].send_keys(or_house[0])
        except: raise Exception('Ошибка ввода дома')
        time.sleep(5)
        # отлавливаем подсказку
        f_ok = False
        f_str = []
        els_ul = driver.find_elements(By.TAG_NAME, 'ul')
        for el_ul in els_ul:
            str_class = el_ul.get_attribute('class')
            if str_class.find('display: none') >= 0: continue
            els_li = el_ul.find_elements(By.TAG_NAME, 'li')
            if len(els_li) > 0:
                for i in range(len(els_li)):
                    a_s = els_li[i].find_elements(By.TAG_NAME, 'a')
                    hs = a_s[0].text
                    if len(hs) == 0: continue
                    if hs.find(or_house[1]) >= 0:
                        cort = (i, hs)
                        f_str.append(cort)
                if len(f_str) > 0:
                    f_ok = True
                    i_sh = find_short_in_cort(f_str)
                    try: els_li[i_sh].click()
                    except: raise Exception('Ошибка клика выбора дома')
                    time.sleep(5)
            if f_ok == True: break
        if f_ok == False: raise Exception(f'Ошибка Дом: {house} не найден')
        
        
        
        # Смотрим блок технической возможности дома
        lst_av_connect = []
        els = el_addr.find_elements(By.XPATH, './/td[@id="house_connected"]')
        if len(els) != 1: raise Exception('Ошибка Нет поля ТхВ дома')
        els_div = els[0].find_elements(By.TAG_NAME, 'div')
        for el_div in els_div:
            text = el_div.text.strip()
            if text: lst_av_connect.append(text)
        
        # Вводим квартиру
        els_anum = el_addr.find_elements(By.XPATH, './/input[@id="anum"]')
        if len(els_anum) != 1: raise Exception('Ошибка Нет поля ввода Квартира')
        apartment = data.get('apartment')
        if apartment == None: raise Exception('Ошибка Не задано значение Квартира')
        try: els_anum[0].send_keys(apartment)
        except: raise Exception('Ошибка ввода Квартира')
        time.sleep(3)
        els = el_addr.find_elements(By.XPATH, './/textarea[@id="adress_comment"]')
        if len(els) != 1: raise Exception('Ошибка Нет поля комментарий к адресу')
        try: els[0].click()
        except: raise Exception('Ошибка клика поля комментарий к адресу')
        time.sleep(3)
        # Смотрим блок технической возможности квартиры
        els = el_addr.find_elements(By.XPATH, './/tr[@id="tr_anum"]')
        if len(els) != 1: raise Exception('Ошибка Нет блока ТхВ')
        els_td = els[0].find_elements(By.TAG_NAME, 'td')
        if len(els_td) != 3: raise Exception('Ошибка Неправильная структура блока ТхВ')
        els_div = els_td[2].find_elements(By.TAG_NAME, 'div')
        for el_div in els_div:
            text = el_div.text.strip()
            if text: lst_av_connect.append(text)
        # Квартира подключена к интернет
        # Квартира подключена к ТВ
        # Квартира подключена к IPTV
        # Квартира не подключена к Домофонии
        # Квартира подключена к видеоконтролю
        # Промо-период доступен
        data['available_connect'] = '\n'.join(lst_av_connect)
        # Соберем информацию об адресе
        address = ''
        els_city = el_addr.find_elements(By.XPATH, './/input[@id="city_area_name"]')
        if els_city[0]: address += els_city[0].get_attribute('value') + ', '
        address += els_street[0].get_attribute('value') + ', '
        address += 'д.' + els_house[0].get_attribute('value') + ', '
        address += 'кв.' + els_anum[0].get_attribute('value') + ', '
        els_porche = el_addr.find_elements(By.XPATH, './/tr[@id="tr_porche"]')
        if els_porche[0]:
            els_lbl = els_porche[0].find_elements(By.XPATH, './/td[@class="porche"]')
            if els_lbl[0]: address += 'подъезд ' + els_lbl[0].text
        data['pv_address'] = address
        
        data['tarifs_all'] = ''
            

            # #===========
            # time.sleep(10)
            # with open('out.html', 'w', encoding='utf-8') as outfile:
                # outfile.write(driver.page_source)
            # raise Exception('Финиш.')
            # #===========

        
    except Exception as e:
        return str(e)[:100], data
    finally:
        if driver: driver.quit()
   
    return '', data

def set_txv_to_dj_domconnect(pv_code):
    url = url_host + 'api/set_txv'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
        'pv_code': pv_code,
        'login': 'sinitsin',
        'password': 'BVNocturne20',
        'id_lid': '1215557',
        
        'region': 'Вор область',
        'city': 'Воронеж',           # город
        'street': 'улица Индустриальн',         # улица
        'house': '21',          # дом
        'apartment': '2',          # квартира
        
        'available_connect': '',
        'pv_address': '',
        'tarifs_all': '',
    }
    
    try:
        responce = requests.get(url, headers=headers, params=params)
        print(responce.status_code)
        print(responce.text)
    except:
        pass
        print('Error: requests.get')

def get_txv_in_dj_domconnect(pv_code):
    url = url_host + 'api/get_txv'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
        'pv_code': pv_code,
    }
    
    try:
        responce = requests.get(url, headers=headers, params=params)
    except:
        return 1, []
    if responce.status_code == 200:
        bid_list = json.loads(responce.text)
        return 0, bid_list
    return 2, []

def set_txv_status(status, data):
    url = url_host + 'api/set_txv_status'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    send_data = {
        'key': 'Q8kGM1HfWz',
        'id': data.get('id'),
        'available_connect': data.get('available_connect'),  # Возможность подключения
        'tarifs_all': data.get('tarifs_all'), # список названий тарифных планов
        'pv_address': data.get('pv_address'),
        'status': status,
    }
    bot_log = data.get('bot_log')
    if bot_log:
        send_data['bot_log'] = bot_log
    try:
        responce = requests.post(url, headers=headers, json=send_data)
        st_code = responce.status_code
        if st_code != 200: return st_code
    except Exception as e:
        return str(e)

def send_crm_txv(txv_dict, opsos):
    user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': user_agent_val,
    }

    restrictions = ''
    error_message = txv_dict.get('bot_log')
    if error_message: restrictions += f'{error_message}\n'
    
    pv_address = txv_dict.get('pv_address')
    if pv_address: restrictions += f'{opsos} определил адрес как: {pv_address}\n'
    
    available_connect = txv_dict.get('available_connect')
    if available_connect: restrictions += f'Возможность подключения: {available_connect}\n'
    
    # Проверим статус лида
    upgrade_status = False
    if available_connect.find('Дом подключен к интернет') >= 0 or available_connect.find('Квартира подключена к интернет') >= 0:
        url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.get'
        params = {
            'id': txv_dict.get('id_lid'),
        }
        try:
            responce = requests.post(url, headers=headers, params=params)
            st_code = responce.status_code
            if st_code != 200: return st_code, ''
            lid = json.loads(responce.text)
            result = lid.get('result')
            status = result.get('STATUS_ID')
            if status and status == '77': upgrade_status = True
        except Exception as e:
            return str(e), ''

    params = {
        'id': txv_dict.get('id_lid'),
        'fields[UF_CRM_1638779781554][]': restrictions[:500],  # вся инфа
    }
    up_status = ''
    if upgrade_status:
        params['fields[STATUS_ID]'] = '72'
        up_status = 'Статус обновлен.'

    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.update'
    try:
        responce = requests.post(url, headers=headers, params=params)
        st_code = responce.status_code
        if st_code != 200: return st_code, ''
        # посмотреть результат https://crm.domconnect.ru/crm/lead/details/1215557/
    except Exception as e:
        return str(e), ''
    return '', up_status
    
def send_telegram(chat: str, token: str, text: str):
    url = "https://api.telegram.org/bot" + token + "/sendMessage"
    try:
        r = requests.post(url, data={
            "chat_id": chat,
            "text": text
        })
    except:
        return 600
    return r.status_code

def run_txv_domru(tlg_chat, tlg_token):
    tlg_mess = ''
    
    # личный бот @infra
    TELEGRAM_CHAT_ID = '1740645090'
    TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'
    
    rez, txv_list = get_txv_in_dj_domconnect(pv_code)
    if rez:
        tlg_mess = 'Ошибка при загрузке запросов из domconnect.ru'
        r = send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, tlg_mess)
        print(tlg_mess, '\nTelegramMessage:', r)
        return
    if len(txv_list) == 0:
        cur_time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        print(f'{cur_time} {opsos}: Запросов ТхВ нет')
        return

    # Перелистываем список словарей с заявками
    for txv_dict in txv_list:
        rez, data = get_txv(txv_dict)
        data['bot_log'] = rez
        e, up_status = send_crm_txv(data, opsos)  # ответ в CRM
        crm_mess = f'Ошибка при отправке в СРМ: {e}\n'
        if e:
            tlg_mess += crm_mess
            data['bot_log'] += crm_mess
        address = f'{data.get("city")} {data.get("street")} д.{data.get("house")} кв.{data.get("apartment")}'
        tlg_mess += f'{opsos}: - Выполнен запрос ТхВ\n'
        tlg_mess += f'Адрес: {address}\n'
        djdc = ''
        if rez == '':  # заявка успешно создана
            djdc = set_txv_status(3, data)
            tlg_mess += f'Успешно. {up_status}\n'
        else:  # не прошло
            djdc = set_txv_status(2, data)
            tlg_mess += f'{data.get("bot_log")}\n'
        if djdc: tlg_mess += f'Ошибка при отправке в dj_domconnect: {djdc}'
        r = send_telegram(tlg_chat, tlg_token, tlg_mess)
        print(tlg_mess)
        print('TelegramMessage:', r)
    #================================================

if __name__ == '__main__':
    # start_time = datetime.now()
    
    # https://internet-tv-dom.ru/operator
    # login: sinitsin
    # password: BVNocturne20

    # txv_dict = {
        # 'pv_code': pv_code,
        # 'login': 'sinitsin',
        # 'password': 'BVNocturne20',
        # 'id_lid': '1215557',
        

        # # 'region': 'Воронежская область',           # город
        # # 'city': 'Воронеж',           # город
        # # 'street': 'Пирогова',         # улица
        # # 'house': '35',          # дом
        # # 'apartment': '197',          # квартира

        # # 'region': 'Самарская область',           # город
        # # 'city': 'Самара',           # город
        # # 'street': 'Партизанская улица',         # улица
        # # 'house': '206',          # дом
        # # 'apartment': '10',          # квартира

        # # 'region': 'Омская область',           # город
        # # 'city': 'Омск',           # город
        # # 'street': 'микрорайон Городок Нефтяников, Энтузиастов',         # улица
        # # 'house': '31',          # дом
        # # 'apartment': '10',          # квартира

        # 'region': 'Санкт-Петербург',           # город
        # 'city': 'Санкт-Петербург',           # город
        # 'street': 'Шкапина',         # улица
        # 'house': '9-11',          # дом
        # 'apartment': '5',          # квартира

        # 'available_connect': '',
        # 'pv_address': '',
        # 'tarifs_all': '',
    # }
    
    
    # # e, data = get_txv(txv_dict)
    # # if e: print(e)
    # # print('available_connect:\n', data['available_connect'])
    # # print('pv_address:\n', data['pv_address'])
    
    # print(ordering_house('9-11'))
    
    
            # if in_house[i].isdigit() and is_dig == False:
            # is_dig = True
            # lst_house.append(' ')
        # if in_house[i].isalpha() and is_dig == True:

    # set_txv_to_dj_domconnect(pv_code)
    # rez, txv_list = get_txv_in_dj_domconnect(pv_code)
    # for txv_dict in txv_list:
        # for k, v in txv_dict.items():
            # print(k, v)
    # data = {'id': 1, 'pv_address': '55632145', 'bot_log': 'Заявка принята С'}
    # r = set_txv_status(0, data)
    # print(r)
    
    # rez, stre = search_for_an_entry(lst_street, 'Светла')
    # rez = search_for_an_entry(lst_reg, 'ярославль')
    # rez = search_for_an_entry(lst_reg, 'Санкт-Петербург')
    

    # Калужская область	Калуга	улица Ленина 31
    # Санкт-Петербург Санкт-Петербург улица Маршала Казакова 78к1
    # Ярославская область Ярославль проспект Толбухина 31


    
    
    pass
    
    # end_time = datetime.now()
    # time_str = '\nDuration: {}'.format(end_time - start_time)
    # print(time_str)
    # # limit_request_line

