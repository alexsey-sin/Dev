import os
import time
from datetime import datetime
import requests  # pip install requests
import json
from selenium import webdriver  # $ pip install selenium
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'


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

def find_regions(lst: list, regs: list, in_str: str):  # Поиск вхождения фразы в списке фраз
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
    
    # поиск с циклом по набиранию подстроки
    for i_s in range(len(in_str)):
        sub_str = in_str[0:i_s+1]
        cnt_phr = 0
        # просмотрим список на вхождение
        for i_lst in range(len(lst)):
            if lst[i_lst][0].find(sub_str) >= 0:
                cnt_phr += 1
                ret_id = i_lst
        if cnt_phr > 1:
            ret_id = -1
        else:
            break
    
    if ret_id >= 0:
        id_group = lst[ret_id][1]
        id_reg = lst[ret_id][2]
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
    
def get_abbreviation_street(type_street: str):  # Поиск аббревиатуры по типу улицы
    type_abbr = {
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
    return type_abbr.get(type_street)

# =========================================================
def set_bid(data):  # Заведение заявки
    driver = None
    try:
        base_url = 'https://eissd.rt.ru/login'
        
        EXE_PATH = 'driver/chromedriver.exe'
        driver = webdriver.Chrome(executable_path=EXE_PATH)
        # s = Service(ChromeDriverManager().install())
        # driver = webdriver.Chrome(service=s)

        driver.implicitly_wait(20)
        driver.get(base_url)
        time.sleep(3)
        
        # ###################### Login ######################
        els = driver.find_elements(By.XPATH, '//input[@data-field="login"]')
        if els[0]: els[0].send_keys(data['login'])
        else: raise Exception('Ошибка авторизации нет поля логин')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@data-field="passw"]')
        if els[0]: els[0].send_keys(data['password'])
        else: raise Exception('Ошибка авторизации нет поля пароль')
        time.sleep(2)

        els = driver.find_elements(By.XPATH, '//input[@data-field="closeOthers"]')
        # Обычным способом чекбокс не отмечается - element not interactable
        if els[0]: driver.execute_script("arguments[0].click();", els[0])
        else: raise Exception('Ошибка авторизации нет чекбокса закрыть другие сессии')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@value="Войти"]')
        if els[0]: els[0].click()
        else: raise Exception('Ошибка авторизации нет кнопки Войти')
        time.sleep(5)
        ###################### Главная страница ######################
        els = driver.find_elements(By.XPATH, '//a[@href="/order/phys/edit"]')
        if len(els) < 2: raise Exception('Нет ссылки Создать заявку ФЛ')
        els[1].click()
        time.sleep(3)
        ###################### Страница ввода заявки ######################
        # проверим всплывашки с рекламой
        driver.implicitly_wait(2)
        els = driver.find_elements(By.XPATH, '//div[@class="ju-popup ju-message user-messages-popup "]')
        for el in els:
            els_btn = el.find_elements(By.TAG_NAME, 'input')
            driver.execute_script("arguments[0].click();", els_btn[0])
            time.sleep(1)

        driver.implicitly_wait(20)
        # Выбираем регион
        els = driver.find_elements(By.XPATH, '//input[@data-field="regionName"]')
        if els[0]: els[0].click()
        else: raise Exception('Ошибка нет поля регион')
        time.sleep(1)
        # Блок регионов
        els_block = driver.find_elements(By.XPATH, '//ul[@class="itemlist-0-0 treeview"]')
        if len(els_block) == 0: raise Exception('Ошибка нет блока регионов')
        
        id_group, id_reg, id_code = find_regions(oblasti, regions, data['region'])
        if id_group < 0: raise Exception('Ошибка Регион не найден')
        # Блок групп
        els_span = els_block[0].find_elements(By.TAG_NAME, 'span')
        if len(els_span) != 8: raise Exception('Ошибка неверное колличество регионов в списке')
        els_span[id_group].click()
        time.sleep(1)
        # Подтянулся список областей
        ul_class_path = f'./*//ul[@class="itemlist-1-{id_code} treeview"]'
        els_ul = els_block[0].find_elements(By.XPATH, ul_class_path)
        if len(els_ul) != 1: raise Exception('Ошибка нет вложенного списка областей')
        els_a = els_ul[0].find_elements(By.TAG_NAME, 'a')
        els_a[id_reg].click()
        time.sleep(5)  # Здесь долго подтягиваются данные
        
        # Вводим контактную информацию
        firstname = data['firstname']
        if firstname == None or len(firstname) < 2: firstname = 'Имя'
        lastname = data['lastname']
        if lastname == None or len(lastname) < 2: lastname = 'Фамилия'
        patronymic = data['patronymic']

        els = driver.find_elements(By.XPATH, '//input[@data-field="contact-lastname"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода фамилии')
        els[0].send_keys(lastname)
        time.sleep(1)
        els = driver.find_elements(By.XPATH, '//input[@data-field="contact-firstname"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода имени')
        els[0].send_keys(firstname)
        time.sleep(1)
        if patronymic:
            els = driver.find_elements(By.XPATH, '//input[@data-field="contact-middlename"]')
            if len(els) != 1: raise Exception('Ошибка нет поля ввода отчества')
            els[0].send_keys(patronymic)
            time.sleep(1)
        
        # Вводим телефон
        els = driver.find_elements(By.XPATH, '//input[@data-field="cell-phone"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода телефона')
        els[0].send_keys(data['phone'][1:])
        time.sleep(1)

        # Вводим доп. информацию
        comment = f'Клиент: {data["lastname"]} {data["firstname"]} {data["patronymic"]}\n'
        comment += f'Адрес: {data["region"]}, {data["city"]}, {data["street"]} д.{data["house"]} кв.{data["apartment"]}\n'
        comment += f'Телефон: {data["phone"]}\n'
        # comment += f'Услуга: {data["service"]}\n'
        comment += f'{data["comment"]}\n'
        els = driver.find_elements(By.XPATH, '//textarea[@data-field="additional-info"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода комментария')
        els[0].send_keys(comment)
        time.sleep(1)

        # Страница возможно сдвинулась и верхняя кнопка не видна, прокрутим страницу вниз
        driver.execute_script('window.scrollTo(-500, 500)')
        time.sleep(1)

        # Копируем контактную информацию в персональные данные
        els = driver.find_elements(By.XPATH, '//span[@class="btn-rel-action copyContactInfo hidePersonInfo-order"]')
        if len(els) != 1: raise Exception('Ошибка нет ссылки копирования')
        els[0].click()
        time.sleep(1)
        
        # Вводим адрес
        # Вводим населенный пункт
        els = driver.find_elements(By.XPATH, '//input[@data-field="city"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода населенного пункта')
        # Передвинем страницу чтоб элемент стал видимым
        driver.execute_script("arguments[0].scrollIntoView();", els[0])
        time.sleep(1)
        driver.execute_script('window.scrollBy(-100, -100)')  # прокручивает страницу относительно её текущего положения
        time.sleep(1)
        els[0].send_keys(data["city"])
        els[0].send_keys(Keys.ENTER)
        time.sleep(3)
        
        # Ищем блок с подсказкой городов
        els = driver.find_elements(By.XPATH, '//fieldset[@class="form-1-fieldset addressConnectFs"]')
        if len(els) != 1: raise Exception('Ошибка нет блока с подсказкой городов')
        els_div = els[0].find_elements(By.XPATH, './/div[@class="field-col-in4cols relative-position"]')
        if len(els_div) < 2: raise Exception('Ошибка нет вложенного блока с подсказкой городов')
        els_li = els_div[0].find_elements(By.TAG_NAME, 'li')
        if len(els_li) == 0: raise Exception('Ошибка нет вариантов выбора населенного пункта')
        time.sleep(3)
        
        # Вводим улицу
        # преобразование по типу улицы
        str_street = data['street'].replace('ё', 'е')
        l_tp_st = ordering_street(str_street)  # попробуем распознать тип улицы
        s_street = ''
        t_street = ''
        if len(l_tp_st) == 0:  # не распознали
            t_street = 'ул.'
            s_street = str_street # как есть
        else:
            t_street = get_abbreviation_street(l_tp_st[0])
            s_street = l_tp_st[1]
            
        els = driver.find_elements(By.XPATH, '//input[@data-field="street"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода улицы')
        
        els[0].send_keys(s_street)
        els[0].send_keys(Keys.ENTER)
        time.sleep(3)
        
        # Ищем блок с подсказкой улиц
        els_li = els_div[1].find_elements(By.TAG_NAME, 'li')
        if len(els_li) == 0: raise Exception('Ошибка нет вариантов выбора улиц')
        # Собираем список подсказок
        lst_street = []
        for el in els_li:
            lst_street.append(el.text)
        # Поищем по вхождению
        f_street = f'{data["city"]};{t_street} {s_street}'
        
        i_fnd = find_string_to_substrs(lst_street, f_street)
        if i_fnd < 0: raise Exception(f'Ошибка поиск улицы по ключу {f_street}: вариантов нет')
        
        # Пробежим по списку подсказки
        for _ in range(i_fnd):
            els[0].send_keys(Keys.ARROW_DOWN)
            time.sleep(0.2)
        time.sleep(0.2)
        els[0].send_keys(Keys.ENTER)
        time.sleep(1)
        
        # Вводим дом
        els = driver.find_elements(By.XPATH, '//input[@data-field="house"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода дома')
        els[0].send_keys(data["house"])
        # els[0].send_keys(Keys.ENTER)
        time.sleep(1)
        
        # Вводим квартиры
        els = driver.find_elements(By.XPATH, '//input[@data-field="flat"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода квартиры')
        els[0].send_keys(data["apartment"])
        # els[0].send_keys(Keys.ENTER)
        time.sleep(1)
        
        # Страница возможно сдвинулась и верхняя кнопка не видна, прокрутим страницу вниз
        driver.execute_script('window.scrollTo(0, 1000)')
        time.sleep(1)

        # Нажимаем кнопку проверить техническую возможность
        els = driver.find_elements(By.XPATH, '//input[@name="checkConnPosibility"]')
        if len(els) != 1: raise Exception('Ошибка нет кнопки проверить техническую возможность')
        els[0].click()
        time.sleep(5)

        # Смотрим таблицу результатов проверки технической возможности
        els = driver.find_elements(By.XPATH, '//tbody[@id="recievedTpTableBody"]')
        if len(els) != 1: raise Exception('Ошибка нет таблицы результатов проверки технической возможности')
        service_dict = {}
            # 'Домашний интернет': (0, OTT)
            # 'Интерактивное ТВ': (0, FTTx)
            # 'Домашний телефон': (0, xDSL)

        els_tr = els[0].find_elements(By.TAG_NAME, 'tr')
        if len(els_tr) == 0: raise Exception('Ошибка нет списка доступных услуг')
        for el_tr in els_tr:
            els_td = el_tr.find_elements(By.TAG_NAME, 'td')
            if els_td[2].text == 'Нет ТхВ': rez = 0
            else: rez = 1
            service_dict[els_td[0].text] = (rez, els_td[1].text)
        
        # print(service_dict) # {'Wink-ТВ-онлайн': (0, 'OTT'), 'Домашний телефон': (1, 'Не определена'), 'Домашний интернет': (1, 'Не определена'), 'Интерактивное ТВ': (1, 'Не определена')}
        
        # Страница возможно сдвинулась, прокрутим страницу вниз
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(1)

        # Ищем блок Подключаемые услуги
        els = driver.find_elements(By.XPATH, '//div[@id="blockServiceChange"]')
        if len(els) != 1: raise Exception('Ошибка нет блока Подключаемые услуги')
        el_con_serv = els[0]
        # Отмечаем чекбоксы Подключаемые услуги
        service_hi = 0
        service_sh = 0
        service_si = 0
        service_itv = 0
        service_wtv = 0
        service_hp = 0
        service_mc = 0
        
        if data['service_home_internet']:
            serv = service_dict.get('Домашний интернет')
            if serv and serv[0] == 1:
                els_ch = el_con_serv.find_elements(By.XPATH, './/input[@name="internetCb"]')
                if len(els_ch) != 1: raise Exception('Ошибка нет галки Домашний интернет')
                # Обычным способом чекбокс не отмечается - element not interactable
                driver.execute_script("arguments[0].click();", els_ch[0])
                service_hi = 1
                time.sleep(1)
            else: raise Exception('По услуге Домашний интернет нет ТхВ')
        if data['service_smart_house']:
            serv = service_dict.get('Умный дом')
            if serv and serv[0] == 1:
                els_ch = el_con_serv.find_elements(By.XPATH, './/input[@name="smarthouseCb"]')
                if len(els_ch) != 1: raise Exception('Ошибка нет галки Умный дом')
                # Обычным способом чекбокс не отмечается - element not interactable
                driver.execute_script("arguments[0].click();", els_ch[0])
                service_sh = 1
                time.sleep(1)
            else: raise Exception('По услуге Умный дом нет ТхВ')
        if data['service_smart_intercom']:
            serv = service_dict.get('Умный Домофон')
            if serv and serv[0] == 1:
                els_ch = el_con_serv.find_elements(By.XPATH, './/input[@name="typedServiceCb1041"]')
                if len(els_ch) != 1: raise Exception('Ошибка нет галки Умный Домофон')
                # Обычным способом чекбокс не отмечается - element not interactable
                driver.execute_script("arguments[0].click();", els_ch[0])
                service_si = 1
                time.sleep(1)
            else: raise Exception('По услуге Умный Домофон нет ТхВ')
        if data['service_interactive_tv']:
            serv = service_dict.get('Интерактивное ТВ')
            if serv and serv[0] == 1:
                els_ch = el_con_serv.find_elements(By.XPATH, './/input[@name="iptvCb"]')
                if len(els_ch) != 1: raise Exception('Ошибка нет галки Интерактивное ТВ')
                # Обычным способом чекбокс не отмечается - element not interactable
                driver.execute_script("arguments[0].click();", els_ch[0])
                service_itv = 1
                time.sleep(1)
            else: raise Exception('По услуге Интерактивное ТВ нет ТхВ')
        if data['service_wink_tv_online']:
            serv = service_dict.get('Wink-ТВ-онлайн')
            if serv and serv[0] == 1:
                els_ch = el_con_serv.find_elements(By.XPATH, './/input[@name="winkCb"]')
                if len(els_ch) != 1: raise Exception('Ошибка нет галки Wink-ТВ-онлайн')
                # Обычным способом чекбокс не отмечается - element not interactable
                driver.execute_script("arguments[0].click();", els_ch[0])
                service_wtv = 1
                time.sleep(1)
            else: raise Exception('По услуге Wink-ТВ-онлайн нет ТхВ')
        if data['service_home_phone']:
            serv = service_dict.get('Домашний телефон')
            if serv and serv[0] == 1:
                els_ch = el_con_serv.find_elements(By.XPATH, './/input[@name="phoneCb"]')
                if len(els_ch) != 1: raise Exception('Ошибка нет галки Домашний телефон')
                # Обычным способом чекбокс не отмечается - element not interactable
                driver.execute_script("arguments[0].click();", els_ch[0])
                service_hp = 1
                time.sleep(1)
            else: raise Exception('По услуге Домашний телефон нет ТхВ')
        if data['service_mobile_connection']:
            serv = service_dict.get('Мобильная связь')
            if serv and serv[0] == 1:
                els_ch = el_con_serv.find_elements(By.XPATH, './/input[@name="mobileCb"]')
                if len(els_ch) != 1: raise Exception('Ошибка нет галки Мобильная связь')
                # Обычным способом чекбокс не отмечается - element not interactable
                driver.execute_script("arguments[0].click();", els_ch[0])
                service_mc = 1
                time.sleep(1)
            else: raise Exception('По услуге Мобильная связь нет ТхВ')
        
        if service_mc + service_sh + service_si + service_itv + service_wtv + service_hp + service_mc == 0:
            if data['general_package']:
                raise Exception('Ошибка при выборе общих пакетных предложений нужно отметить хотя бы одну услугу (любой символ в названии тарифа)')
            else:
                raise Exception('Ошибка не выбрана услуга')
        
        # Общие пакетные предложения
        if data['general_package']:
            time.sleep(3)
            # Если есть общее пакетное предложение - сбрасываем флаги выбора тарифов по услугам
            service_hi = 0
            service_sh = 0
            service_si = 0
            service_itv = 0
            service_wtv = 0
            service_hp = 0
            service_mc = 0
            
            els_all = driver.find_elements(By.XPATH, '//select[@data-field="packetTariffs"]')
            if len(els_all) != 1: raise Exception('Ошибка нет блока общих пакетных предложений')
            els_opt = els_all[0].find_elements(By.TAG_NAME, 'option')
            if len(els_opt) == 0: raise Exception('Ошибка нет общих пакетных предложений')
          
            l_fnd = []  # Составим список предложений
            for el_opt in els_opt:
                l_fnd.append(el_opt.text)
            i_fnd = find_string_to_substrs(l_fnd, data['general_package'])
            if i_fnd < 0: raise Exception(f'Ошибка пакетное предложение \"{data["general_package"]}\" нет в списке.')
            els_opt[i_fnd].click()
            time.sleep(2)
            
        # ждем появления блока по услуге
        time.sleep(3)

        if service_hi:  # Домашний интернет
            els = driver.find_elements(By.XPATH, '//div[@class="col-2-1 internetDisabledOrder internetOrderChangeable"]')
            if len(els) != 1: raise Exception('Ошибка нет блока Домашний интернет')

            # Передвинем страницу чтоб элемент стал видимым
            driver.execute_script("arguments[0].scrollIntoView();", els[0])
            driver.execute_script('window.scrollBy(-100, -100)')  # прокручивает страницу относительно её текущего положения
            time.sleep(2)

            els_offer = els[0].find_elements(By.XPATH, './/select[@data-field="internetTariffs"]')
            if len(els_offer) != 1: raise Exception('Ошибка нет блока предложений тарифов Домашний интернет')
            els_opt = els_offer[0].find_elements(By.TAG_NAME, 'option')
            if len(els_opt) == 0: raise Exception('Ошибка нет предложений тарифов Домашний интернет')

            l_fnd = []  # Составим список предложений
            for el_opt in els_opt:
                l_fnd.append(el_opt.text)
            i_fnd = find_string_to_substrs(l_fnd, data['service_home_internet'])
            if i_fnd < 0: raise Exception(f'Ошибка тариф {data["service_home_internet"]} в списке не найден.')
            els_opt[i_fnd].click()

            # ждем прогрузки
            time.sleep(7)
                
            # Вводим технологию подключения
            els_tech_conn = els[0].find_elements(By.XPATH, './/select[@data-field="internetTechnology"]')
            if len(els_tech_conn) != 1: raise Exception('Ошибка нет блока технологий подключений Домашний интернет')
            els_opt = els_tech_conn[0].find_elements(By.TAG_NAME, 'option')
            if len(els_opt) == 0: raise Exception('Ошибка нет предложений технологий подключений Домашний интернет')
            avail_conn = service_dict['Домашний интернет'][1]
            conn = False
            lst_conn = []
            # Составим список предлагаемых технологий и сразу сравним с тех. вожможностью
            for el_opt in els_opt:
                lst_conn.append(el_opt.text)
                if el_opt.text.lower().strip() == avail_conn.lower().strip():
                    el_opt.click()
                    conn = True
                    break
            if conn == False:
                for i in range(len(lst_conn)):
                    if lst_conn[i] == 'FTTx':
                        els_opt[i].click()
                        conn = True
                        break
            if conn == False:
                if len(lst_conn) < 2: raise Exception('Ошибка нет возможных технологий подключения Домашний интернет')
                else:
                    els_opt[1].click()
            time.sleep(3)
            
            # Смотрим список доп услуг
            els_div = driver.find_elements(By.XPATH, '//div[@id="internetOptions"]')
            if len(els_div) != 1: raise Exception('Нет блока опций Домашний интернет')
            
            # Проход по строкам
            els_tr = els_div[0].find_elements(By.TAG_NAME, 'tr')
            driver.implicitly_wait(1)
            for el_tr in els_tr:
                els_td = el_tr.find_elements(By.TAG_NAME, 'td')
                if len(els_td) < 3: continue
                el_td = els_td[0]
                # Смотрим есть ли блок с отмеченным флажком
                els_div_ch = el_td.find_elements(By.XPATH, './/div[@class="fs-checkbox  fs-checkbox-checked fs-touch-element"]')
                if els_div_ch and len(els_div_ch) > 0:
                    els_input = el_td.find_elements(By.TAG_NAME, 'input')
                    for el_input in els_input:
                        try: el_input.click()
                        except: pass
                        try: driver.execute_script("arguments[0].click();", el_input)
                        except: pass
                        time.sleep(1)
            driver.implicitly_wait(20)
        
        if service_itv:  # Интерактивное ТВ
            els = driver.find_elements(By.XPATH, '//div[@class="units-row iptvDisabledOrder iptvOrderChangeable"]')
            if len(els) != 1: raise Exception('Ошибка нет блока Интерактивное ТВ')

            # Передвинем страницу чтоб элемент стал видимым
            driver.execute_script("arguments[0].scrollIntoView();", els[0])
            driver.execute_script('window.scrollBy(-100, -100)')  # прокручивает страницу относительно её текущего положения
            time.sleep(2)

            els_offer = els[0].find_elements(By.XPATH, './/select[@data-field="iptvTariffs"]')
            if len(els_offer) != 1: raise Exception('Ошибка нет блока предложений тарифов Интерактивное ТВ')
            els_opt = els_offer[0].find_elements(By.TAG_NAME, 'option')
            if len(els_opt) == 0: raise Exception('Ошибка нет предложений тарифов Интерактивное ТВ')

            l_fnd = []  # Составим список предложений
            for el_opt in els_opt:
                l_fnd.append(el_opt.text)
            i_fnd = find_string_to_substrs(l_fnd, data['service_interactive_tv'])
            if i_fnd < 0: raise Exception(f'Ошибка тариф {data["service_interactive_tv"]} в списке не найден.')
            els_opt[i_fnd].click()

            # ждем прогрузки
            time.sleep(5)

            # Вводим технологию подключения
            els_tech_conn = els[0].find_elements(By.XPATH, './/select[@data-field="iptvTechnology"]')
            if len(els_tech_conn) != 1: raise Exception('Ошибка нет блока технологий подключений Интерактивное ТВ')
            
            els_opt = els_tech_conn[0].find_elements(By.TAG_NAME, 'option')
            if len(els_opt) == 0: raise Exception('Ошибка нет предложений технологий подключений Интерактивное ТВ')
            avail_conn = service_dict['Интерактивное ТВ'][1]
            conn = False
            lst_conn = []
            # Составим список предлагаемых технологий и сразу сравним с тех. вожможностью
            for el_opt in els_opt:
                lst_conn.append(el_opt.text)
                if el_opt.text.lower().strip() == avail_conn.lower().strip():
                    el_opt.click()
                    conn = True
                    break
            
            if conn == False:
                for i in range(len(lst_conn)):
                    if lst_conn[i] == 'FTTx':
                        els_opt[i].click()
                        conn = True
                        break
            if conn == False:
                if len(lst_conn) < 2: raise Exception('Ошибка нет возможных технологий подключения Интерактивное ТВ')
                else:
                    els_opt[1].click()
            time.sleep(3)

            # Выбираем пакеты телеканалов
            packet = data.get('service_iptv_packets')
            if packet == None: raise Exception('Ошибка не задан пакет телеканалов Интерактивное ТВ (service_iptv_packets)')
            els_div_pack = driver.find_elements(By.XPATH, '//fieldset[@class="mainPacketsFs bordered"]')
            if len(els_div_pack) != 1: raise Exception('Ошибка нет блока выбора пакета телеканалов Интерактивное ТВ')
            els_inp = els_div_pack[0].find_elements(By.TAG_NAME, 'input')
            if len(els_inp) == 0: raise Exception('Ошибка нет элементов выбора пакета телеканалов Интерактивное ТВ')

            l_fnd = []  # Составим список предложений
            for el_inp in els_inp:
                l_fnd.append(el_inp.get_attribute('option_full_name'))
            i_fnd = find_string_to_substrs(l_fnd, packet)
            if i_fnd < 0: raise Exception(f'Ошибка пакет телеканалов \"{packet}\" не найден.')
            driver.execute_script("arguments[0].click();", els_inp[i_fnd])
            time.sleep(1)

        # Сохранение заявки
        els_save = driver.find_elements(By.XPATH, '//input[@value="Сохранить заявку"]')
        if len(els_save) == 0: raise Exception('Нет кнопки Сохранить заявку')
        # Передвинем страницу чтоб элемент стал видимым
        driver.execute_script("arguments[0].scrollIntoView();", els_save[0])
        time.sleep(2)
        els_save[0].click()
        time.sleep(5)
        
        # Смотрим ответ
        ans = False
        els_div = driver.find_elements(By.XPATH, '//div[@class="content"]')
        for el_div in els_div:
            txt = el_div.text
            if txt.find('успешно сохранена') >= 0:
                lst = txt.split(' ')
                num = lst[1].strip()
                data['bid_number'] = num[1:]
                ans = True
            if txt.find('Дубликат заявки') >= 0: raise Exception(txt)
       
        if ans == False: raise Exception('Не распознан ответ на Сохранить заявку')
        
        # time.sleep(10)
        # # # # data['bid_number'] = '7777777'
        # with open('out.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        
    except Exception as e:
        return str(e)[:100], data
    finally:
        if driver: driver.quit()
    
    return '', data

