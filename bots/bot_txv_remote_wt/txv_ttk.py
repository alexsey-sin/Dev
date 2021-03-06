import os, re, time, json, requests  # pip install requests
from datetime import datetime
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'
opsos = 'ТТК'
pv_code = 5

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
        
        >>> ordering_house('2')
        ('2', '2')
        
        >>> ordering_house('A')
        ('', 'Номер из одной буквы')
        
        Запуск теста: $> python -m doctest txv_ttk.py
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

def is_russian(s: str) -> bool:  # Проверка строки на русские символы
    """
        Проверка входящей строки на наличие в ней только
        букв кириллического алфавита и символы `-` и пробел
        Запуск теста: $> python -m doctest txv_ttk.py
    
        >>> is_russian('абвгд')
        True
        
        >>> is_russian('аовгкjkl')
        False
        
    """
    return bool(re.fullmatch(r'(?i)[а-яё -]+', s))

def wait_spinner(driver):  # Ожидаем крутящийся спинер
    driver.implicitly_wait(1)
    while True:
        time.sleep(1)
        els = driver.find_elements(By.XPATH, '//span[@class="loader"]')
        if len(els):
            attr_disp = els[0].get_attribute('style')
            if attr_disp == '':
                # print('spinner')
                continue
            else: break
        else: break
    driver.implicitly_wait(10)
    time.sleep(2)

