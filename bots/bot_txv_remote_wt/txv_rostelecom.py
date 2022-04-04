import os
import time
from datetime import datetime
import requests  # pip install requests
import json
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'
opsos = 'Ростелесом'
pv_code = 4


regions = [
    ('Волга', '6'),             # 0
    ('Дальний Восток', '2'),    # 1
    ('Москва', '8'),            # 2
    ('Северо-Запад', '3'),      # 3
    ('Сибирь', '4'),            # 4
    ('Урал', '7'),              # 5
    ('Центр', '1'),             # 6
    ('ЮГ', '5')                 # 7
]
oblasti = [
    ('Башкортостан республика', 0, 0),
    ('Кировская область', 0, 1),
    ('Марий Эл республика', 0, 2),
    ('Мордовия республика', 0, 3),
    ('Нижегородская область', 0, 4),
    ('Оренбургская область', 0, 5),
    ('Пензенская область', 0, 6),
    ('Самарская область', 0, 7),
    ('Саратовская область', 0, 8),
    ('Татарстан республика', 0, 9),
    ('Удмуртская республика', 0, 10),
    ('Ульяновская область', 0, 11),
    ('Чувашская республика', 0, 12),
    ('Амурская область', 1, 0),
    ('Еврейская Автономная область', 1, 1),
    ('Камчатский край', 1, 2),
    ('Магаданская область', 1, 3),
    ('Приморский край', 1, 4),
    ('Саха (Якутия) республика', 1, 5),
    ('Сахалинская область', 1, 6),
    ('Хабаровский край', 1, 7),
    ('Чукотский Автономный округ', 1, 8),
    ('Москва', 2, 0),
    ('Московская область', 2, 1),
    ('Архангельская область', 3, 0),
    ('Вологодская область', 3, 1),
    ('Калининградская область', 3, 2),
    ('Карелия республика', 3, 3),
    ('Коми республика', 3, 4),
    ('Ленинградская область', 3, 5),
    ('Мурманская область', 3, 6),
    ('Новгородская область', 3, 7),
    ('Псковская область', 3, 8),
    ('Санкт-Петербург', 3, 9),
    ('Алтай республика', 4, 0),
    ('Алтайский край', 4, 1),
    ('Бурятия республика', 4, 2),
    ('Забайкальский край', 4, 3),
    ('Иркутская область', 4, 4),
    ('Кемеровская область', 4, 5),
    ('Красноярский край', 4, 6),
    ('Новосибирская область', 4, 7),
    ('Омская область', 4, 8),
    ('Томская область', 4, 9),
    ('Тыва республика', 4, 10),
    ('Хакасия республика', 4, 11),
    ('Курганская область', 5, 0),
    ('Пермский край', 5, 1),
    ('Свердловская область', 5, 2),
    ('Тюменская область', 5, 3),
    ('Ханты-Мансийский Автономный округ - Югра', 5, 4),
    ('Челябинская область', 5, 5),
    ('Ямало-Ненецкий Автономный округ', 5, 6),
    ('Белгородская область', 6, 0),
    ('Брянская область', 6, 1),
    ('Владимирская область', 6, 2),
    ('Воронежская область', 6, 3),
    ('Ивановская область', 6, 4),
    ('Калужская область', 6, 5),
    ('Костромская область', 6, 6),
    ('Курская область', 6, 7),
    ('Липецкая область', 6, 8),
    ('Орловская область', 6, 9),
    ('Рязанская область', 6, 10),
    ('Смоленская область', 6, 11),
    ('Тамбовская область', 6, 12),
    ('Тверская область', 6, 13),
    ('Тульская область', 6, 14),
    ('Ярославская область', 6, 15),
    ('Адыгея республика', 7, 0),
    ('Астраханская область', 7, 1),
    ('Волгоградская область', 7, 2),
    ('Дагестан республика', 7, 3),
    ('Ингушетия республика', 7, 4),
    ('Кабардино-Балкарская республика', 7, 5),
    ('Калмыкия республика', 7, 6),
    ('Карачаево-Черкесская республика', 7, 7),
    ('Краснодарский край', 7, 8),
    ('Ростовская область', 7, 9),
    ('Северная Осетия — Алания республика', 7, 10),
    ('Ставропольский край', 7, 11),
    ('Чеченская республика', 7, 12),
]
street_abbr = {
    'улица': 'ул.',
    'проспект': 'пр-кт',
    'переулок': 'пер.',
    'бульвар': 'б-р',
    'шоссе': 'ш.',
    'аллея': 'аллея',
    'тупик': 'туп.',
    'проезд': 'проезд',
    'набережная': 'наб.',
    'площадь': 'пл.',
}
street_exc_abbr = {  # исключаем их из поиска
    'район': 'р-н',
    'микрорайон': 'мкр.',
}
city_abbr = {
    'дачный поселок': 'дп.',
    'рабочий поселок': 'рп.',
    'городской поселок': 'пгт.',
    'поселок': 'п.',
    'село': 'с.',
    'деревня': 'д.',
}