def set_did_to_dj_domconnect():
    url = url_host + 'api/set_bid_rostelecom'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
        'login': 'sz_v_an',
        'password': '@hgfjdhjhQ54564',
        'id_lid': '1188357',
        'firstname': 'Иван',
        'patronymic': '',
        'lastname': '',
        'phone': '79111234567',
        'region': 'Ярославль',
        'city': 'Ярославль',
        'street': 'Светлая',
        'house': '38',
        'apartment': '3',

        'general_package': '',  # Название общего пакетного предложения     'Fb Техно Общения. PRO К'
        # По услугам: Название предложения по услуге или пусто если не нужна услуга
        'service_home_internet': '',      # Домашний интернет       'Технологии доступа 100 100 Мбит/с'
        'service_smart_house': '',      # Умный дом
        'service_smart_intercom': '',      # Умный домофон
        'service_interactive_tv': '',      # Интерактивное ТВ     'Интерактивное ТВ 2.0'
        'service_wink_tv_online': '',      # Wink-ТВ-онлайн
        'service_home_phone': '',      # Домашний телефон
        'service_mobile_connection': '',      # Мобильная связь

        'service_iptv_packets': 'Продвинутый. ОТТ',      # Пакеты телеканалов Интерактивное ТВ

        'comment': 'Тестовая заявка, просьба не обрабатывать',
    }
    
    try:
        responce = requests.get(url, headers=headers, params=params)
        print(responce.status_code)
        print(responce.text)
    except:
        pass
        print('Error: requests.get')