# =========================================================
def get_txv(data):
    driver = None
    try:
        base_url = 'https://onyma-crm.ttk.ru:4443/onyma/'
        
        EXE_PATH = 'driver/chromedriver.exe'
        # driver = webdriver.Chrome(executable_path=EXE_PATH)
        service = Service(EXE_PATH)
        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(10)
        driver.get(base_url)
        time.sleep(3)
        
        ###################### Страница Логин/Пароль ######################
        els = driver.find_elements(By.XPATH, '//input[@id="id_login"]')
        if len(els) != 1: raise Exception('Ошибка Нет поля логин')
        login = data.get('login')
        try:
            if login: els[0].send_keys(login)
            else: raise Exception('Ошибка не задано значение логин')
        except: raise Exception('Ошибка ввода логин')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@id="id_password"]')
        if len(els) != 1: raise Exception('Ошибка Нет поля пароль')
        password = data.get('password')
        try:
            if password: els[0].send_keys(password)
            else: raise Exception('Ошибка не задано значение пароль')
        except: raise Exception('Ошибка ввода пароль')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//select[@id="id_realm"]')
        if len(els) != 1: raise Exception('Ошибка Нет поля тип пользователя')
        f_ok = False
        els_opt = els[0].find_elements(By.TAG_NAME, 'option')
        for el_opt in els_opt:
            if el_opt.get_attribute('value') == 'ttk':
                try: el_opt.click()
                except: raise Exception('Ошибка клика ТТК')
                time.sleep(1)
                f_ok = True
                break
        if f_ok == False: raise Exception('Ошибка Пользователя ТТК нет в списке')

        els = driver.find_elements(By.XPATH, '//input[@type="submit"]')
        if len(els) != 1: raise Exception('Ошибка Нет кнопки Войти')
        try: els[0].click()
        except: raise Exception('Ошибка клика Войти')
        time.sleep(3)

        ###################### Страница Сводные панели ######################
        els = driver.find_elements(By.XPATH, '//a[@href="/onyma/dashboard"]')
        if len(els) != 1: raise Exception('Ошибка Нет ссылки Сводные панели')
        try: els[0].click()
        except: raise Exception('Ошибка клика Сводные панели')
        time.sleep(3)

        ###################### Страница Адрес ######################
        # Вводим Город
        els_div_city = driver.find_elements(By.XPATH, '//div[@data-ctrl="s$region"]')
        if len(els_div_city) != 1: raise Exception('Ошибка Нет блока Город')
        els_inp = els_div_city[0].find_elements(By.XPATH, './/input[@class="editbox w-text value-empty"]')
        if len(els_inp) != 1: raise Exception('Ошибка Нет поля ввода Город')
        city = data.get('city', '')
        if city:
            city = city.replace('ё', 'е')
            city = ordering_city(city)
        else: raise Exception('Ошибка город не задан.')
        try:
            els_inp[0].click()
            time.sleep(0.2)
            els_inp[0].send_keys(city)
            time.sleep(0.2)
            els_inp[0].send_keys(Keys.ENTER)
        except: raise Exception('Ошибка ввода город')
        time.sleep(5)
        # Смотрим варианты
        els_div_opt = els_div_city[0].find_elements(By.XPATH, './/div[@class="options"]')
        if len(els_div_opt) != 1: raise Exception('Ошибка Нет блока подсказок Город')
        els_opt = els_div_opt[0].find_elements(By.TAG_NAME, 'span')
        if len(els_opt) == 0: raise Exception(f'Ошибка нас.пункт {city} не найден.')
        lst_city = []
        try:
            els_inp[0].send_keys(Keys.ARROW_DOWN)
            time.sleep(0.2)
            for el_opt in els_opt:
                if el_opt.text == '': continue
                lst_city.append(el_opt.text)
            i_fnd = find_short(lst_city)
            if i_fnd < 0: raise Exception(f'Ошибка нас.пункт {city} не найден2.')
            # Пробежим по списку подсказки
            for _ in range(i_fnd):
                els_inp[0].send_keys(Keys.ARROW_DOWN)
                time.sleep(0.2)
            els_inp[0].send_keys(Keys.ENTER)
        except: raise Exception('Ошибка кликов в списке городов')
        time.sleep(2)
        
        # Вводим Улицу/дом
        els_div_addr = driver.find_elements(By.XPATH, '//div[@data-ctrl="s$addr_ctrl"]')
        if len(els_div_addr) != 1: raise Exception('Ошибка Нет блока Адрес')
        els_inp = els_div_addr[0].find_elements(By.XPATH, './/input[@class="editbox w-text value-empty"]')
        if len(els_inp) != 1: raise Exception('Ошибка Нет поля ввода Адрес')
        street = data.get('street')
        if street == None: raise Exception('Ошибка Не задано значение Улица')
        name_street = ordering_street_by_type(street)
        if name_street == '': name_street = street
        
        # Добавляем дом
        house = data.get('house')
        if house == None: raise Exception('Ошибка Не задано значение Дом')
        c_house = ordering_house(house)
        if c_house[0] == '': raise Exception(f'Ошибка Дом {house} {c_house[1]}')
        # print(c_house)
        str_hs = f'{name_street}, д {c_house[0]}'
        try: els_inp[0].send_keys(str_hs)
        except: raise Exception('Ошибка ввода значение улица/дом')
        wait_spinner(driver)  # Подождем если есть спинер
        time.sleep(1)
        # Смотрим варианты
        els_div_opt = els_div_addr[0].find_elements(By.XPATH, './/div[@class="option"]')  # здесь их много
        if len(els_div_opt) == 0: raise Exception(f'Ошибка Улица {name_street} не найдена.')
        lst_street = []
        for i in range(len(els_div_opt)):
            txt = els_div_opt[i].text
            i_s = txt.find(name_street)
            i_h = txt.find(f'д {c_house[1]}')
            if i_s >= 0 and i_h >= 0: lst_street.append((i, txt[i_s:]))

        if len(lst_street) > 0:
            f_ind = find_short_tup(lst_street)
            try: els_div_opt[f_ind].click()
            except: raise Exception('Ошибка клика значение Улица2')
            time.sleep(3)
        else: raise Exception(f'Ошибка Улица {name_street} д. {c_house[0]} не найдена.')
                
        # Добавляем квартиру
        els_add = els_div_addr[0].find_elements(By.XPATH, './/span[@class="do-add cursor-pointer mdi onm-icon-plus mdi-15"]')
        if len(els_add) != 1: raise Exception('Ошибка Нет кнопки добавить квартиру')
        try: els_add[0].click()
        except: raise Exception('Ошибка клика добавить квартиру')
        time.sleep(1)
        els_app = els_div_addr[0].find_elements(By.XPATH, './/input[@name="prop7100460000000000000001"]')
        if len(els_app) != 1: raise Exception('Ошибка Нет поля ввести квартиру')
        apartment = data.get('apartment')
        if apartment == None: raise Exception('Ошибка Не задано значение Квартира')
        try: els_app[0].send_keys(apartment)
        except: raise Exception('Ошибка ввода значение Квартира')
        time.sleep(1)
        els_btn_add = els_div_addr[0].find_elements(By.XPATH, './/input[@value="Добавить"]')
        if len(els_btn_add) != 1: raise Exception('Ошибка Нет кнопки добавить квартиру')
        try: els_btn_add[0].click()
        except: raise Exception('Ошибка клика добавить квартиру')
        time.sleep(3)
        
        # Жмем кнопку проверить адрес
        els = driver.find_elements(By.XPATH, '//input[@value="Проверить адрес"]')
        if len(els) != 1: raise Exception('Ошибка Нет кнопки Проверить адрес')
        try: els[0].click()
        except: raise Exception('Ошибка клика Проверить адрес')
        time.sleep(10)
        
        # Смотрим блок Техническая возможность
        els_div_txv = driver.find_elements(By.XPATH, '//div[@data-ctrl="s$addr_info"]')
        if len(els_div_txv) != 1: raise Exception('Ошибка Не найден блок ТхВ')
        els_tbl = els_div_txv[0].find_elements(By.TAG_NAME, 'tbody')  # здесь 2 таблицы вложенные одна в другую
        if len(els_tbl) != 2: raise Exception('Ошибка не опознана структура блока ТхВ')
        els_tr = els_tbl[0].find_elements(By.TAG_NAME, 'tr')
        if len(els_tr) == 0: raise Exception('Ошибка нет строк в таблице ТхВ_1')
        # Возьмем определившийся адрес
        data['pv_address'] = ''
        for el_tr in els_tr:
            els_td = el_tr.find_elements(By.TAG_NAME, 'td')
            if len(els_td) < 2: continue
            if els_td[0].text.find('По адресу') >= 0:
                data['pv_address'] = els_td[1].text

        # Проверим техническую возможность
        data['available_connect'] = ''
        els_tr = els_tbl[1].find_elements(By.TAG_NAME, 'tr')
        if len(els_tr) == 0: raise Exception('Ошибка нет строк в таблице ТхВ_2')
        s_inet = False
        s_tv = False
        for el_tr in els_tr:
            els_td = el_tr.find_elements(By.TAG_NAME, 'td')
            if len(els_td) < 3: continue
            if els_td[0].text.find('Интернет') >= 0:
                data['available_connect'] += f'Интернет: {els_td[1].text}\n'
                if els_td[1].text.find('Есть Тех.Возм.') >= 0:
                    s_inet = True
            if els_td[0].text.find('ТВ') >= 0:
                data['available_connect'] += f'ТВ: {els_td[1].text}\n'
                if els_td[1].text.find('Есть Тех.Возм.') >= 0:
                    s_tv = True
        if data['available_connect'] == '':
            data['available_connect'] = 'ТхВ не определено'
            raise Exception('')
        if s_inet == False and s_tv == False: raise Exception('')
        
        time.sleep(1)

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
        'login': 'wd_dc_sg',
        'password': 'QgdjJGNm',
        'id_lid': '1215557',
        
        # 'region': 'Калужская область',         # область или город областного значения
        'city': 'Калуга',           # город
        'street': 'улица Ленина',         # улица
        'house': '31',          # дом
        'apartment': '2',          # квартира

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
    
    params = {
        'id': txv_dict.get('id_lid'),
        'fields[UF_CRM_1638779781554][]': restrictions[:500],  # вся инфа
    }
    up_status = ''
    if upgrade_status:
        params['fields[STATUS_ID]'] = '72'
        up_status = 'Статус обновлен.'

    # Отсылаем данные в СРМ
    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.update'
    try:
        responce = requests.post(url, headers=headers, params=params)
        st_code = responce.status_code
        if st_code != 200: return st_code, ''
        # посмотреть результат https://crm.domconnect.ru/crm/lead/details/1215557/
    except Exception as e:
        return str(e), ''
    
    if upgrade_status:
        # Запрос в СРМ на создание задачи на контент
        url = 'https://crm.domconnect.ru/rest/371/exgy6kr03s1r1dsf/bizproc.workflow.start'
        data = {
            'TEMPLATE_ID': 407,
            'DOCUMENT_ID':
                [
                    'crm',
                    'CCrmDocumentLead',
                    txv_dict.get('id_lid'),
                ],
        }
        try:
            responce = requests.post(url, headers=headers, json=data)
            st_code = responce.status_code
            if st_code != 200: return st_code, ''
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

