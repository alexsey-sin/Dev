import os
import time
from datetime import datetime
import requests  # pip install requests
import json
from selenium.webdriver.chrome.service import Service
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'
opsos = 'Билайн'
pv_code = 1


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

def check_equality_citys(lst: list, in_str: str):  # Поиск вхождения фразы в списке фраз
    '''
        Поиск вхождения фразы в списке фраз как самостоятельного слова
        Если нет вхождений - возвращаем []
    '''
    # Преобразуем входные данные к нижнему регистру
    in_str = in_str.lower().replace('ё', 'е')
    in_lst = [s.lower().replace('ё', 'е') for s in lst]
    
    # просмотрим список на вхождение как самостоятельного слова
    ln_sb = len(in_str)  # длина иск фразы
    rez_lst = []
    for i_lst in range(len(in_lst)):
        ln_str = len(in_lst[i_lst])  # длина фразы из списка
        # Соберем индексы всех вхождений
        lst_i = []
        i = -1
        while True:
            i = in_lst[i_lst].find(in_str, i+1)  # индекс начала иск фразы
            if i >= 0: lst_i.append(i) # иск фраза входит
            else: break
        if len(lst_i) == 0: continue # нет вхождений
        
        # Проверим каждое вхождение
        for li in lst_i:
            if li > 0:  # иск фраза не в начале
                if in_lst[i_lst][li - 1].isalpha(): continue  #не повезло - буква
            if li + ln_sb < ln_str:
                if in_lst[i_lst][li + ln_sb].isalpha(): continue #не повезло - буква
            # Слово самостоятельное, добавляем индекс в рез список
            rez_lst.append(i_lst)
            break
        
    return rez_lst

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
        for ts in lst_type_street:
            if sub.find(ts) >= 0:
                not_rez = False
                lst_ts.append((ts, sub.replace(ts, '').strip()))
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
    if lst_house[1].find('с') >= 0:
        lst_house[1] = 'СТР'
        return (lst_house[0], ''.join(lst_house))
    
    return ('', 'Номер не распознан')

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
    
