import os
import time
from datetime import datetime
import requests  # pip install requests
import json
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

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
    
def ordering_street(in_street: str):  # Преобразование строки улица
    '''
        разбиваем строку по запятым, и каждый фрагмент проверяем на
        изветсный тип улицы
        выдаем название без типа улицы
        если известный тип не найден - возвращаем пустую строку
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
    out_street = ''
    lst = in_street.split(',')
    for sub in lst:
        rez = False
        for ts in lst_type_street:
            if sub.find(ts) >= 0:
                rez = True
                out_street = sub.replace(ts, '').strip()
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
    if len(lst_house) == 2:  # значит буква - склеиваем как 30А
        lst_house[1] = lst_house[1].upper()
        return (lst_house[0], ''.join(lst_house))
    # анализируем  корп, литер
    if lst_house[1].find('к') >= 0:
        lst_house[1] = ' к'
        return (lst_house[0], ''.join(lst_house))
    if lst_house[1].find('л') >= 0:
        lst_house[1] = ' лит'
        return (lst_house[0], ''.join(lst_house))
    
    return ('', 'Номер не распознан')

def get_txv(data):
    driver = None
    try:
        base_url = 'https://internet-tv-dom.ru/operator'
        
        EXE_PATH = 'driver/chromedriver.exe'
        driver = webdriver.Chrome(executable_path=EXE_PATH)

        # EXE_PATH = r'c:/Dev/bot_opsos/driver/firefoxdriver.exe'
        # driver = webdriver.Firefox(executable_path=EXE_PATH)

        driver.implicitly_wait(1)
        driver.get(base_url)
        time.sleep(3)
        
        ###################### Страница ссылок городов ######################
        city = data.get('city')
        els = driver.find_elements(By.XPATH, '//div[@id="b12356"]')
        if len(els) != 1: raise Exception('Ошибка нет блока городов')
        els_a = els[0].find_elements(By.TAG_NAME, 'a')
        if len(els_a) == 0: raise Exception('Ошибка нет городов')
        url_city = ''
        for el_a in els_a:
            if el_a.text == city:
                url_city = el_a.get_attribute('href')
        if url_city: driver.get(url_city)
        else: raise Exception(f'Ошибка город \"{city}\" в списке городов не найден')

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
        # Вводим улицу
        els_street = el_addr.find_elements(By.XPATH, './/input[@id="street_name"]')
        if len(els_street) != 1: raise Exception('Ошибка Нет поля ввода Улица')
        street = data.get('street')
        if street == None: raise Exception('Ошибка Не задано значение Улица')
        ord_street = ordering_street(street)
        if ord_street == '': ord_street = street
        try: els_street[0].send_keys(ord_street)
        except: raise Exception('Ошибка ввода улицы')
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
                    except: raise Exception('Ошибка клика выбора улицы')
                    time.sleep(5)
                
            if f_ok == True: break
        if f_ok == False: raise Exception(f'Ошибка Улица: {street} не найдена')
        # Вводим дом
        els_house = el_addr.find_elements(By.XPATH, './/input[@id="house_id"]')
        if len(els_house) != 1: raise Exception('Ошибка Нет поля ввода Дом')
        house = data.get('house')
        if house == None: raise Exception('Ошибка Не задано значение Дом')
        try: els_house[0].send_keys(house)
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
                    if len(a_s[0].text) > 0: f_str.append(a_s[0].text)
                if len(f_str) > 0:
                    f_ok = True
                    i_sh = find_short(f_str)
                    try: els_li[i_sh].click()
                    except: raise Exception('Ошибка клика выбора дома')
                    time.sleep(5)
            if f_ok == True: break
        if f_ok == False: raise Exception(f'Ошибка Дом: {house} не найден')
        # Смотрим блок технической возможности дома
        av_connect = ''
        els = el_addr.find_elements(By.XPATH, './/td[@id="house_connected"]')
        if len(els) != 1: raise Exception('Ошибка Нет поля ТхВ дома')
        els_div = els[0].find_elements(By.TAG_NAME, 'div')
        for el_div in els_div:
            av_connect += f'{el_div.text}\n'
        
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
            av_connect += f'{el_div.text}\n'
        # Квартира подключена к интернет
        # Квартира подключена к ТВ
        # Квартира подключена к IPTV
        # Квартира не подключена к Домофонии
        # Квартира подключена к видеоконтролю
        # Промо-период доступен
        data['available_connect'] = av_connect
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
        # Жмем кнопку Далее
        els = el_addr.find_elements(By.XPATH, './/input[@value="Далее"]')
        if len(els) != 1: raise Exception('Ошибка После адреса нет кнопки Далее')
        try: els[0].click()
        except: raise Exception('Ошибка клика кнопки Далее2')
        time.sleep(3)
        ###################### Блок операции с договором ######################
        els_dog = driver.find_elements(By.XPATH, '//div[@id="operation_agreement_content"]')
        if len(els_dog) != 1: raise Exception('Ошибка Нет блока операции с договором')
        el_dog = els_dog[0]
        # Выбираем создать новый договор
        els_sel = el_dog.find_elements(By.XPATH, './/select[@id="sel_agreement"]')
        if len(els_sel) != 1: raise Exception('Ошибка Нет списка операции с договором')
        els_opt = els_sel[0].find_elements(By.TAG_NAME, 'option')
        f_ok = False
        for el_opt in els_opt:
            if el_opt.text == 'Создать новый договор':
                f_ok = True
                try: el_opt.click()
                except: raise Exception('Ошибка клика Создать новый договор')
                time.sleep(0.5)
                break
        if f_ok == False: raise Exception('Ошибка пункт: Создать новый договор не найден')
        # Жмем кнопку Далее
        els = el_dog.find_elements(By.XPATH, './/input[@value="Далее"]')
        if len(els) != 1: raise Exception('Ошибка После адреса нет кнопки Далее')
        try: els[0].click()
        except: raise Exception('Ошибка клика кнопки Далее3')
        time.sleep(3)
        ###################### Блок информация о клиенте ######################
        els_clnt = driver.find_elements(By.XPATH, '//div[@id="client_info_content"]')
        if len(els_clnt) != 1: raise Exception('Ошибка Нет блока информация о клиенте')
        el_clnt = els_clnt[0]
        # Вводим ФИО
        els_fio = el_clnt.find_elements(By.XPATH, '//input[@id="client_fio"]')
        if len(els_fio) != 1: raise Exception('Ошибка Нет поля ввода ФИО клиента')
        try: els_fio[0].send_keys('Клиент Клиентович')
        except: raise Exception('Ошибка ввода ФИО клиента')
        time.sleep(1)
        # Вводим телефон
        els_tlf = el_clnt.find_elements(By.XPATH, '//input[@id="phone_mobile"]')
        if len(els_tlf) != 1: raise Exception('Ошибка Нет поля ввода телефона')
        try: els_tlf[0].click()
        except: raise Exception('Ошибка клика активации поля ввода телефона')
        time.sleep(0.5)
        try: els_tlf[0].send_keys('011111111')
        except: raise Exception('Ошибка ввода телефона')
        time.sleep(1)
        # Жмем кнопку Далее
        els = el_clnt.find_elements(By.XPATH, './/input[@value="Далее"]')
        if len(els) != 1: raise Exception('Ошибка После Блок информация о клиенте нет кнопки Далее')
        try: els[0].click()
        except: raise Exception('Ошибка клика кнопки Далее4')
        time.sleep(3)
        ###################### Блок пакетов услуг ######################
        els_pack = driver.find_elements(By.XPATH, '//table[@id="products"]')
        if len(els_pack) != 1: raise Exception('Ошибка Нет блока пакетов услуг')
        els_div_pack = els_pack[0].find_elements(By.XPATH, './/div[@class="tarif_pack"]')
        lst_tar = []
        for el_div_pack in els_div_pack:
            els_lbl = el_div_pack.find_elements(By.TAG_NAME, 'label')
            if els_lbl[0]: lst_tar.append(els_lbl[0].text)
        data['tarifs_all'] = '\n'.join(lst_tar)
        ###################### Выбор оборудования интернет ######################
        time.sleep(2)

        # #===========
        # time.sleep(10)
        # with open('out.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        # raise Exception('Финиш.')
        # #===========

        
    except Exception as e:
        return str(e), data
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
        
        'city': 'Ярославль',           # город
        # 'street': 'улица Пирогова',         # улица
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

    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.update'
    
    # Данные для СРМ
    # 'available_connect': '',
    # 'tarifs_all': '',
    # 'pv_address': '',
    
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
    
    params = {
        'id': txv_dict.get('id_lid'),
        'fields[UF_CRM_1638779781554][]': restrictions[:500],  # вся инфа
    }

    try:
        responce = requests.post(url, headers=headers, params=params)
        st_code = responce.status_code
        if st_code != 200: return st_code
        # посмотреть результат https://crm.domconnect.ru/crm/lead/details/1215557/
    except Exception as e:
        return str(e)
    
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
        crm = send_crm_txv(data, opsos)  # ответ в CRM
        crm_mess = f'Ошибка при отправке в СРМ: {crm}\n'
        if crm:
            tlg_mess += crm_mess
            data['bot_log'] += crm_mess
        address = f'{data.get("city")} {data.get("street")} д.{data.get("house")} кв.{data.get("apartment")}'
        tlg_mess += f'{opsos}: - Выполнен запрос ТхВ\n'
        tlg_mess += f'Адрес: {address}\n'
        djdc = ''
        if rez == '':  # заявка успешно создана
            djdc = set_txv_status(3, data)
            tlg_mess += 'Успешно.\n'
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
    
    # https://internet-tv-dom.ru/operator
    # login: sinitsin
    # password: BVNocturne20

    # run_bid_mts()
    
    # txv_dict = {
        # 'pv_code': pv_code,
        # 'login': 'sinitsin',
        # 'password': 'BVNocturne20',
        # 'id_lid': '1215557',
        
        # 'city': 'Ярославль',           # город
        # # 'street': 'улица Пирогова',         # улица
        # 'street': 'улица Индустриальн',         # улица
        # 'house': '21',          # дом
        # 'apartment': '2',          # квартира
        
        # # 'city': 'Тольятти',           # город
        # # 'street': 'улица Карбышева',         # улица
        # # 'house': '16',          # дом
        # # 'apartment': '2',          # квартира

        # # 'city': 'Краснодар',           # город
        # # 'street': 'улица Троцкого',         # улица
        # # 'house': '32',          # дом
        # # 'apartment': '2',          # квартира

        # 'available_connect': '',
        # 'pv_address': '',
        # 'tarifs_all': '',
    # }
    
    
    # e, data = get_txv(txv_dict)
    # if e: print(e)
    # print('available_connect:\n', data['available_connect'])
    # print('tarifs_all:\n', data['tarifs_all'])
    # print('pv_address:\n', data['pv_address'])
    
    
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
    
    end_time = datetime.now()
    time_str = '\nDuration: {}'.format(end_time - start_time)
    print(time_str)
    # limit_request_line

