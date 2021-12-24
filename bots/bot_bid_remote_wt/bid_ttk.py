import os
import time
import re
from datetime import datetime
import requests  # pip install requests
import json
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager


# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'

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
        (если строка не пустая)
    '''
    l_min = 10000
    i_min = -1
    for i in range(len(f_lst)):
        if len(f_lst[i]) == 0: continue
        l_phr = len(f_lst[i])
        if l_phr < l_min:
            l_min = l_phr
            i_min = i
    return i_min
    
def ordering_street_by_type(in_street: str):  # Преобразование строки улица
    '''
        разбиваем строку по запятым, и каждый фрагмент проверяем на
        изветсный тип улицы
        выдаем название с сокращенным типом улицы
        если известный тип не найден - возвращаем пустую строку
    '''
    type_abbr = {
        'улица': 'ул ',
        'проспект': 'просп ',
        'переулок': 'пер ',
        'шоссе': 'ш ',
        'аллея': 'аллея ',
        'тупик': 'тупик ',
        'проезд': 'пр-д ',
        'набережная': 'наб ',
        'площадь': 'пл ',
        'бульвар': 'б-р ',
    }
    # Преобразуем ё к е
    in_street = in_street.replace('ё', 'е')
    
    out_street = ''
    lst = in_street.split(',')
    for sub in lst:
        rez = False
        for ts in type_abbr.keys():
            if sub.find(ts) >= 0:
                rez = True
                out_street = type_abbr[ts] + sub.replace(ts, '').strip()
                break
        if rez: break
    return out_street

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
    if len(lst_house) > 3: return ('', 'В номере много позиций')
    if len(lst_house) == 2:  # значит буква - склеиваем как 30а
        lst_house[1] = lst_house[1].lower()
        return (lst_house[0], ''.join(lst_house))
    # анализируем  корп, литер
    if lst_house[1].find('к') >= 0:
        lst_house[1] = 'корп'
        return (lst_house[0], ' '.join(lst_house))
    if lst_house[1].find('л') >= 0:
        lst_house[1] = 'лит'
        return (lst_house[0], ' '.join(lst_house))
    
    return ('', 'Номер не распознан')

def is_russian(s: str) -> bool:  # Проверка строки: Можно использовать буквы кириллического алфавита и символы “-” и пробел
    return bool(re.fullmatch(r'(?i)[а-яё -]+', s))

# =========================================================
def set_bid(data):
    driver = None
    try:
        base_url = 'https://onyma-crm.ttk.ru:4443/onyma/'
        
        EXE_PATH = 'driver/chromedriver.exe'
        driver = webdriver.Chrome(executable_path=EXE_PATH)
        # s = Service(ChromeDriverManager().install())
        # driver = webdriver.Chrome(service=s)

        driver.implicitly_wait(10)
        driver.get(base_url)
        time.sleep(3)
        
        ###################### Страница Логин/Пароль ######################
        els = driver.find_elements(By.XPATH, '//input[@id="id_login"]')
        if len(els) != 1: raise Exception('Ошибка: Нет поля логин')
        els[0].send_keys(data.get('login'))
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@id="id_password"]')
        if len(els) != 1: raise Exception('Ошибка: Нет поля пароль')
        els[0].send_keys(data.get('password'))
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//select[@id="id_realm"]')
        if len(els) != 1: raise Exception('Ошибка: Нет поля тип пользователя')
        f_ok = False
        els_opt = els[0].find_elements(By.TAG_NAME, 'option')
        for el_opt in els_opt:
            if el_opt.get_attribute('value') == 'ttk':
                el_opt.click()
                time.sleep(1)
                f_ok = True
        if f_ok == False: raise Exception('Ошибка: Пользователя ТТК нет в списке')

        els = driver.find_elements(By.XPATH, '//input[@type="submit"]')
        if len(els) != 1: raise Exception('Ошибка: Нет кнопки Войти')
        els[0].click()
        time.sleep(3)

        ###################### Страница Сводные панели ######################
        els = driver.find_elements(By.XPATH, '//a[@href="/onyma/dashboard"]')
        if len(els) != 1: raise Exception('Ошибка: Нет ссылки Сводные панели')
        els[0].click()
        time.sleep(3)

        ###################### Страница Адрес ######################
        # Вводим Город
        els_div_city = driver.find_elements(By.XPATH, '//div[@data-ctrl="s$region"]')
        if len(els_div_city) != 1: raise Exception('Ошибка: Нет блока Город')
        els_inp = els_div_city[0].find_elements(By.XPATH, './/input[@class="editbox w-text value-empty"]')
        if len(els_inp) != 1: raise Exception('Ошибка: Нет поля ввода Город')
        city = data.get('city')
        if city == None: raise Exception('Ошибка: Не задано значение Город')
        els_inp[0].click()
        time.sleep(0.2)
        els_inp[0].send_keys(city)
        time.sleep(0.2)
        els_inp[0].send_keys(Keys.ENTER)
        time.sleep(3)
        # Смотрим варианты
        els_div_opt = els_div_city[0].find_elements(By.XPATH, './/div[@class="options"]')
        if len(els_div_opt) != 1: raise Exception('Ошибка: Нет блока подсказок Город')
        els_opt = els_div_opt[0].find_elements(By.TAG_NAME, 'span')
        if len(els_opt) == 0: raise Exception(f'Ошибка: Город \"{city}\" не найден (нет списка вариантов)')
        lst_city = []
        els_inp[0].send_keys(Keys.ARROW_DOWN)
        time.sleep(0.2)
        for el_opt in els_opt:
            if el_opt.text == '': continue
            lst_city.append(el_opt.text)
        i_fnd = find_short(lst_city)
        if i_fnd < 0: raise Exception(f'Ошибка: Город \"{city}\" не найден2 (нет списка вариантов)')
        # Пробежим по списку подсказки
        for _ in range(i_fnd):
            els_inp[0].send_keys(Keys.ARROW_DOWN)
            time.sleep(0.2)
        els_inp[0].send_keys(Keys.ENTER)
        time.sleep(2)
        
        # Вводим Улицу/дом
        els_div_addr = driver.find_elements(By.XPATH, '//div[@data-ctrl="s$addr_ctrl"]')
        if len(els_div_addr) != 1: raise Exception('Ошибка: Нет блока Адрес')
        els_inp = els_div_addr[0].find_elements(By.XPATH, './/input[@class="editbox w-text value-empty"]')
        if len(els_inp) != 1: raise Exception('Ошибка: Нет поля ввода Адрес')
        street = data.get('street')
        if street == None: raise Exception('Ошибка: Не задано значение Улица')
        name_street = ordering_street_by_type(street)
        if name_street == '': name_street = street
        els_inp[0].send_keys(name_street)
        time.sleep(5)
        # Смотрим варианты
        els_div_opt = els_div_addr[0].find_elements(By.XPATH, './/div[@class="option"]')  # здесь их много
        if len(els_div_opt) == 0: raise Exception(f'Ошибка: Улица \"{name_street}\" не определена (нет списка вариантов)')
        lst_addr = []
        f_ok = False
        for el_opt in els_div_opt:
            if el_opt.text == name_street:
                f_ok = True
                el_opt.click()
                time.sleep(2)
                break
        if f_ok == False: raise Exception(f'Ошибка: Улица \"{name_street}\" не найдена')
        # Добавляем дом
        house = data.get('house')
        if house == None: raise Exception('Ошибка: Не задано значение Дом')
        c_house = ordering_house(house)
        if c_house[0] == '': raise Exception(f'Ошибка: Дом \"{house}\" {c_house[1]}')
        str_hs = f', д {c_house[0]}'
        els_inp[0].send_keys(str_hs)
        time.sleep(5)
        # Смотрим варианты
        addr = els_inp[0].get_attribute('value')
        # print('Address:', addr)
        els_div_opt = els_div_addr[0].find_elements(By.XPATH, './/div[@class="option"]')  # здесь их много
        if len(els_div_opt) == 0: raise Exception(f'Ошибка: Дом \"{addr}\" не определен (нет списка вариантов)')
        lst_addr = []
        for el_opt in els_div_opt:
            lst_addr.append(el_opt.text)
        # Проходим по списку, проверяем вхождение полного номера дома и бракуем если есть квартира
        for i in range(len(lst_addr)):
            if lst_addr[i].find(' кв ') >= 0 or lst_addr[i].find(c_house[1]) < 0: lst_addr[i] = ''
        # выберем саму короткую
        i_fnd = find_short(lst_addr)
        if i_fnd < 0: raise Exception(f'Ошибка: Дом \"{addr}\" не определен2 (нет списка вариантов)')
        els_div_opt[i_fnd].click()
        time.sleep(2)
        
        # Добавляем квартиру
        els_add = els_div_addr[0].find_elements(By.XPATH, './/span[@class="do-add cursor-pointer mdi onm-icon-plus mdi-15"]')
        if len(els_add) != 1: raise Exception('Ошибка: Нет кнопки добавить квартиру')
        els_add[0].click()
        time.sleep(1)
        els_app = els_div_addr[0].find_elements(By.XPATH, './/input[@name="prop7100460000000000000001"]')
        if len(els_app) != 1: raise Exception('Ошибка: Нет поля ввести квартиру')
        apartment = data.get('apartment')
        if apartment == None: raise Exception('Ошибка: Не задано значение Квартира')
        els_app[0].send_keys(apartment)
        time.sleep(1)
        els_btn_add = els_div_addr[0].find_elements(By.XPATH, './/input[@value="Добавить"]')
        if len(els_btn_add) != 1: raise Exception('Ошибка: Нет кнопки добавить квартиру')
        els_btn_add[0].click()
        time.sleep(1)
        
        # Жмем кнопку проверить адрес
        els = driver.find_elements(By.XPATH, '//input[@value="Проверить адрес"]')
        if len(els) != 1: raise Exception('Ошибка: Нет кнопки Проверить адрес')
        els[0].click()
        time.sleep(10)
        
        # Смотрим блок Техническая возможность
        els_div_txv = driver.find_elements(By.XPATH, '//div[@data-ctrl="s$addr_info"]')
        if len(els_div_txv) != 1: raise Exception('Ошибка: Не найден блок ТхВ')
        els_tbl = els_div_txv[0].find_elements(By.TAG_NAME, 'tbody')  # здесь 2 таблицы вложенные одна в другую
        if len(els_tbl) != 2: raise Exception('Ошибка: не опознана структура блока ТхВ')
        els_tr = els_tbl[1].find_elements(By.TAG_NAME, 'tr')
        if len(els_tr) == 0: raise Exception('Ошибка: нет строк в таблице ТхВ')
        # Проверим техническую возможность
        is_TxV_ok = True
        mess_txv = ''
        g_package = data.get('general_package')
        s_internet = data.get('service_internet')  # Тарифный план интернет если есть
        s_tv = data.get('service_tv')  # Тарифный план ТВ если есть
        if not g_package and not s_internet and not s_tv: raise Exception('Ошибка: Должен быть хотя бы один тарифный план')
        for el_tr in els_tr:
            if (g_package or s_internet) and el_tr.text.find('Интернет') >= 0 and el_tr.text.find('Нет Тех.Возм') >= 0:
                mess_txv += 'Интернет - Нет ТхВ,'
            if (g_package or s_tv) and el_tr.text.find('ТВ') >= 0 and el_tr.text.find('Нет Тех.Возм') >= 0:
                mess_txv += 'ТВ - Нет ТхВ,'
        if mess_txv: raise Exception(mess_txv)
        
        # Заполняем данные клиента
        # Старица возможно удлиннилась/сдвинулась, прокрутим страницу вниз
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(0.3)
        # Вводим ФИО
        firstname = data.get('firstname')
        if not firstname or not is_russian(firstname): firstname = 'Имя'
        patronymic = data.get('patronymic')
        if not patronymic or not is_russian(patronymic): patronymic = 'Отчество'
        lastname = data.get('lastname')
        if not lastname or not is_russian(lastname): lastname = 'Фамилия'

        els = driver.find_elements(By.XPATH, '//input[@name="s$lname"]')
        if len(els) != 1: raise Exception('Ошибка: Нет поля Фамилия клиента')
        els[0].send_keys(lastname)
        time.sleep(0.3)
        
        els = driver.find_elements(By.XPATH, '//input[@name="s$fname"]')
        if len(els) != 1: raise Exception('Ошибка: Нет поля Имя клиента')
        els[0].send_keys(firstname)
        time.sleep(0.3)

        els = driver.find_elements(By.XPATH, '//input[@name="s$mname"]')
        if len(els) != 1: raise Exception('Ошибка: Нет поля Отчество клиента')
        els[0].send_keys(patronymic)
        time.sleep(0.3)

        phone = data.get('phone')
        if phone == None: raise Exception('Ошибка: Не задано значение телефон')
        els = driver.find_elements(By.XPATH, '//input[@name="s$tel"]')
        if len(els) != 1: raise Exception('Ошибка: Нет поля Телефон клиента')
        els[0].send_keys(phone[1:])
        time.sleep(0.3)

        # Откуда абонент узнал о ТТК
        els = driver.find_elements(By.XPATH, '//div[@data-ctrl="s$found_ttk"]')
        if len(els) != 1: raise Exception('Ошибка: Нет поля Откуда абонент узнал о ТТК')
        els_spn = els[0].find_elements(By.XPATH, './/span[@class="trigger mdi mdi-20 mdi-chevron-down"]')
        if len(els_spn) != 1: raise Exception('Ошибка: Нет кнопки поля Откуда абонент узнал о ТТК')
        els_spn[0].click()
        time.sleep(3)
        els_div = els[0].find_elements(By.XPATH, './/div[@class="listbox-item"]')
        if len(els_div) == 0: raise Exception('Ошибка: Нет данных поля Откуда абонент узнал о ТТК')
        els_div[0].click()
        time.sleep(1)
        
        # Вводим доп. информацию
        comment = f'Клиент: {data["lastname"]} {data["firstname"]} {data["patronymic"]}\n'
        comment += f'Адрес: {data["city"]}, {data["street"]} д.{data["house"]} кв.{data["apartment"]}\n'
        comment += f'Телефон: {data["phone"]}\n'
        tarif = ''
        if g_package: tarif += f'Общий пакет: {g_package}, '
        if s_internet: tarif += f'Интернет: {s_internet}, '
        if s_tv: tarif += f'ТВ: {s_tv}, '
        comment += f'Тариф: {tarif}\n'
        comment += f'{data["comment"]}\n'
        els = driver.find_elements(By.XPATH, '//textarea[@name="comment"]')
        if len(els) != 1: raise Exception('Ошибка: Нет поля комментарий')
        els[0].send_keys(comment)
        time.sleep(5)

        # Раздел услуги
        els = driver.find_elements(By.XPATH, '//div[@data-ctrl="s$obj_serv"]')
        if len(els) != 1: raise Exception('Ошибка: Нет блока кнопки поля услуги')
        els_spn = els[0].find_elements(By.XPATH, './/span[@add_action_id="7100110000000000000911"]')
        if len(els_spn) != 1: raise Exception('Ошибка: Нет кнопки поля услуги')
        els_spn[0].click()
        time.sleep(3)
        
        # Если общий пакет
        if g_package:
            els = driver.find_elements(By.XPATH, '//div[@data-ctrl="pack_new"]')
            if len(els) != 1: raise Exception('Ошибка: Нет блока услуги общий пакет')
            els_spn = els[0].find_elements(By.XPATH, './/span[@class="trigger mdi mdi-20 mdi-chevron-down"]')
            if len(els_spn) != 1: raise Exception('Ошибка: Нет кнопки поля услуги общий пакет')
            els_spn[0].click()
            time.sleep(3)
            els_div = els[0].find_elements(By.XPATH, './/div[@class="listbox-item"]')
            if len(els_div) == 0: raise Exception('Ошибка: Нет списка услуг общий пакет')
            lst_tarif = []
            print('Общий пакет:')
            for el_div in els_div:
                lst_tarif.append(el_div.text)
                print(el_div.text)
            i_fnd = find_string_to_substrs(lst_tarif, g_package)
            if i_fnd < 0: raise Exception(f'Ошибка: общий пакет с фразой(фразами) \"{g_package}\" не найден. Возможны варианты: {";".join(lst_tarif)}')
            els_div[i_fnd].click()
            time.sleep(3)
            
        else:
            # Если раздельно интернет
            if s_internet:
                els = driver.find_elements(By.XPATH, '//div[@data-ctrl="serv_inet_poffer"]')
                if len(els) != 1: raise Exception('Ошибка: Нет блока услуги интернет')
                els_spn = els[0].find_elements(By.XPATH, './/span[@class="trigger mdi mdi-20 mdi-chevron-down"]')
                if len(els_spn) != 1: raise Exception('Ошибка: Нет кнопки поля услуги интернет')
                els_spn[0].click()
                time.sleep(3)
                els_div = els[0].find_elements(By.XPATH, './/div[@class="listbox-item"]')
                if len(els_div) == 0: raise Exception('Ошибка: Нет списка услуг интернет')
                lst_tarif = []
                for el_div in els_div:
                    lst_tarif.append(el_div.text)
                i_fnd = find_string_to_substrs(lst_tarif, s_internet)
                if i_fnd < 0: raise Exception(f'Ошибка: услуга интернет с фразой(фразами) \"{s_internet}\" не найден. Возможны варианты: {";".join(lst_tarif)}')
                els_div[i_fnd].click()
                time.sleep(10)
            # Если раздельно ТВ
            if s_tv:
                els = driver.find_elements(By.XPATH, '//div[@data-ctrl="a$7100420000000000000379"]')
                if len(els) != 1: raise Exception('Ошибка: Нет блока услуги ТВ')
                els_spn = els[0].find_elements(By.XPATH, './/span[@data-column-name="a$7100420000000000000380_0"]')
                if len(els_spn) != 1: raise Exception('Ошибка: Нет поля услуги ТВ')
                els_spn1 = els_spn[0].find_elements(By.XPATH, './/span[@class="trigger mdi mdi-20 mdi-chevron-down"]')
                if len(els_spn1) != 1: raise Exception('Ошибка: Нет кнопки поля услуги ТВ')
                els_spn1[0].click()
                time.sleep(3)
                els_div = els[0].find_elements(By.XPATH, './/div[@class="listbox-item"]')
                if len(els_div) == 0: raise Exception('Ошибка: Нет списка услуг ТВ')
                lst_tarif = []
                for el_div in els_div:
                    lst_tarif.append(el_div.text)
                i_fnd = find_string_to_substrs(lst_tarif, s_tv)
                if i_fnd < 0: raise Exception(f'Ошибка: услуга ТВ с фразой(фразами) \"{s_tv}\" не найден. Возможны варианты: {";".join(lst_tarif)}')
                els_div[i_fnd].click()
                time.sleep(10)

        # Выбор оборудования
        equipment = data.get('equipment')
        if equipment:
            
            lst_target = equipment.split('##')
            
            for target in lst_target:
                target = target.strip()
                if len(target) == 0: continue
                l_tar = target.split('#')
                if len(l_tar) != 2: raise Exception(f'Ошибка: оборудование \"{target}\" должно быть в формате: название#способ_приобретения')
                device = l_tar[0]
                acquisition = l_tar[1]
                
                els = driver.find_elements(By.XPATH, '//div[@data-ctrl="a$7100420000000000000377"]')
                if len(els) != 1: raise Exception('Ошибка: Нет блока выбора оборудования')
                els_spn = els[0].find_elements(By.XPATH, './/span[@class="dummy-element"]')
                if len(els_spn) == 0: raise Exception('Ошибка: Нет поля выбора оборудования')
                # print('dummy-element', len(els_spn))
                els_spn[0].click()
                time.sleep(3)
                els_spn1 = els[0].find_elements(By.XPATH, './/span[@class="trigger mdi mdi-20 mdi-chevron-down"]')
                if len(els_spn1) == 0: raise Exception('Ошибка: Нет кнопки поля выбора оборудования')
                # print('trigger mdi mdi-20 mdi-chevron-down', len(els_spn1))
                # Выбираем оборудование
                els_spn1[len(els_spn1)-2].click()
                time.sleep(3)
                els_div = els[0].find_elements(By.XPATH, './/div[@class="listbox-item"]')
                if len(els_div) == 0: raise Exception('Ошибка: Нет списка оборудования')
                # print('listbox-item', len(els_div))
                lst_equipment = []
                for el_div in els_div:
                    lst_equipment.append(el_div.text)
                i_fnd = find_string_to_substrs(lst_equipment, device)
                if i_fnd < 0: raise Exception(f'Ошибка: оборудование с фразой(фразами) \"{device}\" не найден. Возможны варианты: {";".join(lst_equipment)}')
                els_div[i_fnd].click()
                time.sleep(3)
                # Выбираем способ приобретения
                els = driver.find_elements(By.XPATH, '//div[@data-ctrl="a$7100420000000000000377"]')
                els_spn = els[0].find_elements(By.XPATH, './/span[@class="control c-smartselect inited"]')
                if len(els_spn) == 0: raise Exception('Ошибка: Нет поля выбора способов приобретения')
                els_spn[len(els_spn)-1].click()
                time.sleep(3)
                els_spn1 = els[0].find_elements(By.XPATH, './/span[@class="trigger mdi mdi-20 mdi-chevron-down"]')
                if len(els_spn1) == 0: raise Exception('Ошибка: Нет кнопки поля выбора способов приобретения')
                # Выбираем оборудование
                els_spn1[len(els_spn1)-1].click()
                time.sleep(3)
                els_div = els[0].find_elements(By.XPATH, './/div[@class="listbox-item"]')
                if len(els_div) == 0: raise Exception('Ошибка: Нет списка способов приобретения')
                lst_acquisition = []
                for el_div in els_div:
                    lst_acquisition.append(el_div.text)
                    # print(el_div.text)
                i_fnd = find_string_to_substrs(lst_acquisition, acquisition)
                if i_fnd < 0: raise Exception(f'Ошибка: оборудование \"{device}\" со способом приобретения с фразой(фразами) \"{acquisition}\" не найден. Возможны варианты: {";".join(lst_acquisition)}')
                els_div[i_fnd].click()
                time.sleep(10)
                # print(f'Обор. {device} с приобретением {acquisition} выбран')

        # Старица возможно удлиннилась/сдвинулась, прокрутим страницу вниз
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(0.3)
        
        # Нажимаем кнопку сохранить
        els = driver.find_elements(By.XPATH, '//button[@value="Сохранить"]')
        if len(els) != 1: raise Exception('Ошибка: Нет кнопки сохранить заявку')
        els[0].click()
        time.sleep(5)
                
        # Всплывающее окно подтверждения действий
        mess_timeout = 'Истекло время ожидания окна подтверждения действий сохранить заявку'
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present(), mess_timeout)
            alert = driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            raise Exception(mess_timeout)           
        time.sleep(5)
            
        # Старица возможно удлиннилась/сдвинулась, прокрутим страницу вниз
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(0.3)

        # Нажимаем Добавить абонента
        els = driver.find_elements(By.XPATH, '//button[@value="Добавить абонента"]')
        if len(els) != 1: raise Exception('Ошибка: Нет кнопки Добавить абонента')
        els[0].click()
        time.sleep(5)
                
        driver.implicitly_wait(1)
        els = driver.find_elements(By.XPATH, '//div[@class="message msg-error"]')
        if len(els) > 0: raise Exception(f'Ошибка: Сообщение от ТТК: {els[0].text}')

        # Анализируем страницу ответа
        els = driver.find_elements(By.XPATH, '//td[@data-name="sub_proc_id"]')
        if len(els) != 1: raise Exception('Ошибка: В ответе нет поля с номером заявки')
        data['bid_number'] = els[0].text
        print(f'Создана заявка {data["bid_number"]}')
        time.sleep(1)
        # # # # # # data['bid_number'] = '333333'

        # time.sleep(15)
        # with open('out.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        # raise Exception('Финиш.')

    except Exception as e:
        print(e)
        return e, data,
    finally: driver.quit()   
    
    return '', data, 

def set_did_to_dj_domconnect():
    url = url_host + 'api/set_bid_ttk'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
        'login': 'wd_dc_sg',
        'password': 'QgdjJGNm',
        'id_lid': '1188357',
        
        'city': 'Ярославль',           # город
        # 'street': 'улица Пирогова',         # улица
        'street': 'улица Индустриальн',         # улица
        'house': '21',          # дом
        'apartment': '2',          # квартира
        
        # В названиях тарифных планов, названиях роутеров, приставок и способов приобретения
        # может быть указано либо название целиком либо набор ключевых фраз через точку с запятой
        'general_package': '',  # Название общего пакетного предложения     'На все 100. (Интернет + ИТВ + Приставка)'
        # 'general_package': 'На все 100. (Интернет + ИТВ + Приставка)',  # Название общего пакетного предложения     'На все 100. (Интернет + ИТВ + Приставка)'
        # По услугам: Название предложения по услуге или пусто если не нужна услуга
        # 'service_internet': '',      # Домашний интернет       'ТТК 100'
        'service_internet': 'ТТК 100',      # Домашний интернет       'ТТК 100'
        # 'service_internet': 'На все 100. (Интернет + Оборудование)',      # Домашний интернет
        # 'service_tv': '',      # ТВ
        'service_tv': 'Расширенный Привилегия 2021 Премиум',      # ТВ

        # 'equipment': '',      # Оборудование
        # 'equipment': 'Wi-Fi роутер DIR-615 единоразово#Оборудование',      # Оборудование
        # 'equipment': 'ТВ приставка SB-213 в рассрочку (целевая)',
        # В поле оборудование (equipment): Каждое оборудование указываем название#способ приобретения (через символ решетка)
        # Если несколько видов оборудования то их разделяем двумя символами решетка
        'equipment': 'ТВ приставка SB-213 в рассрочку (целевая)#Акция 1р./219р./219р.##Блок питания к ТВ приставкам SB-213, SB-214 единовременно (КТТК 400р.)#Оборудование##Wi-Fi роутер QBR-1041NW единоразово (2300р.)#Оборудование',
        
        'firstname': 'Иван',
        'patronymic': 'Иванович',
        'lastname': '',
        'phone': '79011111113',
        'comment': 'Тестовая заявка, просьба не обрабатывать',          # коментарий обязательно: подъезд этаж
        'bid_number': '',          # номер заявки
    }
    
    try:
        responce = requests.get(url, headers=headers, params=params)
        print(responce.status_code)
        print(responce.text)
    except:
        print('Error: requests.get')

def get_did_in_dj_domconnect():
    url = url_host + 'api/get_bid_ttk'
    
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
    url = url_host + 'api/set_bid_ttk_status'
    
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
    
    l_tarif = []
    g_package = bid_dict.get('general_package')
    s_internet = bid_dict.get('service_internet')
    s_tv = bid_dict.get('service_tv')
    if g_package: l_tarif.append(f'Общий пакет: {g_package}')
    if s_internet: l_tarif.append(f'Тариф интернет: {s_internet}')
    if s_tv: l_tarif.append(f'Тариф ТВ: {s_tv}')
        
    params = {
        'id': bid_dict.get('id_lid'),
        'fields[UF_CRM_5864F4DAAC508]': f'Заявка: {bid_dict.get("bid_number")}',
        'fields[UF_CRM_1493413514]': 4,
        'fields[UF_CRM_5864F4DA85D5A]': ', '.join(l_tarif),
        'fields[UF_CRM_1499386906]': 523  # PartnerWEB
    }
    error_message = bid_dict.get("bot_log")
    if error_message:
        params['fields[UF_CRM_5864F4DAAC508]'] = error_message

    try:
        responce = requests.post(url, headers=headers, params=params)
    except:
        pass
    # https://crm.domconnect.ru/crm/lead/details/1188357/

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

def run_bid_ttk(tlg_chat, tlg_token):
    opsos = 'ТТК'
    
    rez, bid_list = get_did_in_dj_domconnect()
    if rez:
        tlg_mess = 'Ошибка при загрузке заявок из domconnect.ru'
        r = send_telegram(tlg_chat, tlg_token, tlg_mess)
        print('TelegramMessage:', r)
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
            address = f'{data.get("city")} {data.get("street")} д.{data.get("house")} кв.{data.get("apartment")}\n'
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
    # https://onyma-crm.ttk.ru:4443/onyma/
    # login: wd_dc_sg
    # password: QgdjJGNm

    # # личный бот @infra
    # TELEGRAM_CHAT_ID = '1740645090'
    # TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'
    # run_bid_ttk(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
    
    # bid_dict = {
        # 'login': 'wd_dc_sg',
        # 'password': 'QgdjJGNm',
        # 'id_lid': '1188357',
        
        # # 'region': 'Калужская область',         # область или город областного значения
        # 'city': 'Ярославль',           # город
        # # 'city': 'Ростов-на-Дону',           # город
        # # 'street': 'Рабочая площадь',
        # # 'street': 'улица Пирогова',         # улица
        # 'street': 'улица Труфанова',         # улица
        # # 'street': 'улица Звёздная',         # улица
        # # 'street': 'улица Индустриальная',         # улица
        # 'house': '30 корп 3',          # дом
        # # 'house': '31/41',          # дом
        # 'apartment': '61',          # квартира
        
        # 'general_package': '',  # Название общего пакетного предложения     'На все 100. (Интернет + ИТВ + Приставка)'
        # # 'general_package': 'На все 100. (Интернет + ИТВ + Приставка)',  # Название общего пакетного предложения     'На все 100. (Интернет + ИТВ + Приставка)'
        # # По услугам: Название предложения по услуге или пусто если не нужна услуга
        # # 'service_internet': '',      # Домашний интернет       'ТТК 100'
        # 'service_internet': 'ТТК 100',      # Домашний интернет       'ТТК 100'
        # # 'service_internet': 'На все 100. (Интернет + Оборудование)',      # Домашний интернет
        # # 'service_tv': '',      # ТВ
        # 'service_tv': 'Расширенный Привилегия 2021 Премиум',      # ТВ

        # # 'equipment': '',      # Оборудование
        # # 'equipment': 'Wi-Fi роутер DIR-615 единоразово#Оборудование',      # Оборудование
        # # 'equipment': 'ТВ приставка SB-213 в рассрочку (целевая)',
        # 'equipment': 'ТВ приставка SB-213 в рассрочку (целевая)#Акция 1р./219р./219р.##Блок питания к ТВ приставкам SB-213, SB-214 единовременно (КТТК 400р.)#Оборудование##Wi-Fi роутер QBR-1041NW единоразово (2300р.)#Оборудование',
        # # # В названиях тарифных планов, названиях роутеров, приставок и способов приобретения
        # # # может быть указано либо название целиком либо набор ключевых фраз через точку с запятой
        
        
        # 'firstname': 'Иван',
        # 'patronymic': '',
        # 'lastname': '',
        # 'phone': '79011111113',
        # 'comment': 'Тестовая заявка, просьба не обрабатывать',          # коментарий обязательно: подъезд этаж
        # 'bid_number': '',          # номер заявки
    # }
    # # street = 'Рабочая площадь'
    # # s = ordering_street_by_type(street)
    # # print(s)
    # e, data = set_bid(bid_dict)
    
    # # print(data['bid_number'])
    
    # set_did_to_dj_domconnect()
    # rez, bid_list = get_did_in_dj_domconnect()
    # for bid_dict in bid_list:
        # for k, v in bid_dict.items():
            # print(k, v)
    # data = {'id': 1, 'bid_number': '55632145', 'bot_log': 'Заявка принята'}
    # set_bid_status(3, data)
    
    
    pass
    '''
        В Калуге ул Бульвар Моторостроителей
        В Москве б-р Волжский
    '''
    '''
        Примеры пакетных предложений:
            На все 100. (Интернет + ИТВ + Приставка)
            На все 100. (Интернет + Оборудование)
            Сногсшибательный (Интернет + ИТВ + Видеосервис Start)
            Сногсшибательный (Интернет + ИТВ)
            Ударный (Интернет + ИТВ + Приставка)
            Ударный (Интернет + ИТВ Социальный)
    
        Примеры тарифов Интернет:
            В Игре
            Макси.
            Сногсшибательный
            ТТК 100
            ТТК 60
            Ударный

        Примеры тарифов ТВ:
            Базовый Привилегия 2021 Премиум
            Интерактивное ТВ "Профессионал ТВ"
            Интерактивное ТВ "Тариф Базовый март 2019"
            Интерактивное ТВ "Тариф Расширенный март 2019"
            Интерактивное ТВ "Тариф Социальный 01.09.2018"
            Расширенный Привилегия 2021 Премиум
            Социальный Привилегия 2021 Премиум

        Примеры оборудования:
            Wi-Fi роутер DIR-615 в рассрочку (целевая)
            Wi-Fi роутер DIR-615 единоразово (КТТК 1750р.)
            Wi-Fi роутер DIR-620 в рассрочку (целевая)
            Wi-Fi роутер DIR-620 единоразово (КТТК 1750р.)
            Wi-Fi роутер QBR-1041NW в рассрочку (целевая)
            Wi-Fi роутер QBR-1041NW единоразово (2300р.)
            Wi-Fi роутер SNR-CPE-W4N в рассрочку (целевая)
            Wi-Fi роутер SNR-CPE-W4N единоразово (КТТК 1750р.)
            Блок питания к ТВ приставкам NV-501, NV-501-WAC единовременно (КТТК 400р.)
            Блок питания к ТВ приставкам SB-213, SB-214 единовременно (КТТК 400р.)
            Восстановленная ТВ приставка Eltex NV 501 WAC в рассрочку (целевая)
            Восстановленная ТВ приставка Eltex NV 501 WAC единоразово (КТТК 4500р.)
            Восстановленная ТВ приставка Eltex NV 501 в рассрочку (целевая)
            Восстановленная ТВ приставка Eltex NV 501 единоразово (КТТК 4500р.)
            Восстановленная ТВ приставка Eltex NV 711 WAC в рассрочку (целевая)
            Восстановленная ТВ приставка Eltex NV 711 WAC единоразово (КТТК 4500р.)
            Восстановленная ТВ приставка Eltex NV 711 в рассрочку (целевая)
            Восстановленная ТВ приставка Eltex NV 711 единоразово (КТТК 4500р.)
            Восстановленная ТВ приставка SB-213 в рассрочку (целевая)
            Восстановленная ТВ приставка SB-213 единоразово (КТТК 4500р.)
            Восстановленная ТВ приставка SB-214 в рассрочку (целевая)
            Восстановленная ТВ приставка SB-214 единоразово (КТТК 4500р.)
            Программное обеспечение Apple TV
            Программное обеспечение Smart TV
            Пульт дистанционного управления к ТВ приставкам NV-501/501WAC/711/711WAC единовременно (500р.)
            Пульт дистанционного управления к ТВ приставкам SB-213, SB-214 единовременно (550р.)
            ТВ приставка Eltex NV-501 Wac в рассрочку (целевая)
            ТВ приставка Eltex NV-501 Wac единоразово (КТТК 5000р.)
            ТВ приставка Eltex NV-501 в рассрочку (целевая)
            ТВ приставка Eltex NV-501 единоразово (КТТК 5000р.)
            ТВ приставка Eltex NV-711 Wac в рассрочку (целевая)
            ТВ приставка Eltex NV-711 Wac единоразово (5000р.)
            ТВ приставка Eltex NV-711 в рассрочку (целевая)
            ТВ приставка Eltex NV-711 единоразово (5000р.)
            ТВ приставка SB-213 в рассрочку (целевая)
            ТВ приставка SB-213 единоразово (КТТК 5000р.)
            ТВ приставка SB-214 в рассрочку (целевая)
            ТВ приставка SB-214 единоразово (КТТК 5000р.)
            ТВ приставка SB-315 в рассрочку (целевая)
            ТВ приставка SB-315 единоразово (КТТК 5000р.)

        Примеры способов приобретения:
            110р./175р./175р.
            150р. х 36мес.
            1р./229р./229р.
            210р. х 24мес.
            Акция 1р./219р./219р.
            Профессионал 165р. х 24мес.
            Оборудование
    '''