def get_txv(data):
    driver = None
    rez_set_bid = ''
    try:
        base_url = 'https://partnerweb.beeline.ru/'
        
        EXE_PATH = 'driver/chromedriver.exe'
        service = Service(EXE_PATH)
        driver = webdriver.Chrome(service=service)

        # EXE_PATH = r'c:/Dev/bot_opsos/driver/firefoxdriver.exe'
        # driver = webdriver.Firefox(executable_path=EXE_PATH)

        driver.implicitly_wait(20)
        driver.get(base_url)
        time.sleep(3)
        
        ###################### Login ######################
        els = driver.find_elements(By.ID, 'id_login')
        if len(els) != 1: raise Exception('Ошибка нет поля логин')
        login = data.get('login')
        try: 
            if login: els[0].send_keys(login)
            else: raise Exception('Ошибка не задан логин')
        except: raise Exception('Ошибка действий 01')
        time.sleep(1)
        
        workercode = data.get('login_2')
        if not workercode: raise Exception('Ошибка не задан PartnerWeb (login2)')
        els = driver.find_elements(By.ID, 'id_workercode')
        if len(els) != 1: raise Exception('Ошибка нет поля workercode')
        try: els[0].send_keys(workercode)
        except: raise Exception('Ошибка действий 02')
        time.sleep(1)

        els = driver.find_elements(By.ID, 'id_password')
        if len(els) != 1: raise Exception('Ошибка нет поля пароль')
        password = data.get('password')
        try:
            if password: els[0].send_keys(password)
            else: raise Exception('Ошибка не задан пароль')
        except: raise Exception('Ошибка действий 03')
        time.sleep(1)

        els = driver.find_elements(By.TAG_NAME, 'button')
        if len(els) != 1: raise Exception('Ошибка нет кнопки войти')
        try: els[0].click()
        except: raise Exception('Ошибка действий 04')
        time.sleep(5)
        ###################### Главная страница ######################
        els_a = driver.find_elements(By.XPATH, '//a[@href="/ngapp#!/checkaddress/search"]')
        if len(els_a) != 1: raise Exception('Ошибка авторизации')
        try: els_a[0].click()
        except: raise Exception('Ошибка действий 05')
        time.sleep(5)
        ###################### Страница поиска адреса ######################
        # Вводим название населенного пункта
        els = driver.find_elements(By.ID, 'btn-append-to-body')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода города')
        city = data.get('city')
        try:
            city = city.replace('ё', 'е')
            if city: els[0].send_keys(city)
            else: raise Exception('Ошибка не задан город')
        except: raise Exception('Ошибка действий 06')
        time.sleep(3)
        
        # Ищем всплывающее контекстное меню с подсказкой города
        driver.implicitly_wait(1)

        els_ul = driver.find_elements(By.XPATH, '//ul[@class="dropdown-menu ng-scope"]')
        if len(els_ul) != 1: raise Exception('Ошибка нет всплывающее контекстное меню с подсказкой города')
        els_a = els_ul[0].find_elements(By.TAG_NAME, 'a')
        if len(els_a) == 0: raise Exception(f'Ошибка Населенный пункт {city} не найден')
        elif len(els_a) == 1:
            try: els_a[0].click()
            except: raise Exception('Ошибка действий 07')
        else:
            # Множественный выбор
            lst_nas_punkt = []
            for el in els_a:
                lst_nas_punkt.append(el.text)
            
            lst_cheq = check_equality_citys(lst_nas_punkt, city)
            if len(lst_cheq) == 0: raise Exception(f'Ошибка Населенный пункт: {city} не найден2')
            elif len(lst_cheq) > 1:
                lst_tup = []
                for ci in lst_cheq:
                    lst_tup.append((ci, lst_nas_punkt[ci]))
                i_tup = find_short_tup(lst_tup)
                try: els_a[i_tup].click()
                except: raise Exception('Ошибка действий 10')
        
        time.sleep(3)

        # Вводим название улицы
        els_street = driver.find_elements(By.XPATH, '//input[@placeholder="Улица"]')
        if len(els_street) != 1: raise Exception('Ошибка не найдено поле ввода названия улицы')
        el_street = els_street[0]
        # Удалим если что-то уже введено
        try:
            el_street.click()
            time.sleep(0.2)
            el_street.send_keys(Keys.CONTROL + 'a')
            time.sleep(0.2)
            el_street.send_keys(Keys.DELETE)
            time.sleep(0.2)
        except: raise Exception('Ошибка ввода 5')

        # Преобразуем в нормальный вид [тип, название]
        street = data.get('street')
        if not street: raise Exception('Ошибка не задано поле улица')
        street = street.replace('ё', 'е')
        lst_street = ordering_street(street)
        # print(lst_street)
        if lst_street:  # если распознали по типу
            try: el_street.send_keys(lst_street[1])
            except: raise Exception('Ошибка ввода 7')
        else:  # если нет - вводим как есть
            try: el_street.send_keys(street)
            except: raise Exception('Ошибка ввода 8')
            lst_street = ('', street)
        
        # Нажимаем кнопку найти
        els_button = driver.find_elements(By.XPATH, '//button[@ng-click="checkaddressAbstractController.searchPattern()"]')
        if len(els_button) != 1: raise Exception('Ошибка не найдена кнопка поиск улицы')
        try: els_button[0].click()
        except: raise Exception('Ошибка действий 13')
        time.sleep(5)
        
        # Определим - найдена ли улица однозначно
        els_div = driver.find_elements(By.XPATH, '//div[@ng-hide="checkaddressAbstractController.loading"]')
        if len(els_div) > 0:  # Проблемма - улица не найдена или множественный выбор
            streets = []
            for el_div in els_div:
                if el_div.text == 'Улицы не найдены':
                    raise Exception(f'Ошибка Улица: {street} не найдена.')
            
            # Ищем всплывающее контекстное меню с подсказкой улиц
            els_div = driver.find_elements(By.ID, 'listStart')
            if len(els_div) != 1: raise Exception('Ошибка - нет всплывающее контекстное меню с подсказкой улицы')
            els_a = els_div[0].find_elements(By.XPATH, './/a[@class="link ng-binding"]')
            if len(els_a) == 0: raise Exception(f'Ошибка Улица: {street} не найдена2.')
            f_lst = []
            for i in range(len(els_a)):
                txt = els_a[i].text
                if lst_street[0] == '':
                    if txt.find(lst_street[1]) >= 0: f_lst.append((i, txt))
                else:
                    if txt.find(lst_street[0]) >= 0 and txt.find(lst_street[1]) >= 0: f_lst.append((i, txt))
            if len(f_lst) == 0: raise Exception(f'Ошибка Улица: {street} не найдена3.')
            elif len(f_lst) == 1:
                try: els_a[f_lst[0][0]].click()
                except: raise Exception('Ошибка действий 14')
            else:
                i_fnd = find_short_tup(f_lst)
                try: els_a[i_fnd].click()
                except: raise Exception('Ошибка действий 15')
            time.sleep(1)

        driver.implicitly_wait(10)
        time.sleep(3)
        
        
        # Обработаем номер дома
        house = data.get('house')
        if house: c_house = ordering_house(house)
        else: raise Exception('Ошибка не задан номер дома')
        if c_house[0] == '': raise Exception(f'Ошибка не распознан номер дома: \"{house}\"')
        
        #=====================================
        table_all_house = False
        find_house = False
        link_house = None
        while True:
            # Ищем таблицу с номерами домов
            els_table = driver.find_elements(By.TAG_NAME, 'table')
            if len(els_table) != 1: raise Exception('Ошибка - нет таблицы домов')
            el_table = els_table[0]
            
            els_a = el_table.find_elements(By.TAG_NAME, 'a')
            if len(els_a) > 0:
                for el_a in els_a:
                    if el_a.text == c_house[1]:
                        link_house = el_a
                        find_house = True
                        break
                if find_house: break
            if table_all_house == False:
                # Кликнем: Показать все дома
                els = driver.find_elements(By.XPATH, '//div[@ng-click="checkaddressAbstractController.toggleConnectedHousesFilter()"]')
                if len(els) == 1:
                    try: els[0].click()
                    except: raise Exception('Ошибка действий 16')
                    time.sleep(2)
                table_all_house = True
            else: break
                
        
        time.sleep(2)
        if find_house:
            if table_all_house == False:
                try: link_house.click()
                except: raise Exception('Ошибка действий 17')
                time.sleep(3)
            else:
                data['available_connect'] = 'Нет ТхВ - Дом не подключен'
                raise Exception('')  # Просто выход
        else: raise Exception(f'Ошибка Дом: {house} не найден')
            
        # Берем информацию об ограничениях по адресу
        info_restrictions = 'Есть ТхВ\n'
        els = driver.find_elements(By.XPATH, '//div[@class="modal-content"]')
        if len(els) != 1: raise Exception('Ошибка нет всплывающего окна с информацией об ограничениях')
        els_b = els[0].find_elements(By.TAG_NAME, 'b')
        for el_b in els_b: info_restrictions += f'{el_b.text}\n'
        els_p = els[0].find_elements(By.TAG_NAME, 'p')
        for el_p in els_p: info_restrictions += f'{el_p.text}\n'
        
        data['available_connect'] = info_restrictions
        
        # Жмем продолжить
        els_btn = driver.find_elements(By.XPATH, '//button[@ng-click="ok()"]')
        if len(els_btn) != 1: raise Exception('Ошибка нет кнопки продолжить после прочтения ограничений')
        try: els_btn[0].click()
        except: raise Exception('Ошибка действий 18')
        time.sleep(3)
        ###################### Страница ввода заявки ######################
        # Ищем квартиру
        apartment = data.get('apartment')
        if apartment:
            driver.set_window_size(300,800)
            time.sleep(2)
            
            els_ih = driver.find_elements(By.XPATH, '//input[@name="flat"]')
            if len(els_ih) < 2: raise Exception('Ошибка нет поля ввода квартиры')
            try: els_ih[1].send_keys(apartment)
            except: raise Exception('Ошибка действий 19')
            time.sleep(1)
            driver.set_window_size(1000,1000)
            time.sleep(1)
        
        # Вытаскиваем определившийся адрес
        els = driver.find_elements(By.XPATH, '//a[contains(@ui-sref, "checkaddress.address")]')
        # (By.XPATH, '//textarea[contains(@class, "SearchInput_textArea")]')
        if len(els) == 0: raise Exception('Ошибка нет полного адреса')
        data['pv_address'] = els[0].text
        
        # Жмем проверить
        els_btn = driver.find_elements(By.XPATH, '//button[@ng-click="$abonCtrl.checkAddress()"]')
        if len(els_btn) < 2: raise Exception('Ошибка нет кнопки проверить квартиру')
        try: els_btn[0].click()
        except: raise Exception('Ошибка действий 20')
        time.sleep(3)

        driver.implicitly_wait(1)
        # Проверяем блок если есть активный договор
        els_er = driver.find_elements(By.XPATH, '//div[@ng-if="$abonCtrl.addressErrorMessage"]')
        if els_er:
            er_text = els_er[0].text
            if er_text.find('есть активный договор') >= 0: data['available_connect'] = 'Есть ТхВ'
            else: data['available_connect'] = er_text
        time.sleep(2)
        raise Exception('')  # Просто выход

        # #===========
        # time.sleep(10)
        # with open('out_file.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        # raise Exception('Финиш.')
        # #===========
        
    except Exception as e:
        rez_set_bid = str(e)[:100]
    finally:
        if driver: driver.quit()
   
    return rez_set_bid, data

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
        'login': '0K23-181',
        'password': 'CgslU7tfFsK5w8',
        'id_lid': '1215557',
        'city': 'Ярославль',
        'street': 'улица Труфанова',
        'house': '29 корп 3',
        'apartment': '65',
        'region': 'Яроа'
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