def ordering_region(in_region: str):  # Преобразование строки регион
    '''
        анализируем строку на изветсный тип региона
        если тип вначале - удаляем и обрезаем конечные пробелы
        возвращаем измененную строку если есть изменения
        
    '''
    lst_type_region = [
        'республика',
        'область',
        'край',
        'округ',
    ]
    # у входящей строки преобразуем в нижний регистр первый символ
    reg = in_region[:1].lower() + in_region[1:]
    
    for tp in lst_type_region:
        if reg.find(tp) == 0:
            return reg[len(tp):].strip()
    return in_region

def find_regions(obls: list, regs: list, in_str: str):  # Поиск вхождения фразы в списке фраз
    '''
        Поиск вхождения фразы в списке фраз
        Поиск ведется последовательно начиная с первой буквы in_str
        - назовем её подстрока. Если таких вхождений в списке много,
        2 и более добавляем следующую букву к подстроке.
        Поиск завершен если вхождений только одно.
        код_листа берем из списка регионов
        Возвращаем индекс фразы в списке и индекс её в группе. (id_в _группе, id_в_списке, код_листа)
        Если нет вхождений - возвращаем (-1, -1, -1)
    '''
    in_str = in_str.replace('ё', 'е')
    
    ret_id = -1
    ret_group_id = -1
    
    # Если "Республика вначале"
    if in_str.find('Республика') == 0:
        lst = in_str.split(' ')
        lst.pop(0)
        lst.append('республика')
        in_str = ' '.join(lst)
    
    # поиск с циклом по набиранию подстроки
    for i_s in range(len(in_str)):
        sub_str = in_str[0:i_s+1]
        cnt_phr = 0
        # просмотрим список на вхождение
        for i_lst in range(len(obls)):
            if obls[i_lst][0].find(sub_str) >= 0:
                cnt_phr += 1
                ret_id = i_lst
        if cnt_phr > 1:
            ret_id = -1
        else:
            break
    
    if ret_id >= 0:
        id_group = obls[ret_id][1]
        id_reg = obls[ret_id][2]
        id_code = regs[id_group][1]
        return (id_group, id_reg, id_code)  # похожая фраза найдена и она в единственной строке
    
    return (-1, -1, -1)

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

def ordering_string(in_street: str, in_abbr: dict):  # Преобразование строки населенный пункт, улица
    '''
        разбиваем строку по запятым, и каждый фрагмент проверяем на
        известный тип улицы
        выдаем список [тип_улицы, название]
        если известный тип не найден - возвращаем пустой список
    '''
    out_cort = []
    lst = in_street.split(',')
    for sub in lst:
        rez = False
        for ts in in_abbr:
            if sub.find(ts) >= 0:
                rez = True
                out_cort.append(ts)
                out_cort.append(sub.replace(ts, '').strip())
                break
        if rez: break
    return out_cort