def get_did_in_dj_domconnect():
    url = url_host + 'api/get_bid_rostelecom'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
    }
    
    try:
        responce = requests.get(url, headers=headers, params=params)
    except:
        return 1, []
    if responce.status_code == 200:
        bid_list = json.loads(responce.text)
        return 0, bid_list
    return 2, []

def set_bid_status(status, data):
    url = url_host + 'api/set_bid_rostelecom_status'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
        'id': data.get('id'),
        'bid_number': data.get('bid_number'),
        'status': status,
    }
    bot_log = data.get('bot_log')
    if bot_log:
        params['bot_log'] = bot_log
    try:
        responce = requests.get(url, headers=headers, params=params)
    except:
        pass

def send_crm_bid(bid_dict):
    user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.update'

    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': user_agent_val,
    }

    number_bid_ctn = f'Заявка: {bid_dict.get("bid_number")}'
    service = ''
    gp = bid_dict.get('general_package')
    if gp:
        sv = []
        if bid_dict.get('service_home_internet'): sv.append('Домашний интернет')
        if bid_dict.get('service_smart_house'): sv.append('Умный дом')
        if bid_dict.get('service_smart_intercom'): sv.append('Умный домофон')
        if bid_dict.get('service_interactive_tv'): sv.append(f'Интерактивное ТВ с пакетом {bid_dict.get("service_iptv_packets")}')
        if bid_dict.get('service_wink_tv_online'): sv.append('Wink-ТВ-онлайн')
        if bid_dict.get('service_home_phone'): sv.append('Домашний телефон')
        if bid_dict.get('service_mobile_connection'): sv.append('Мобильная связь')
        
        service = f'Пакетное предложение {gp} по услугам {",".join(sv)}'
    else:
        if bid_dict.get('service_home_internet'): service += f'Домашний интернет с тарифом {bid_dict.get("service_home_internet")}, '
        if bid_dict.get('service_smart_house'): service += f'Умный дом с тарифом {bid_dict.get("service_smart_house")}, '
        if bid_dict.get('service_smart_intercom'): service += f'Умный домофон с тарифом {bid_dict.get("service_smart_intercom")}, '
        if bid_dict.get('service_interactive_tv'): service += f'Интерактивное ТВ с тарифом {bid_dict.get("service_interactive_tv")} и пакетом {bid_dict.get("service_iptv_packets")}, '
        if bid_dict.get('service_wink_tv_online'): service += f'Wink-ТВ-онлайн с тарифом {bid_dict.get("service_wink_tv_online")}, '
        if bid_dict.get('service_home_phone'): service += f'Домашний телефон с тарифом {bid_dict.get("service_home_phone")}, '
        if bid_dict.get('service_mobile_connection'): service += f'Мобильная связь с тарифом {bid_dict.get("service_mobile_connection")}, '

    params = {
        'id': bid_dict.get('id_lid'),
        'fields[UF_CRM_5864F4DAAC508]': number_bid_ctn,
        'fields[UF_CRM_1493413514]': 3,
        'fields[UF_CRM_5864F4DA85D5A]': service,
        'fields[UF_CRM_1499386906]': 523,  # PartnerWEB
    }
    error_message = bid_dict.get("bot_log")
    if error_message:
        params['fields[UF_CRM_5864F4DAAC508]'] = error_message

    try:
        responce = requests.post(url, headers=headers, params=params)
        # посмотреть результат https://crm.domconnect.ru/crm/lead/details/1188357/
    except:
        pass

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