def run_txv_beeline(tlg_chat, tlg_token):
    tlg_mess = ''
    
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

    # Перелистываем список словарей с запросами
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
    # https://partnerweb.beeline.ru
    # set_txv_to_dj_domconnect(pv_code)
    
    # личный бот @infra     TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
    TELEGRAM_CHAT_ID = '1740645090'
    TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'
    
    # run_txv_beeline(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
    # rez, txv_list = get_txv_in_dj_domconnect(pv_code)
    # for val in txv_list:
        # print(val)
    
    # # Красногорск	Красногорский бульвар	8
    # data = {
        # 'login': 'S01-181',
        # 'login_2': '1999999222',
        # 'password': '8GFysus@kffs7',
        # 'pv_code': pv_code,

        # # 'city': 'Энгельс',8GFysus@kffs7 Липецк, ул Катукова д 24
        # # 'street': 'проспект Химиков',
        # # 'house': '3/1',
        # # 'apartment': '10',
        
        # # 'region': 'Московская область',
        # # 'city': 'Химки',
        # # 'street': 'микрорайон Левобережный, Совхозная улица',
        # # 'house': '18',
        # # 'apartment': '10',
        
        # 'region': 'Ленинградская область',
        # 'city': 'Липецк',
        # 'street': 'Катукова',  #
        # 'house': '24',
        # 'apartment': '10',
        
        # # 'region': 'Тверская область',
        # # 'city': 'Тверь',
        # # 'street': 'Волоколамский проспект',
        # # 'house': '14',     # Есть договор
        # # 'apartment': '10',
        
        # # 'region': 'Ярославская область',
        # # 'city': 'Ярославль',
        # # 'street': 'посёлок Текстилей, Большая Донская улица',
        # # 'house': '15',     # 
        # # 'apartment': '10',
        
        # # 'region': 'Мурманская область',
        # # 'city': 'Мурманск',
        # # 'street': 'Баумана',
        # # 'house': '36',     # 
        # # 'apartment': '10',
        
        # # 'region': 'Краснодарский край',
        # # 'city': 'Красноярск',
        # # 'street': 'проспект 60 лет Образования СССР',
        # # 'house': '14',     # Дом подключен
        # # 'apartment': '10',
        
        # 'available_connect': '',  # Возможность подключения
        # 'tarifs_all': '', # список названий тарифных планов
        # 'pv_address': '',
    # }
    # rez, data = get_txv(data)
    # if rez: print(rez)

    # print('available_connect:', data['available_connect'])
    # print('pv_address:', data['pv_address'])
    
    # end_time = datetime.now()
    # time_str = '\nDuration: {}'.format(end_time - start_time)
    # print(time_str)
    # limit_request_line

    # ls = [
        # 'район Режный, микрорайон Левобережный, Совхозная улица',
        # 'район Режный, микрорайон Левобережный',
        # 'микрорайон Левобережный',
        # 'микрорайон Левобережный, Совхозная',
        # 'Совхозная',
    # ]
    # for s in ls:
        # print(s)
        # rez = ordering_street(s)
        # print(rez)
        # print()
    # lc = [
        # 'Мурманская о., г. Мурманск',
        # 'Мурманская обл., ЗАТО Североморск, пгт. Т омскw',
        # # 'Мурманская обл., г. Оленегорск',
        # # 'Мурманская обл., г. Полярный',
        # # 'Мурманская обл., г. Североморск',
        # # 'Мурманская обл., нп. Видяево',
        # # 'Мурманская о., г. Мурманск',
        # ' омск2 '
    # ]
    # lst_cheq = check_equality_citys(lc, 'омск')
    # print(lst_cheq)
    pass
    '''
        1 аккаунт
            S24-61
            1010000101
            Gf&dhdk234hfbbs4

        2 аккаунт
            0K23-181
            1010000101
            CgslU7tfFsK5w8
    '''
    # user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

    # headers = {
        # 'Content-Type': 'application/json',
        # 'Connection': 'Keep-Alive',
        # 'User-Agent': user_agent_val,
    # }
    # url = 'https://crm.domconnect.ru/rest/371/exgy6kr03s1r1dsf/bizproc.workflow.start'
    # # url = 'https://crm.domconnect.ru/rest/371/exgy6kr03s1r1dsf/bizproc.workflow.start?TEMPLATE_ID=407&DOCUMENT_ID[]=crm&DOCUMENT_ID[]=CCrmDocumentLead&DOCUMENT_ID[]=1439397'
    # params = {
        # 'TEMPLATE_ID': 407,
        # # 'DOCUMENT_ID': ['crm', 'CCrmDocumentLead', txv_dict.get('id_lid')],
        # 'DOCUMENT_ID[]': ['crm', 'CCrmDocumentLead', 1440564],
    # }
    # responce = requests.post(url, headers=headers, params=params)
    # # responce = requests.post(url, headers=headers)
    # st_code = responce.status_code
    # print(st_code)
    
    
    # https://crm.domconnect.ru/rest/371/exgy6kr03s1r1dsf/bizproc.workflow.start?TEMPLATE_ID=407&DOCUMENT_ID[]=crm&DOCUMENT_ID[]=CCrmDocumentLead&DOCUMENT_ID[]=1439397
    
    
    