def remove_street_exc_abbr(in_street: str):
    '''
        разбиваем строку по запятым, и каждый фрагмент проверяем на
        известный тип района, удаляем его
        возвращаем что осталось
    '''
    out_lst = []
    lst = in_street.split(',')
    for sub in lst:
        rez = False
        for ex in street_exc_abbr:
            if sub.find(ex) >= 0:
                rez = True
                break
        if rez == False: out_lst.append(sub.strip())
        
    return ','.join(out_lst)
    
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

def wait_spinner(driver):  # Ожидаем крутящийся спинер
    driver.implicitly_wait(1)
    while True:
        time.sleep(1)
        els = driver.find_elements(By.XPATH, '//div[contains(@class, "ju-spinner")]')
        if len(els):
            print('ju-spinner')
        else: break
    driver.implicitly_wait(10)
    time.sleep(2)

def replace_part_house(lst: list):
    new_lst = []
    for s in lst:
        if s.find('к') >= 0: continue
        if s.find('л') >= 0: continue
        if s.find('с') >= 0: continue
        new_lst.append(s)
        
    
    return new_lst

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
        
        
        На выходе кортеж (N, lst_num) где N первая цифра дома,
        а lst_num список частей номера 
        Если ошибка парсинга - ('', [])
        
    '''
    # '14', '30А', '31/41', '30 корп 3', '30 корп3', '12 лит А(АД)', '30 лит 3', '30 стр. 3', '31/41корп2', '31/41 корп2', '31/41 корп 2', '1', '205', 'й'
    
    
    in_house = in_house.strip().lower()
    if len(in_house) == 0: return ('', [])
    if in_house.isdigit(): return (in_house, [in_house, ])
    if len(in_house) < 2 and in_house[0].isalpha(): return ('', [])  # Номер дома не может быть из одной буквы
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
        lst_house.append(in_house[i])
    in_house = ''.join(lst_house)
    # Заменяем двойные пробелы на одинарные
    while '  ' in in_house:
        in_house = in_house.replace('  ', ' ')
    # Проверка на дробь
    lst_house = in_house.split('/')
    if len(lst_house) > 2: return ('', [])
    if len(lst_house) == 2:
        lst2_house = lst_house[1].split(' ')
        lst2_house = [lst_house[0], ] + replace_part_house(lst2_house)  # Заменим корп, лит, стр на к, л, с
        return (lst_house[0], lst2_house)
    # Разделяем по пробелу
    lst2_house = in_house.split(' ')
    lst2_house = replace_part_house(lst2_house)  # Заменим корп, лит, стр на к, л, с
    return (lst2_house[0], lst2_house)

def find_string_to_listsubstrs(in_lst: list, f_lst: list):  # Поиск строки в in_lst по вхождению списка подстрок
    sub_lst = []
    for x in f_lst:
        x = x.lower().strip()
        if x != '': sub_lst.append(x)
    
    in_lst = [x.lower().strip() for x in in_lst]
    
    rez_lst = []
    for i in range(len(in_lst)):  # цикл по списку фраз
        f_ok = True
        in_str = in_lst[i]
        for s_sub in sub_lst:  # цикл по подстрокам
            if in_str.find(s_sub) >= 0:
                in_str = in_str.replace(s_sub, '')
                continue
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
    
# =========================================================

def get_txv(data):
    driver = None
    try:
        base_url = 'https://eissd.rt.ru/login'
        
        EXE_PATH = 'driver/chromedriver.exe'
        driver = webdriver.Chrome(executable_path=EXE_PATH)

        # EXE_PATH = r'c:/Dev/bot_opsos/driver/firefoxdriver.exe'
        # driver = webdriver.Firefox(executable_path=EXE_PATH)

        driver.implicitly_wait(10)
        driver.get(base_url)
        time.sleep(3)
        
        # ###################### Login ######################
        login = data.get('login')
        if login:
            els = driver.find_elements(By.XPATH, '//input[@data-field="login"]')
            try: els[0].send_keys(login)
            except: raise Exception('Ошибка ввода логин')
            time.sleep(1)
        else: raise Exception('Ошибка не задан логин')

        password = data.get('password')
        if password:
            els = driver.find_elements(By.XPATH, '//input[@data-field="passw"]')
            try: els[0].send_keys(password)
            except: raise Exception('Ошибка ввода пароля')
            time.sleep(2)
        else: raise Exception('Ошибка не задан пароль')

        els = driver.find_elements(By.XPATH, '//input[@data-field="closeOthers"]')
        # Обычным способом чекбокс не отмечается - element not interactable
        try: driver.execute_script("arguments[0].click();", els[0])
        except: raise Exception('Ошибка отметки чекбокса закрыть другие сессии')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@value="Войти"]')
        try: els[0].click()
        except: raise Exception('Ошибка нажатия кнопки авторизации')
        time.sleep(1)
        
        wait_spinner(driver)  # Подождем если есть спинер
        
        driver.implicitly_wait(1)
        els = driver.find_elements(By.XPATH, '//div[@class="form-group error"]')
        if els: raise Exception(f'Ошибка {els[0].text}')  # Неверное имя пользователя или пароль
        driver.implicitly_wait(10)
        ###################### Главная страница ######################
        els = driver.find_elements(By.XPATH, '//a[@href="/order/phys/edit"]')
        if len(els) < 2: raise Exception('Нет ссылки Создать заявку ФЛ')
        try: els[1].click()
        except: raise Exception('Ошибка клика ссылки перехода на страницу ввода заявки')
        time.sleep(3)
        ###################### Страница ввода заявки ######################
        # проверим всплывашки с рекламой
        driver.implicitly_wait(2)
        els = driver.find_elements(By.XPATH, '//div[@class="ju-popup ju-message user-messages-popup "]')
        for el in els:
            els_btn = el.find_elements(By.TAG_NAME, 'input')
            try: driver.execute_script("arguments[0].click();", els_btn[0])
            except: raise Exception('Ошибка закрытия окна всплывашки с рекламой')
            time.sleep(1)
        driver.implicitly_wait(10)

        # Выбираем регион
        els = driver.find_elements(By.XPATH, '//input[@data-field="regionName"]')
        try: els[0].click()
        except: raise Exception('Ошибка выбора региона')
        time.sleep(1)
        # Блок регионов
        els_block = driver.find_elements(By.XPATH, '//ul[@class="itemlist-0-0 treeview"]')
        if len(els_block) == 0: raise Exception('Ошибка нет блока регионов')
        
        region = data.get('region')
        if region == None: raise Exception('Ошибка Регион не задан')
        id_group, id_reg, id_code = find_regions(oblasti, regions, region)
        if id_group < 0: raise Exception('Ошибка Регион не найден')
        # Блок групп
        els_span = els_block[0].find_elements(By.TAG_NAME, 'span')
        if len(els_span) != 8: raise Exception('Ошибка неверное колличество регионов в списке')
        try: els_span[id_group].click()
        except: raise Exception('Ошибка клика групп регионов')
        time.sleep(1)
        # Подтянулся список областей
        ul_class_path = f'./*//ul[@class="itemlist-1-{id_code} treeview"]'
        els_ul = els_block[0].find_elements(By.XPATH, ul_class_path)
        if len(els_ul) != 1: raise Exception('Ошибка нет вложенного списка областей')
        els_a = els_ul[0].find_elements(By.TAG_NAME, 'a')
        try: els_a[id_reg].click()
        except: raise Exception('Ошибка клика регион')
        time.sleep(10)  # Здесь долго подтягиваются данные
        
        # Ищем блок ввода адреса
        els_fieldset_addr = driver.find_elements(By.XPATH, '//fieldset[@class="form-1-fieldset addressConnectFs"]')
        if len(els_fieldset_addr) == 0: raise Exception('Ошибка нет блока адреса')
        # Вводим адрес
        # Вводим населенный пункт
        city = data.get('city')
        if city == None: raise Exception('Ошибка Город не задан')
        str_city = city.replace('ё', 'е')
        els = els_fieldset_addr[0].find_elements(By.XPATH, './/input[@data-field="city"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода населенного пункта')
        # Передвинем страницу чтоб элемент стал видимым
        driver.execute_script("arguments[0].scrollIntoView();", els[0])
        time.sleep(1)
        driver.execute_script('window.scrollBy(-100, -200)')  # прокручивает страницу относительно её текущего положения
        time.sleep(1)

        l_tp_st = ordering_string(str_city, city_abbr)  # попробуем распознать тип населенный пункт
        s_city = ''
        t_city = ''
        if len(l_tp_st) == 0:  # не распознали
            t_city = 'г.'
            s_city = city # как есть
        else:
            t_city = city_abbr.get(l_tp_st[0])
            s_city = l_tp_st[1]
        try:
            els[0].send_keys(s_city)
            time.sleep(1)
            els[0].send_keys(Keys.ENTER)
        except: raise Exception('Ошибка ввода населенного пункта')
        time.sleep(3)
        
        # Ищем блок с подсказкой городов
        els_fieldset_addr = driver.find_elements(By.XPATH, '//fieldset[@class="form-1-fieldset addressConnectFs"]')
        if len(els_fieldset_addr) == 0: raise Exception('Ошибка нет блока адреса2')
        els_div = els_fieldset_addr[0].find_elements(By.XPATH, './/div[@class="field-col-in4cols relative-position"]')
        if len(els_div) < 2: raise Exception('Ошибка нет вложенного блока с подсказкой городов')
        els_li = els_div[0].find_elements(By.TAG_NAME, 'li')
        if len(els_li) == 0: raise Exception('Ошибка нет вариантов выбора населенного пункта')
        lst_city = []
        for el in els_li:
            l_c = el.text.split('\n')
            lst_city.append(l_c[0])
        # Поищем по вхождению
        f_city = f'{t_city};{s_city}'
        i_fnd = find_string_to_substrs(lst_city, f_city)
        # возьмем короткое
        i_fnd = find_short(lst_city)
        if i_fnd < 0: raise Exception(f'Ошибка поиск населенного пункта по ключу {f_city}: вариантов нет')
        try:els_li[i_fnd].click()
        except: raise Exception('Ошибка выбора населенного пункта из списка')
        time.sleep(3)
        
        # Вводим улицу
        # преобразование по типу улицы
        street = data.get('street')
        if street == None: raise Exception('Ошибка Улица не задана')
        str_street = street.replace('ё', 'е')
        # Удалим из строки районы и микрорайоны
        str_street = remove_street_exc_abbr(str_street)
        l_tp_st = ordering_string(str_street, street_abbr)  # попробуем распознать тип улицы
        s_street = ''
        t_street = ''
        if len(l_tp_st) == 0:  # не распознали
            t_street = 'ул'
            # t_street = ''
            s_street = str_street # как есть
        else:
            t_street = street_abbr.get(l_tp_st[0])
            s_street = l_tp_st[1]
            
        els_fieldset_addr = driver.find_elements(By.XPATH, '//fieldset[@class="form-1-fieldset addressConnectFs"]')
        if len(els_fieldset_addr) == 0: raise Exception('Ошибка нет блока адреса3')
        els = els_fieldset_addr[0].find_elements(By.XPATH, './/input[@data-field="street"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода улицы')
        
        try:
            els[0].send_keys(s_street)
            time.sleep(1)
            els[0].send_keys(Keys.ENTER)
        except: raise Exception('Ошибка ввода улицы')
        time.sleep(3)
        
        # Ищем блок с подсказкой улиц
        els_fieldset_addr = driver.find_elements(By.XPATH, '//fieldset[@class="form-1-fieldset addressConnectFs"]')
        if len(els_fieldset_addr) == 0: raise Exception('Ошибка нет блока адреса4')
        els_div = els_fieldset_addr[0].find_elements(By.XPATH, './/div[@class="field-col-in4cols relative-position"]')
        if len(els_div) < 2: raise Exception('Ошибка нет вложенного блока с подсказкой улиц')
        els_li = els_div[1].find_elements(By.TAG_NAME, 'li')
        if len(els_li) == 0: raise Exception('Ошибка нет вариантов выбора улиц')
        # Собираем список подсказок
        lst_street = []
        for el in els_li:
            l_c = el.text.split('\n')
            lst_street.append(l_c[0])
        # Поищем по вхождению город, тип и улице
        f_street = f'{s_city};{t_street} {s_street}'
        i_fnd = find_string_to_substrs(lst_street, f_street)
        if i_fnd < 0:
            # Пробуем просто по типу и улице
            f_street = f'{t_street};{s_street}'
            i_fnd = find_string_to_substrs(lst_street, f_street)
        
        if i_fnd < 0: raise Exception(f'Ошибка поиск улицы по ключу {f_street}: вариантов нет')
        # Пробежим по списку подсказки
        try:
            for _ in range(i_fnd):
                els[0].send_keys(Keys.ARROW_DOWN)
                time.sleep(0.2)
            time.sleep(0.2)
            els[0].send_keys(Keys.ENTER)
        except: raise Exception('Ошибка выбора улицы из списка')
        time.sleep(3)
        
        # Вводим дом
        house = data.get('house')
        if house == None: raise Exception('Ошибка Дом не задан')
        c_house = ordering_house(house)
        if c_house[0] == '': raise Exception(f'Ошибка: Номер дома {house} не распознан.')

        els_fieldset_addr = driver.find_elements(By.XPATH, '//fieldset[@class="form-1-fieldset addressConnectFs"]')
        if len(els_fieldset_addr) == 0: raise Exception('Ошибка нет блока адреса4')
        els = els_fieldset_addr[0].find_elements(By.XPATH, './/input[@data-field="house"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода дома')
        try:
            els[0].send_keys(c_house[0])
            time.sleep(1)
            els[0].send_keys(Keys.ENTER)
        except: raise Exception('Ошибка ввода дома')
        time.sleep(5)
        
        # Ищем блок с подсказкой домов
        els_fieldset_addr = driver.find_elements(By.XPATH, '//fieldset[@class="form-1-fieldset addressConnectFs"]')
        if len(els_fieldset_addr) == 0: raise Exception('Ошибка нет блока адреса5')
        els_div = els_fieldset_addr[0].find_elements(By.XPATH, './/div[@class="field-col-in2cols relative-position"]')
        if len(els_div) != 1: raise Exception('Ошибка нет списка вариантов домов')
        els_li = els_div[0].find_elements(By.TAG_NAME, 'li')
        if len(els_li) == 0: raise Exception('Ошибка нет вариантов выбора домов')
        # Собираем список подсказок
        lst_house = []
        for el in els_li:
            lst_house.append(el.text)
        # Поищем по вхождению
        i_fnd = find_string_to_listsubstrs(lst_house, c_house[1])
        
        if i_fnd < 0: raise Exception(f'Ошибка поиск дома по номеру {house}: вариантов нет')
        # Пробежим по списку подсказки
        try:
            for _ in range(i_fnd):
                els[0].send_keys(Keys.ARROW_DOWN)
                time.sleep(0.2)
            time.sleep(0.2)
            els[0].send_keys(Keys.ENTER)
        except: raise Exception('Ошибка выбора дома из списка')
        time.sleep(3)
        
        # Вводим квартиру
        apartment = data.get('apartment')
        if apartment:
            els_fieldset_addr = driver.find_elements(By.XPATH, '//fieldset[@class="form-1-fieldset addressConnectFs"]')
            if len(els_fieldset_addr) == 0: raise Exception('Ошибка нет блока адреса5')
            els = els_fieldset_addr[0].find_elements(By.XPATH, './/input[@data-field="flat"]')
            if len(els) != 1: raise Exception('Ошибка нет поля ввода квартиры')
            try: els[0].send_keys(apartment)
            except: raise Exception('Ошибка ввода квартиры')
            time.sleep(1)
        time.sleep(3)

        # Возьмем определившийся адрес
        data['pv_address'] = ''
        driver.implicitly_wait(2)
        els_div_adr = driver.find_elements(By.XPATH, '//div[@id="addresse-form"]')
        if els_div_adr[0]:
            els_adr = els_div_adr[0].find_elements(By.XPATH, './/span[@class="fullAddress"]')
            if els_adr[0]: data['pv_address'] = els_adr[0].text
        driver.implicitly_wait(10)
        time.sleep(3)
        
        # Нажимаем кнопку проверить техническую возможность
        els = driver.find_elements(By.XPATH, '//input[@name="checkConnPosibility"]')
        if len(els) != 1: raise Exception('Ошибка нет кнопки проверить техническую возможность')
        try: els[0].click()
        except: raise Exception('Ошибка нажатия кнопки проверить техническую возможность')
        time.sleep(1)
        
        wait_spinner(driver)  # Подождем если есть спинер

        # Смотрим таблицу результатов проверки технической возможности
        els = driver.find_elements(By.XPATH, '//tbody[@id="recievedTpTableBody"]')
        if len(els) != 1: raise Exception('Ошибка нет таблицы результатов проверки технической возможности')
        # service_dict = {}
            # 'Домашний интернет': (0, OTT)
            # 'Интерактивное ТВ': (0, FTTx)
            # 'Домашний телефон': (0, xDSL)

        els_tr = els[0].find_elements(By.TAG_NAME, 'tr')
        if len(els_tr) == 0: raise Exception('Ошибка нет списка доступных услуг')
        data['available_connect'] = ''
        for el_tr in els_tr:
            els_td = el_tr.find_elements(By.TAG_NAME, 'td')
            row_str = ''
            for el_td in els_td:
                row_str += f'{el_td.text} '
            data['available_connect'] += f'{row_str}\n'
        # Тарифные планы не собираем потому как эже скрипт работает больше 2 мин. (2,07) 
        
        # # Страница возможно сдвинулась, прокрутим страницу вниз
        # driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        # time.sleep(1)

        
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
        # 'login': 'sz_v_an',
        # 'password': 'gBLnFexH6d1~vCZHRVEt3E',
        'id_lid': '1215557',

        'region': 'Ярославль',
        'city': 'Ярославль',
        'street': 'Светлая',
        'house': '38',
        'apartment': '3',
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

    # HELP: https://dev.1c-bitrix.ru/rest_help/crm/leads
    
    available_connect = txv_dict.get('available_connect')
    
    '''
        Алексей, по боту РТК ТхВ

        Когда бот проверяет ТХВ, добавить в конце проверку. 
        Если в результате есть строка "Есть ТхВ" (или как там пишет ртк), то:

        Смотрим статус лида через rest. 
        Если статус лида id 77 (Новые (Нет ТхВ РТК))
        Меняем статус на id 72 (Новые (РТК))
    '''
    # Проверим статус лида
    upgrade_status = False
    if available_connect.find('Есть ТхВ') >= 0:
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
    
    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.update'
    
    restrictions = ''
    error_message = txv_dict.get('bot_log')
    if error_message: restrictions += f'{error_message}\n'
    
    pv_address = txv_dict.get('pv_address')
    if pv_address: restrictions += f'{opsos} определил адрес как: {pv_address}\n'
    
    if available_connect: restrictions += f'Возможность подключения: {available_connect}\n'
    
    params = {
        'id': txv_dict.get('id_lid'),
        'fields[UF_CRM_1638779781554][]': restrictions[:500],  # вся инфа
    }
    up_status = ''
    if upgrade_status:
        params['fields[STATUS_ID]'] = '72'
        up_status = 'Статус обновлен.'
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

def run_txv_rostelecom(tlg_chat, tlg_token):
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
        time.sleep(1)
    #================================================


if __name__ == '__main__':
    # личный бот @infra     TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
    TELEGRAM_CHAT_ID = '1740645090'
    TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

    # общий канал бот @Domconnect_bot Автозаявки        BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN
    BID_TELEGRAM_CHAT_ID = '-1001646764735'
    BID_TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'
    
    
    # start_time = datetime.now()
    
    
    # run_txv_rostelecom(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
    
    
    # url: https://eissd.rt.ru/login
    # login: sz_v_an
    # password: m~|HqEu~VB}|P1QDrDX%

    
    # txv_dict = {
        # # 'login': 'sz_v_an',
        # # 'password': 'm~|HqEu~VB}|P1QDrDX%',
        # 'login': 'sz_v_an',
        # 'password': 'm~|HqEu~VB}|P1QDrDX%',
        # 'id_lid': '1215557',
        
        # # 'region': 'Республика Северная Осетия — Алания',
        # # 'city': 'Владикавказ',
        # # 'street': 'Братьев Темировых',
        # # 'house': '69/4',          # дом
        # # 'apartment': '255',          # квартира
        
        # # 'region': 'Республика Алтай',
        # # 'city': 'Горно-Алтайск',
        # # 'street': 'Проточная улица',
        # # 'house': '10/1к2',          # дом
        # # 'apartment': '10',          # квартира
        
        # # 'region': 'Приморский край',
        # # 'city': 'Владивосток',
        # # 'street': 'Гульбиновича',
        # # 'house': '29/2',          # дом
        # # 'apartment': '40',          # квартира
        
        # # 'region': 'Республика Марий Эл',
        # # 'city': 'Йошкар-Ола',
        # # 'street': 'Машиностроителей',
        # # 'house': '4А',          # дом
        # # 'apartment': '2',          # квартира
        
        # # 'region': 'Республика Алтай',
        # # 'city': 'село Усть-Кокса',
        # # 'street': 'Ленина',
        # # 'house': '20А',          # дом
        # # 'apartment': '10',          # квартира
        
        # # 'region': 'Ростовская область',         # область или город областного значения
        # # 'city': 'Ростов-на-Дону',           # город
        # # 'street': 'садовое товарищество Садовод-Любитель, 2-й Хлопковый переулок',         # улица
        # # 'house': '12',          # дом
        # # 'apartment': '10',          # квартира
        
        # 'region': 'Ярославская область',         # область или город областного значения
        # 'city': 'Ярославль',           # город
        # 'street': 'улица Труфанова',         # улица
        # 'house': '29 корп 2',          # дом
        # 'apartment': '63',          # квартира

        # 'available_connect': '',  # Возможность подключения
        # 'tarifs_all': '', # список названий тарифных планов
        # 'pv_address': '',
    # }
    
    # e, data = get_txv(txv_dict)
    # if e: print(e)
    
    # print('pv_address:', data['pv_address'])
    # print('available_connect:')
    # print(data['available_connect'])
    
    # s = remove_street_exc_abbr(txv_dict['street'])
    # print(find_regions(oblasti, regions, txv_dict['region']))
    
    
    # set_txv_to_dj_domconnect(pv_code)
    # rez, txv_list = get_txv_in_dj_domconnect(pv_code)
    # for txv_dict in txv_list:
        # for k, v in txv_dict.items():
            # print(k, v)


    # data = {'id': 1, 'pv_address': '55632145', 'bot_log': 'Заявка принята МТС'}
    # r = set_txv_status(0, data)
    # print(r)


    # houses = ['14', '30А', '31/41', '30 корп 3', '30 корп3', '12 лит А(АД)', '30 лит 3', '30 стр. 3', '31/41корп2', '31/41 корп2', '31/41 корп 2', '1', '205', 'й']
    # # for h in houses:
        # # rez = ordering_house(h)
        # # print(rez)
    # i_fnd = find_string_to_listsubstrs(houses, ['41', '31', '2'])
    # print(i_fnd)
        
    # end_time = datetime.now()
    # time_str = '\nDuration: {}'.format(end_time - start_time)
    # print(time_str)
    # limit_request_line
    pass