def run_bid_rostelecom(tlg_chat, tlg_token):
    opsos = 'Ростелесом'
    
    # личный бот @infra
    TELEGRAM_CHAT_ID = '1740645090'
    TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'
    
    rez, bid_list = get_did_in_dj_domconnect()
    if rez:
        tlg_mess = 'Ошибка при загрузке заявок из domconnect.ru'
        r = send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, tlg_mess)
        print(tlg_mess, '\nTelegramMessage:', r)
        return
    if len(bid_list) == 0:
        cur_time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        print(f'{cur_time} {opsos}: Заявок нет')
        return

    # Перелистываем список словарей с заявками
    for bid_dict in bid_list:
        rez, data = set_bid(bid_dict)
        data['bot_log'] = rez
        send_crm_bid(data)  # ответ в CRM
        tlg_mess = ''
        if rez == '':  # заявка успешно создана
            set_bid_status(3, data)
            tlg_mess = f'{opsos}: - создана заявка\n'
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'Номер заявки: {data.get("bid_number")}\n'
        else:  # не прошло
            set_bid_status(2, data)
            tlg_mess = f'{opsos}:\n'
            address = f'{data.get("region")} {data.get("city")} {data.get("street")} д.{data.get("house")} кв.{data.get("apartment")}\n'
            fio = f'{data.get("firstname")} {data.get("patronymic")} {data.get("lastname")}'
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'Логин: {data.get("partner_login")}\n'
            tlg_mess += f'Адрес: {address}\n'
            tlg_mess += f'ФИО: {fio}\n'
            tlg_mess += f'Ошибка: {data.get("bot_log")}\n'
        r = send_telegram(tlg_chat, tlg_token, tlg_mess)
        print(tlg_mess)
        print('TelegramMessage:', r)
    #================================================