def run_txv_ttk(tlg_chat, tlg_token):
    # личный бот @infra
    TELEGRAM_CHAT_ID = '1740645090'
    TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'
    
    rez, txv_list = get_txv_in_dj_domconnect(pv_code)
    if rez:
        tlg_mess = f'ТхВ {opsos}: Ошибка при загрузке запросов из domconnect.ru'
        r = send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, tlg_mess)
        print(tlg_mess, '\nTelegramMessage:', r)
        return
    if len(txv_list) == 0:
        cur_time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        print(f'{cur_time} {opsos}: Запросов ТхВ нет')
        return

    # Перелистываем список словарей с заявками
    for txv_dict in txv_list:
        tlg_mess = ''
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
    start_time = datetime.now()
    
    # https://onyma-crm.ttk.ru:4443/onyma/
    # login: wd_dc_sg
    # password: 9zWxQjOh

    
    # txv_dict = {
        # 'pv_code': pv_code,
        # 'login': 'wd_dc_sg',
        # 'password': '9zWxQjOh',
        # 'id_lid': '1215557',
        
        # # 'city': 'Абакан',           # город
        # # 'street': 'Кати Перекрещенко',         # улица
        # # 'house': '2',          # дом
        # # 'apartment': '95',          # квартира

        # # 'region': 'Калужская область',         # область или город областного значения
        # # 'city': 'Калуга',           # город
        # # 'street': 'улица Ленина',         # улица
        # # 'house': '31',          # дом
        # # 'apartment': '2',          # квартира

        # # # # 'region': 'Ярославская область',         # область или город областного значения
        # # 'city': 'Ярославль',           # город
        # # 'street': 'улица Звездная',         # улица улица Звездная 31
        # # 'house': '31/41',          # дом
        # # 'apartment': '61',          # квартира

        # # # 'region': 'Нижегородская область',         # область или город областного значения
        # # 'city': 'Заволжье',           # город     проспект Дзержинского 54
        # # 'street': 'проспект Дзержинского',         # улица
        # # 'house': '54',          # дом
        # # 'apartment': '64',          # квартира

        # # # 'region': 'Нижегородская область',         # область или город областного значения
        # # 'city': 'Калининград',           # город
        # # 'street': 'Беломорская улица',         # улица
        # # 'house': '2',          # дом
        # # 'apartment': '10',          # квартира

        # # 'region': 'Владимирская область',         # область или город областного значения
        # # 'city': 'Муром',           # город
        # # 'street': '30 лет Победы',         # улица      30 лет Победы 9
        # # 'house': '9',          # дом
        # # 'apartment': '4',          # квартира

        # # 'city': 'посёлок Новогорный',           # город
        # # 'street': '8 Марта',         # улица
        # # 'house': '7',          # дом
        # # 'apartment': '30',          # квартира

        # # # 'region': 'Ярославская область',         # область или город областного значения
        # # 'city': 'Ярославль',           # город
        # # 'street': 'улица Труфанова',         # улица
        # # 'house': '29 корп 2',          # дом
        # # 'apartment': '63',          # квартира

        # # # 'region': 'Ярославская область',         # область или город областного значения
        # 'city': 'Тульская область посёлок Грицовский',           # город
        # 'street': 'Первомайская улица',         # улица
        # 'house': '9',          # дом
        # 'apartment': '10',          # квартира

        # 'available_connect': '',  # Возможность подключения
        # 'tarifs_all': '', # список названий тарифных планов
        # 'pv_address': '',
    # }
    
    
    # e, data = get_txv(txv_dict)
    # if e: print(e)
    # print(data['tarifs_all'])
    # print(data['available_connect'])
    # print(data['pv_address'])
    
    
    set_txv_to_dj_domconnect(pv_code)
    # rez, txv_list = get_txv_in_dj_domconnect(pv_code)
    # print(rez)
    # for txv_dict in txv_list:
        # for k, v in txv_dict.items():
            # print(k, v)
    # data = {'id': 1, 'pv_address': '55632145', 'bot_log': 'Заявка принята МТС'}
    # r = set_txv_status(0, data)
    # print(r)
    
    # rez, stre = search_for_an_entry(lst_street, 'Светла')
    # rez = search_for_an_entry(lst_reg, 'ярославль')
    # rez = search_for_an_entry(lst_reg, 'Санкт-Петербург')
    

    # Калужская область	Калуга	улица Ленина 31
    # Санкт-Петербург Санкт-Петербург улица Маршала Казакова 78к1
    # Ярославская область Ярославль проспект Толбухина 31




    
    
    pass
    
    end_time = datetime.now()
    time_str = '\nDuration: {}'.format(end_time - start_time)
    print(time_str)
    # limit_request_line