if __name__ == '__main__':
    pass
    # set_did_to_dj_domconnect()
    
    # data = {'id': 1,}
    # set_bid_status(3, data)
    
    # rez, bid_list = get_did_in_dj_domconnect()
    # print(bid_list)
    
    # data = {
        # 'login': 'sz_v_an',
        # 'password': '@hgfjdhjhQ54564',
        # 'id_lid': '1188357',
        # 'firstname': 'Иван',
        # 'patronymic': '',
        # 'lastname': '',
        # 'phone': '79111234567',
        
        
        # 'region': 'Ярославль',
        # 'city': 'Ярославль',
        # 'street': 'Светлая',
        
        # # 'region': 'Санкт-Петербург',
        # # 'city': 'Санкт-Петербург',
        # # 'street': 'аллея Котельникова',

        # # 'region': 'Московская область',
        # # 'city': 'Реутов',
        # # 'street': 'улица Победы',

        # # 'region': 'Ярославская область',
        # # 'city': 'Ярославль',
        # # 'street': 'проспект Ленина',
        
        # # 'region': 'Санкт-Петербург',
        # # 'city': 'Санкт-Петербург',
        # # 'street': 'бульвар Красных Зорь',

        # # 'region': 'Московская область',
        # # 'city': 'Орехово-Зуево',
        # # 'street': 'улица Володарского',
		
        # # 'region': 'Ивановская область',
        # # 'city': 'Иваново',
        # # 'street': 'Большая Воробьёвская улица',
        
        # # 'region': 'Саратовская область',
        # # 'city': 'Саратов',
        # # 'street': '3-й Дачный посёлок, улица Мира',


				


        # 'house': '38',
        # 'apartment': '3',

        # # 'general_package': 'Fb ;Техно ; выгоды;',  # Название общего пакетного предложения     'Fb Техно Общения. PRO К'
        # 'general_package': '',  # Название общего пакетного предложения     'Fb Техно Общения. PRO К'
        # # По услугам: Название предложения по услуге или пусто если не нужна услуга
        # 'service_home_internet': 'Технологии; доступа ; 100 Мбит/с',      # Домашний интернет       'Технологии доступа 100 100 Мбит/с'
        # 'service_smart_house': '',      # Умный дом
        # 'service_smart_intercom': '',      # Умный домофон
        # 'service_interactive_tv': 'Интерактивное ;ТВ ;2.0',      # Интерактивное ТВ     'Интерактивное ТВ 2.0'
        # 'service_wink_tv_online': '',      # Wink-ТВ-онлайн
        # 'service_home_phone': '',      # Домашний телефон
        # 'service_mobile_connection': '',      # Мобильная связь

        # 'service_iptv_packets': 'Продвинутый;ОТТ',      # Пакеты телеканалов Интерактивное ТВ

        # 'comment': 'Тестовая заявка, просьба не обрабатывать',
    # }
    # # Санкт-Петербург	Санкт-Петербург	аллея Котельникова

    # rez, data = set_bid(data)
    # if rez: print(rez)
    # # print(data.get('bid_number'))
    
    # reg = 'Ярославль'
    # # find_regions(oblasti, regions, reg)
    # id_group, id_reg, id_code = find_regions(oblasti, regions, reg)

'''

    # https://eissd.rt.ru/login
    # sz_v_an
    # @hgfjdhjhQ54564


    # 79108280465 телефон Евгения
    # # Страница возможно сдвинулась, прокрутим страницу вниз
    # driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    # time.sleep(1)

    # # Выполнение клика мышкой через скрипт
    # driver.execute_script("arguments[0].click();", els_input[0])
    
    # # Передвинем страницу чтоб элемент стал видимым
    # driver.execute_script("arguments[0].scrollIntoView();", els[0])
    # driver.execute_script('window.scrollBy(-500, 0)')  # прокручивает страницу относительно её текущего положения

    # Новый вариант использования selenium webdriver
    
    from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager
    from selenium.webdriver.chrome.service import Service

        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s)

    
    
    Проблема с адресами Воронеж, Ленина (пер. пл. ул.)
    С адресами всплыла проблема. Завожу Ленина, в подсказке первой строкой пер. Ленина (Воронеж) бот её и выбирает
    
    
'''
