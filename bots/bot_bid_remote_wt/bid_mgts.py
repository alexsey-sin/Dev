import os
import time
from datetime import datetime, timedelta 
import requests  # pip install requests
import json
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'

def ordering_street(in_street: str):  # Преобразование строки улица
    '''
        разбиваем строку по запятым, и каждый фрагмент проверяем на
        изветсный тип улицы
        выдаем список из бвух элементов: название и сокращенный тип улицы
        если известный тип не найден - возвращаем пустой список
    '''
    type_abbr = {
        'улица': 'ул.',
        'проспект': 'просп.',
        'переулок': 'пер.',
        'шоссе': 'шоссе',
        'аллея': 'аллея',
        'тупик': 'тупик',
        'проезд': 'пр.',
        'набережная': 'наб.',
        'площадь': 'пл.',
        'бульвар': 'бульв.',
    }
    # Преобразуем ё к е
    in_street = in_street.replace('ё', 'е')
    
    out_cort = []
    lst = in_street.split(',')
    for sub in lst:
        rez = False
        for ts in type_abbr.keys():
            if sub.find(ts) >= 0:
                rez = True
                name = sub.replace(ts, '').strip()
                out_cort.append(name)
                out_cort.append(f'{type_abbr[ts]} {name}')
                break
        if rez: break
    return out_cort

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
    in_house = in_house.replace('.', '')
    # Проходим по строке и если цифры сливаются с буквами вставляем пробел
    n_house = ''
    lst_house = [in_house[0],]
    is_dig = False
    if in_house[0].isdigit(): is_dig = True
    for i in range(1, len(in_house)):
        if not in_house[i].isalpha() and is_dig == False:
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

    lst_house = in_house.split(' ')
    if len(lst_house) == 1: return (lst_house[0], lst_house[0])
    if len(lst_house) > 3: return ('', 'В номере много позиций')
    if len(lst_house) == 2:  # значит буква - склеиваем как 30а
        lst_house[1] = lst_house[1].lower()
        return (lst_house[0], ''.join(lst_house))
    # анализируем  корп, литер
    if lst_house[1].find('к') >= 0:
        lst_house[1] = ', корп.'
        return (lst_house[0], ''.join(lst_house))
    if lst_house[1].find('л') >= 0:
        lst_house[1] = ', лит.'
        return (lst_house[0], ''.join(lst_house))
    if lst_house[1].find('с') >= 0:
        lst_house[1] = ', стр.'
        return (lst_house[0], ''.join(lst_house))
    
    return ('', 'Номер не распознан')

def find_short_tup(f_lst):
    '''
        На входе список кортежей.
        в кортеже индкс фразы на странице и фраза
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
    
def wait_spiner(driver):
    driver.implicitly_wait(0)
    while True:
        els = driver.find_elements(By.XPATH, '//img[@class="preloader"]')
        if not els: break
        disp = els[0].get_attribute('style')
        if disp == 'display: none;': break
        time.sleep(1)
    driver.implicitly_wait(10)
    time.sleep(1)

def set_bid(data, bid_type):
    driver = None
    try:
        # base_url = 'https://oao.mgts.ru'
        data['delete_after'] = False
        login = data.get('login')
        pass_1 = data.get('password')
        if not login or not pass_1: raise Exception('Не задан первичный логин/пароль')
        base_url = f'https://{login}:{pass_1}@oao.mgts.ru'

        EXE_PATH = 'driver/chromedriver.exe'
        driver = webdriver.Chrome(executable_path=EXE_PATH)

        driver.implicitly_wait(10)
        driver.get(base_url)
        time.sleep(3)
        
        ###################### Login ######################
        els = driver.find_elements(By.ID, 'loginform-username')
        if len(els) != 1: raise Exception('Ошибка нет поля login')
        log_2 = data.get('login2')
        try:
            if log_2: els[0].send_keys(log_2)
            else: raise Exception('Ошибка не задан второй логин')
        except: raise Exception('Ошибка ввода логин')
        time.sleep(1)

        els = driver.find_elements(By.ID, 'loginform-password')
        if len(els) != 1: raise Exception('Ошибка нет поля пароль')
        pass_2 = data.get('password2')
        try:
            if pass_2: els[0].send_keys(pass_2)
            else: raise Exception('Ошибка не задан второй пароль')
        except: raise Exception('Ошибка ввода второй пароль')
        time.sleep(1)
        
        els = driver.find_elements(By.XPATH, '//button[@name="login-button"]')
        if len(els) != 1: raise Exception('Ошибка нет кнопки войти')
        try: els[0].click()
        except: raise Exception('Ошибка клика войти')
        time.sleep(5)
        
        driver.implicitly_wait(1)
        els = driver.find_elements(By.XPATH, '//div[@class="alert alert-danger"]')
        if els: raise Exception(els[0].text)
        driver.implicitly_wait(10)
        
        # ###################### Страница поиска адреса ######################  isElementPresent в цикле
        # поле Город
        city = data.get('city')
        if city:
            # Активируем поле ввода названия города
            els = driver.find_elements(By.XPATH, '//span[@id="select2-getCity-container"]')
            if len(els) != 1: raise Exception('Ошибка нет поля город')
            try: els[0].click()
            except: raise Exception('Ошибка активации поля ввода город')
            time.sleep(1)
            # Вводим город
            els = driver.find_elements(By.XPATH, '//input[@aria-controls="select2-getCity-results"]')
            if len(els) != 1: raise Exception('Ошибка нет поля ввода город')
            try: els[0].send_keys(city)
            except: raise Exception('Ошибка ввода город')
            time.sleep(3)
            # Смотрим подсказку
            els = driver.find_elements(By.XPATH, '//ul[@id="select2-getCity-results"]')
            if len(els) != 1: raise Exception('Ошибка нет списка подсказки город')
            els_li = els[0].find_elements(By.TAG_NAME, 'li')
            f_lst = []
            for i in range(len(els_li)):
                name_city = els_li[i].text
                f_lst.append((i, name_city))
                
                
            i_fnd = find_short_tup(f_lst)
            try: els_li[i_fnd].click()
            except: raise Exception('Ошибка выбора улица')

        # Разберем поле Улица
        street = data.get('street')
        if not street: raise Exception('Ошибка не заполнено поле улица')
        c_street = ordering_street(street)
        if not c_street: raise Exception(f'Ошибка {street} не распознано')
        # print(c_street)
        
        # Активируем поле ввода названия улицы
        els = driver.find_elements(By.XPATH, '//span[@aria-labelledby="select2-getStreet-container"]')
        if len(els) != 1: raise Exception('Ошибка нет поля улица')
        try: els[0].click()
        except: raise Exception('Ошибка активации поля ввода улица')
        time.sleep(1)
        # Вводим улицу
        els = driver.find_elements(By.XPATH, '//input[@class="select2-search__field"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода улица')
        try: els[0].send_keys(c_street[0])
        except: raise Exception('Ошибка ввода улица')
        time.sleep(3)
        # Смотрим подсказку
        els = driver.find_elements(By.XPATH, '//ul[@id="select2-getStreet-results"]')
        if len(els) != 1: raise Exception('Ошибка нет списка подсказки улица')
        els_li = els[0].find_elements(By.TAG_NAME, 'li')
        f_lst = []
        el_lst = []
        for el_li in els_li:
            name_street = el_li.text
            # print(name_street)
            if name_street == c_street[1]:
                el_lst.append(el_li)
                f_lst.append(name_street)
                break
        if len(f_lst) == 0: raise Exception(f'Ошибка нет вариантов {street}')
        if len(f_lst) == 1:
            try: el_lst[0].click()
            except: raise Exception('Ошибка выбора улица')
        else:
            # Множественный выбор
            raise Exception(f'Ошибка много вариантов улица: {";".join(f_lst)}')
        time.sleep(3)

        # Разберем поле дом
        house = data.get('house').strip()
        if not house: raise Exception('Ошибка не задан дом')
        c_house = ordering_house(house)
        if not c_house[0]: raise Exception(f'Ошибка распознавания дома: {c_house[1]}: \"{house}\".')
        # Активируем поле ввода номера дома
        els = driver.find_elements(By.XPATH, '//span[@aria-labelledby="select2-getHouse-container"]')
        if len(els) != 1: raise Exception('Ошибка нет поля дом')
        try: els[0].click()
        except: raise Exception('Ошибка активации поля ввода дом')
        time.sleep(1)
        # Вводим дом
        els = driver.find_elements(By.XPATH, '//input[@class="select2-search__field"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода дома')
        try: els[0].send_keys(c_house[0])
        except: raise Exception('Ошибка ввода дома')
        time.sleep(3)
        # Смотрим подсказку
        els = driver.find_elements(By.XPATH, '//ul[@id="select2-getHouse-results"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода дома')
        els_li = els[0].find_elements(By.TAG_NAME, 'li')
        f_lst = []
        el_lst = []
        for el_li in els_li:
            name_house = el_li.text
            # print(name_house)
            if name_house == c_house[1]:
                el_lst.append(el_li)
                f_lst.append(name_house)
                break
        if len(f_lst) == 0: raise Exception(f'Ошибка нет вариантов дома {house}')
        if len(f_lst) == 1:
            try: el_lst[0].click()
            except: raise Exception('Ошибка выбора дома')
        else:
            # Множественный выбор
            raise Exception(f'Ошибка много вариантов дома: {";".join(f_lst)}')
        time.sleep(3)

        # Квартира (ручной ввод - карандаш)
        apartment = data.get('apartment').strip()
        if not apartment: raise Exception('Ошибка не задана квартира')
        # Активируем поле ввода номера дома
        els = driver.find_elements(By.XPATH, '//span[@class="pencilFlat glyphicon glyphicon-pencil"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ручной ввод квартира')
        try: els[0].click()
        except: raise Exception('Ошибка активации поля ввода квартира')
        time.sleep(1)
        # Вводим квартира
        els = driver.find_elements(By.XPATH, '//input[@id="manualFlatInput"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода квартира')
        try: els[0].send_keys(apartment)
        except: raise Exception('Ошибка ввода квартира')
        time.sleep(1)
        # Жмем кнопку подтверждения ввода квартиры
        els = driver.find_elements(By.XPATH, '//button[contains(@onclick, "saveManualFlat")]')
        if len(els) != 1: raise Exception('Ошибка нет кнопки подтверждения ввода квартира')
        try: els[0].click()
        except: raise Exception('Ошибка клика кнопки подтверждения ввода квартира')
        time.sleep(2)

        # Жмем кнопку поиск клиента
        els = driver.find_elements(By.XPATH, '//button[@onclick="saveAddress();"]')
        if len(els) != 1: raise Exception('Ошибка нет кнопки Поиск клиента')
        try: els[0].click()
        except: raise Exception('Ошибка нажатия кнопки Поиск клиента')
        time.sleep(2)
        
        # Ждем спинер
        wait_spiner(driver)
        time.sleep(3)

        if bid_type == 'delete':
            # Жмем кнопку Удалить заказ
            els = driver.find_elements(By.XPATH, '//button[contains(@class, "buttonClosePreorder")]')
            if len(els) != 1: raise Exception('Ошибка нет кнопки удаления заказа')
            els[0].click()
            time.sleep(2)

            # Ждем всплывашку с выбором статуса заявки
            driver.implicitly_wait(0)
            while True:
                els_sel = driver.find_elements(By.XPATH, '//select[@id="commonform-preorderstatus"]')
                if els_sel[0]:
                    time.sleep(2)
                    try: els_sel[0].click()
                    except: raise Exception('Ошибка клика списка статуса заявки')
                    break
                time.sleep(1)
            driver.implicitly_wait(10)
            time.sleep(1)
            
            els_opt = els_sel[0].find_elements(By.TAG_NAME, 'option')
            if len(els_opt) == 0: raise Exception('Ошибка нет вариантов статуса заявки')
            for el_opt in els_opt:
                if el_opt.get_attribute('value') == 'SUBSCRIBER_REJECT_BEFORE_WFM':
                    try: el_opt.click()
                    except: raise Exception('Ошибка клика варианта статуса заявки')
            time.sleep(1)
            
            els = driver.find_elements(By.XPATH, '//button[@id="close-preorder-button"]')
            if len(els) != 1: raise Exception('Ошибка нет кнопки подтверждения статуса заявки')
            try: els[0].click()
            except: raise Exception('Ошибка клика кнопки подтверждения статуса заявки')
            time.sleep(10)
        
        elif bid_type == 'new':
            # Смотрим возможность подключения
            # Если в строке таблицы "Новый абонент" есть VIRT - то не заводим
            # А если PON или FTTX - то заводим
            f_techn = False
            els = driver.find_elements(By.XPATH, '//div[@class="panel-body"]/div')
            for el in els:
                content = el.text
                if content.find('Новый абонент') >= 0:
                    if content.find('PON') >= 0 or content.find('FTTX') >= 0:
                        f_techn = True
                        el_radio = el.find_elements(By.XPATH, './/input[@type="radio"]')
                        if el_radio:
                            try: el_radio[0].click()
                            except: raise Exception('Ошибка выбора нового клиента')
                            time.sleep(1)
                            break
                        else: raise Exception('Ошибка нет радиокнопки выбора нового клиента')
                    
            if not f_techn: raise Exception('Нет ТхВ')
            
            # Жмем кнопку Продажа/Допродажа МТС
            els = driver.find_elements(By.XPATH, '//button[@preorder_type_name="Mts_Sale"]')
            if len(els) != 1: raise Exception('Ошибка нет кнопки Продажа/Допродажа МТС')
            try: els[0].click()
            except: raise Exception('Ошибка нажатия кнопки Продажа/Допродажа МТС')
            data['delete_after'] = True
            time.sleep(2)
            
            # Ждем спинер
            wait_spiner(driver)
            time.sleep(2)
            
            # Канал работы с заявкой
            # Определяем канал Диллер
            els_ch = driver.find_elements(By.XPATH, '//select[@id="channel"]')
            if len(els_ch) != 1: raise Exception('Ошибка нет поля Канал')
            try: els_ch[0].click()
            except: raise Exception('Ошибка клика поля Канал')
            time.sleep(1)
            els_opt = els_ch[0].find_elements(By.TAG_NAME, 'option')
            if len(els_opt) == 0: raise Exception('Ошибка вариантов Канал')
            for el_opt in els_opt:
                if el_opt.get_attribute('value') == 'DEALER':
                    try: el_opt.click()
                    except: raise Exception('Ошибка клика выбора DEALER')
                    break
            time.sleep(1)
            # Определяем Диллер Домконнект
            els_dlr = driver.find_elements(By.XPATH, '//select[@id="source"]')
            if len(els_dlr) != 1: raise Exception('Ошибка нет поля Компания')
            try: els_dlr[0].click()
            except: raise Exception('Ошибка клика поля Компания')
            time.sleep(1)
            els_opt = els_dlr[0].find_elements(By.TAG_NAME, 'option')
            if len(els_opt) == 0: raise Exception('Ошибка вариантов Компания')
            for el_opt in els_opt:
                if el_opt.get_attribute('value') == 'DEALER.DOMCONNECT':
                    try: el_opt.click()
                    except: raise Exception('Ошибка клика выбора DEALER')
                    break
            time.sleep(2)
            
            # Заполняем услуги технологии PON
            els_serv = driver.find_elements(By.XPATH, '//div[@id="activeService"]')
            if len(els_serv) != 1: raise Exception('Ошибка нет блока услуг')
            # Передвинем страницу чтоб элемент стал видимым
            driver.execute_script("arguments[0].scrollIntoView();", els_serv[0])
            time.sleep(1)
            # отмечаем поле интернет
            els_i = els_serv[0].find_elements(By.XPATH, './/input[@passvarname="Интернет"]')
            if len(els_i) != 1: raise Exception('Ошибка нет поля Интернет')
            check = els_i[0].get_attribute('checked')
            # print('check', check)
            if not check:
                try: els_i[0].click()
                except: raise Exception('Ошибка клика поля Интернет')
                time.sleep(3)
            # услуга ТВ
            count_tv = data['count_tv']
            try:
                count_tv = int(count_tv)
                if count_tv > 3: raise Exception()
            except: raise Exception('Ошибка входных данных (0 <= count_tv <= 3)')
            # отмечаем услугу ТВ
            if count_tv:
                els_t = els_serv[0].find_elements(By.XPATH, './/input[@passvarname="Телевидение"]')
                if len(els_t) != 1: raise Exception('Ошибка нет поля Телевидение')
                check = els_t[0].get_attribute('checked')
                # print('checkTV', check)
                if not check:
                    try: els_t[0].click()
                    except: raise Exception('Ошибка клика поля Телевидение')
                    time.sleep(3)
                count_tv -= 1
                # отмечаем поле мультирум
                if count_tv:
                    els_m = els_serv[0].find_elements(By.XPATH, './/select[@passvarname="Мультирум"]')
                    if len(els_m) != 1: raise Exception('Ошибка нет поля Мультирум')
                    try: els_m[0].click()
                    except: raise Exception('Ошибка клика поля Мультирум')
                    time.sleep(2)
                    els_opt = els_m[0].find_elements(By.TAG_NAME, 'option')
                    if len(els_opt) == 0: raise Exception('Ошибка вариантов поля Мультирум')
                    for el_opt in els_opt:
                        if el_opt.get_attribute('value') == str(count_tv):
                            try: el_opt.click()
                            except: raise Exception('Ошибка клика выбора Мультирум')
                            break
                    time.sleep(1)
                    
            # Жмем кнопку Далее
            cnt = 10
            while True:
                time.sleep(1)
                cnt -= 1
                if cnt == 0: raise Exception('Ошибка превышено ожидание кнопки Далее(шаг два)')
                els = driver.find_elements(By.XPATH, '//button[@id="toStepTwo"]')
                if len(els) != 1: raise Exception('Ошибка нет кнопки Далее(шаг два)')
                dis = els[0].get_attribute('disabled')
                if dis: continue
                try: els[0].click()
                except: raise Exception('Ошибка клика кнопки Далее(шаг два)')
                break
            
            
            time.sleep(2)
            
            # Ждем спинер
            wait_spiner(driver)
            time.sleep(2)
            
            # Шаг 2: Выбор оборудования   (Видео 16:50)
            # WIFI_ROUTER
            wifi_router = data['wifi_router'].strip()
            if wifi_router:
                # Открываем список
                els = driver.find_elements(By.XPATH, '//select[@id="device-2-cpeid"]')
                if len(els) != 1: raise Exception('Ошибка нет списка оборудования wifi')
                try: els[0].click()
                except: raise Exception('Ошибка клика списка оборудования wifi')
                time.sleep(1)
                # Выбираем тип оборудования
                els_opt = els[0].find_elements(By.TAG_NAME, 'option')
                if len(els_opt) == 0: raise Exception('Ошибка вариантов оборудования wifi')
                f_ok = False
                for el_opt in els_opt:
                    if el_opt.text.strip() == wifi_router:
                        try: el_opt.click()
                        except: raise Exception('Ошибка клика выбора оборудования wifi')
                        f_ok = True
                        break
                if f_ok == False:
                    try: els_opt[-1].click()
                    except: raise Exception('Ошибка клика выбора оборудования wifi')
                time.sleep(2)
            
            # TV_ADAPTER
            tv_adapter = data['tv_adapter'].strip()
            if tv_adapter:
                els_block = driver.find_elements(By.XPATH, '//div[@passvarname="ТВ-приставка"]')
                if len(els_block) == 0: raise Exception('Ошибка нет блоков выбора ТВ-приставка')
                for el_block in els_block:
                    # Открываем список
                    els = el_block.find_elements(By.XPATH, './/select[@cpeid="cpeTitle"]')
                    if len(els) != 1: raise Exception('Ошибка нет списка оборудования ТВ-приставка')
                    try: els[0].click()
                    except: raise Exception('Ошибка клика списка оборудования ТВ-приставка')
                    time.sleep(2)
                    # Выбираем тип оборудования
                    els_opt = els[0].find_elements(By.TAG_NAME, 'option')
                    if len(els_opt) == 0: raise Exception('Ошибка вариантов оборудования ТВ-приставка')
                    f_ok = False
                    for el_opt in els_opt:
                        if el_opt.text.strip() == tv_adapter:
                            try: el_opt.click()
                            except: raise Exception('Ошибка клика выбора оборудования ТВ-приставка')
                            f_ok = True
                            break
                    if f_ok == False:
                        try: els_opt[-1].click()
                        except: raise Exception('Ошибка клика выбора оборудования ТВ-приставка')
                    time.sleep(2)
                    
            # Жмем кнопку Далее
            cnt = 10
            while True:
                time.sleep(1)
                cnt -= 1
                if cnt == 0: raise Exception('Ошибка превышено ожидание кнопки Далее(шаг три)')
                els = driver.find_elements(By.XPATH, '//button[@id="next-step"]')
                if len(els) != 1: raise Exception('Ошибка нет кнопки Далее(шаг три)')
                dis = els[0].get_attribute('disabled')
                if dis: continue
                try: els[0].click()
                except: raise Exception('Ошибка клика кнопки Далее(шаг три)')
                break
            
            time.sleep(3)
            # Ждем спинер
            wait_spiner(driver)
            time.sleep(2)
            
            # Шаг 3: Тарифный план   (Видео 21:50)
            tarif = data['tarif'].strip()
            if not tarif: raise Exception('Ошибка не задан тариф')
            els_sp = driver.find_elements(By.XPATH, '//span[@aria-labelledby="select2-decreeMain-container"]')
            if len(els_sp) != 1: raise Exception('Ошибка нет поля выбора тариф')
            try: els_sp[0].click()
            except: raise Exception('Ошибка клика поля выбора тариф')
            time.sleep(2)
            
            els = driver.find_elements(By.XPATH, '//ul[@id="select2-decreeMain-results"]')
            if len(els) != 1: raise Exception('Ошибка нет списка выбора тариф')
            # Выбираем Тариф
            els_opt = els[0].find_elements(By.TAG_NAME, 'li')
            if len(els_opt) == 0: raise Exception('Ошибка вариантов выбора тариф')
            f_ok = False
            lst = []
            for el_opt in els_opt:
                tar = el_opt.text.strip()
                lst.append(tar)
                if tar == tarif:
                    try: el_opt.click()
                    except: raise Exception('Ошибка клика выбора тариф')
                    f_ok = True
                    break
            if f_ok == False: raise Exception(f'Ошибка тариф {tarif} не найден. Есть: {";".join(lst)}')
            time.sleep(2)
            
            # Жмем кнопку сохранить
            cnt = 10
            while True:
                time.sleep(1)
                cnt -= 1
                if cnt == 0: raise Exception('Ошибка превышено ожидание кнопки сохранить(шаг 4)')
                els = driver.find_elements(By.XPATH, '//button[@id="savePackage"]')
                if len(els) != 1: raise Exception('Ошибка нет кнопки сохранить')
                dis = els[0].get_attribute('disabled')
                if dis: continue
                try: els[0].click()
                except: raise Exception('Ошибка клика кнопки сохранить')
                break
            
            time.sleep(1)

            # Жмем кнопку Далее
            cnt = 10
            while True:
                time.sleep(1)
                cnt -= 1
                if cnt == 0: raise Exception('Ошибка превышено ожидание кнопки Далее(шаг 4)')
                els = driver.find_elements(By.XPATH, '//button[@id="next-step"]')
                if len(els) != 1: raise Exception('Ошибка нет кнопки Далее(шаг 4)')
                dis = els[0].get_attribute('disabled')
                if dis: continue
                try: els[0].click()
                except: raise Exception('Ошибка клика кнопки Далее(шаг 4)')
                break

            time.sleep(3)
            # Ждем спинер
            wait_spiner(driver)
            time.sleep(2)

            # Шаг 4: Информация об абоненте   (Видео 23:50)
            # Фамилия
            lastname = data['lastname']
            if not lastname: lastname = '_'
            els = driver.find_elements(By.XPATH, '//input[@id="infomainform-surname"]')
            if len(els) != 1: raise Exception('Ошибка нет поля фамилия')
            try: els[0].send_keys(lastname)
            except: raise Exception('Ошибка ввода фамилия')
            time.sleep(1)
            # Имя
            firstname = data['firstname']
            if not firstname: firstname = '_'
            els = driver.find_elements(By.XPATH, '//input[@id="infomainform-name"]')
            if len(els) != 1: raise Exception('Ошибка нет поля Имя')
            try: els[0].send_keys(firstname)
            except: raise Exception('Ошибка ввода Имя')
            time.sleep(1)
            # Отчество
            patronymic = data['patronymic']
            if patronymic:
                els = driver.find_elements(By.XPATH, '//input[@id="infomainform-patronymicname"]')
                if len(els) != 1: raise Exception('Ошибка нет поля Отчество')
                try: els[0].send_keys(patronymic)
                except: raise Exception('Ошибка ввода Отчество')
                time.sleep(1)
                
            # Чекбокс данные по умолчанию
            els = driver.find_elements(By.XPATH, '//input[@id="infomainform-isdefaultpersonaldata"]')
            if len(els) != 1: raise Exception('Ошибка нет поля данные по умолчанию')
            try: els[0].click()
            except: raise Exception('Ошибка клика данные по умолчанию')
            time.sleep(1)
            # Чекбокс адрес регистрации
            els = driver.find_elements(By.XPATH, '//input[@id="infomainform-equaltdregaddress"]')
            if len(els) != 1: raise Exception('Ошибка нет поля адрес регистрации')
            try: els[0].click()
            except: raise Exception('Ошибка клика адрес регистрации')
            time.sleep(1)
            
            # Телефон
            phone = data['phone']
            if not phone: raise Exception('Ошибка нет поля адрес регистрации')
            els = driver.find_elements(By.XPATH, '//input[@id="infomainform-contactmobphone"]')
            if len(els) != 1: raise Exception('Ошибка нет поля Телефон')
            try: els[0].send_keys(phone[2:])
            except: raise Exception('Ошибка ввода Телефон')
            time.sleep(1)
            
            # Доставка счета
            els = driver.find_elements(By.XPATH, '//select[@id="infomainform-deliverytype"]')
            if len(els) != 1: raise Exception('Ошибка нет поля Доставка счета')
            try: els[0].click()
            except: raise Exception('Ошибка клика данные по умолчанию')
            time.sleep(1)
            els_opt = els[0].find_elements(By.TAG_NAME, 'option')
            if len(els_opt) == 0: raise Exception('Ошибка вариантов выбора Доставка счета')
            try: els_opt[-1].click()
            except: raise Exception('Ошибка клика Доставка счета')
            time.sleep(2)
            
            # Жмем кнопку Далее
            cnt = 10
            while True:
                time.sleep(1)
                cnt -= 1
                if cnt == 0: raise Exception('Ошибка превышено ожидание кнопки Далее(шаг 5)')
                els = driver.find_elements(By.XPATH, '//button[@id="next-step"]')
                if len(els) != 1: raise Exception('Ошибка нет кнопки Далее(шаг 5)')
                dis = els[0].get_attribute('disabled')
                if dis: continue
                try: els[0].click()
                except: raise Exception('Ошибка клика кнопки Далее(шаг 5)')
                break
            
            time.sleep(3)
            # Ждем спинер
            wait_spiner(driver)
            time.sleep(2)

            # Шаг 5: Утверждение списка услуг   (Видео 27:40)
            # Берем номер заявки
            # Развернуть страницу на весь экран
            driver.fullscreen_window()
            time.sleep(2)
            els_div = driver.find_elements(By.XPATH, '//div[contains(@class, "step1PhoneNumber")]')
            if len(els_div) != 1: raise Exception('Ошибка нет поля с номером заказа')
            cont = els_div[0].text
            lst_cont = cont.split(':')
            if len(lst_cont) != 2: raise Exception('Ошибка формат поля с номером заказа не распознан')
            data['bid_number'] = lst_cont[1].strip()
            
            # Жмем кнопку Далее
            els = driver.find_elements(By.XPATH, '//button[@id="toSeventhStep"]')
            if len(els) != 1: raise Exception('Ошибка нет кнопки Далее(шаг 6)')
            try: els[0].click()
            except: raise Exception('Ошибка клика кнопки Далее(шаг 6)')
            time.sleep(2)
            
            
            # Модальное окно подтверждения
            els_div = driver.find_elements(By.XPATH, '//div[@id="modalForm"]')
            if len(els_div) != 1: raise Exception('Ошибка нет окна подтверждения заказа')
            els_btn = els_div[0].find_elements(By.XPATH, './/button[@id="modalOkButton"]')  # Подтвердить
            # els_btn = els_div[0].find_elements(By.XPATH, './/button[@id="modalExtraButton"]')  # Отмена
            if len(els_btn) != 1: raise Exception('Ошибка нет кнгопки ОК окна подтверждения заказа')
            try: els_btn[0].click()
            except: raise Exception('Ошибка клика кнопки ОК окна подтверждения заказа')
            
            time.sleep(3)
            # Ждем спинер
            wait_spiner(driver)
            time.sleep(2)
            
            # Шаг 7: Работа с нарядами (назначение в график)   (Видео 28:00)
            # Заполним поле комментарий
            comment = data['comment']
            if comment:
                els = driver.find_elements(By.XPATH, '//textarea[@id="commonform-comment"]')
                if len(els) != 1: raise Exception('Ошибка нет поля комментарий')
                try: els[0].send_keys(comment)
                except: raise Exception('Ошибка ввода комментарий')
                time.sleep(1)

            # График наряда
            tp_grafic = data.get('tp_grafic')
            try: int_grafic = int(tp_grafic)
            except: raise Exception(f'Ошибка заданного значения tp_grafic: {tp_grafic} (0-3)')
            if int_grafic < 0 or int_grafic > 3: raise Exception(f'Ошибка заданного значения tp_grafic: {tp_grafic} (0-3)')
            if int_grafic > 0:
                # Изменим конечную дату
                els = driver.find_elements(By.XPATH, '//input[@id="step7form-intervalfinish"]')
                if len(els) != 1: raise Exception('Ошибка нет поля даты окончания')
                fin_data = els[0].get_attribute('value')
                dt_fin = datetime.strptime(fin_data, '%d.%m.%Y')  # дата в формате 13.01.2022 надо прибавить 3 дня
                dt_fin2 = dt_fin + timedelta(days=3)
                s_dt_fin2 = dt_fin2.strftime('%d.%m.%Y')
                try:
                    els[0].send_keys(Keys.CONTROL + 'a')
                    time.sleep(0.2)
                    els[0].send_keys(Keys.DELETE)
                    time.sleep(0.2)
                    els[0].send_keys(s_dt_fin2)
                    time.sleep(0.2)
                except: raise Exception('Ошибка ввода конечной даты')
                # Жмем кнопку Подобрать
                els_btn = driver.find_elements(By.XPATH, '//button[@id="getWFMComplex"]')
                if len(els_btn) != 1: raise Exception('Ошибка нет кнопки Подобрать таймслот')
                try: els_btn[0].click()
                except: raise Exception('Ошибка клика кнопки Подобрать таймслот')
                time.sleep(10)
                # Откроем таймслоты
                els_div_ts = driver.find_elements(By.XPATH, '//div[@id="newTimeslot"]')
                if len(els_div_ts) != 1: raise Exception('Ошибка нет окна таймслот')
                els_ts = els_div_ts[0].find_elements(By.TAG_NAME, 'input')
                if len(els_ts) == 0: raise Exception('Ошибка нет доступных таймслот')
                lst_ts = []
                try:
                    for el_ts in els_ts:
                        # Начало таймслота (appointmentstart="2022-01-13T14:00:00")
                        ts_row = el_ts.get_attribute('appointmentstart')
                        lst_st = ts_row.split('T')
                        dt_gr = datetime.strptime(lst_st[0], '%Y-%m-%d')
                        s_date = dt_gr.strftime('%d.%m.%Y')
                        out_lst = [s_date,]
                        ts_hour = lst_st[1].split(':')[0]
                        out_lst.append(ts_hour)
                        # Окончание таймслота (appointmentfinish="2022-01-13T16:00:00")
                        ts_row = el_ts.get_attribute('appointmentfinish')
                        lst_st = ts_row.split('T')
                        ts_hour = lst_st[1].split(':')[0]
                        out_lst.append(ts_hour)
                        lst_ts.append(out_lst)
                except: raise Exception('Ошибка парсинга доступных таймслот')
                
                err_mess_grafic = ''
                if int_grafic == 1:  # В график на ближайший таймслот
                    try: els_ts[0].click()
                    except: raise Exception('Ошибка клика таймслота')
                    time.sleep(2)
                
                elif int_grafic == 2:  # В график по значению dt_grafic
                    dt_grafic = data.get('dt_grafic')
                    if not dt_grafic: raise Exception(f'Ошибка заданного dt_grafic {dt_grafic}')
                    try:
                        dt_gr = dt_grafic.split(' ')
                        t_date = dt_gr[0]
                        t_start = dt_gr[1]
                    except: raise Exception(f'Ошибка заданного dt_grafic {dt_grafic}')
                    f_ind = -1
                    for i in range(len(lst_ts)):
                        if lst_ts[i][0] == t_date and lst_ts[i][1] >= t_start:
                            f_ind = i
                            break
                    if f_ind >= 0: 
                        try: els_ts[f_ind].click()
                        except: raise Exception('Ошибка клика таймслота')
                        time.sleep(2)
                    else:
                        err_mess_grafic = f'Ошибка Заданный таймслот {dt_grafic} не найден. '
                if int_grafic == 3 or err_mess_grafic:
                    new_lst = [f'{d} {s}-{f}' for d, s, f in lst_ts]
                    err_mess_grafic += f'Доступны таймслоты: {"; ".join(new_lst)}'
                    raise Exception(err_mess_grafic)
                    
                # Заполним поле комментарий
                if not comment: comment = 'Без комментария'
                els = driver.find_elements(By.XPATH, '//input[@id="step7form-comment"]')
                if len(els) != 1: raise Exception('Ошибка нет поля комментарий2')
                try: els[0].send_keys(comment)
                except: raise Exception('Ошибка ввода комментарий2')
                time.sleep(1)
                # Жмем кнопку создать наряд
                data['delete_after'] = False
                els_btn = els_div_ts[0].find_elements(By.XPATH, './/button[@id="create-new0"]')
                if len(els_btn) != 1: raise Exception('Ошибка нет кнопки создать наряд')
                driver.execute_script("arguments[0].scrollIntoView();", els_btn[0])
                time.sleep(1)
                try: els_btn[0].click()
                except: raise Exception('Ошибка клика кнопки создать наряд')
                time.sleep(2)
                    
                # отлавливаем всплывающее окно
                els_div_mf = None
                cnt = 60
                while True:
                    if cnt == 0: raise Exception('Ошибка превышено ожидание окна подтверждения на выполнение работ')
                    els_div_mf = driver.find_elements(By.XPATH, '//div[@id="modalForm"]')
                    if len(els_div_mf) != 1: raise Exception('Ошибка нет окна подтверждения выполнения работ')
                    els_div = els_div_mf[0].find_elements(By.XPATH, './/div[@class="modal-body"]')
                    if len(els_div) != 1: raise Exception('Ошибка окно подтверждения выполнения работ нет контента')
                    cont = els_div[0].text
                    if len(cont) < 10:
                        cnt -= 1
                        time.sleep(1)
                        continue
                    cont = cont.replace('Номер заявки:', '\nЗаявка на монтаж: ')
                    data['bid_number'] += cont
                    break
                    
                # Жмем Отправить в работу
                els_btn = els_div_mf[0].find_elements(By.XPATH, './/button[@id="modalOkButton"]')
                # els_btn = els_div_mf[0].find_elements(By.XPATH, './/button[@id="modalExtraButton"]')
                if len(els_btn) != 1: raise Exception('Ошибка нет кнопки Отправить в работу')
                driver.execute_script("arguments[0].scrollIntoView();", els_btn[0])
                time.sleep(1)
                try: els_btn[0].click()
                except: raise Exception('Ошибка клика кнопки Отправить в работу')
                time.sleep(5)
                return '', data
                
            # Жмем кнопку Далее (на печать документов)
            els = driver.find_elements(By.XPATH, '//button[contains(@class, "preloaderShow")]')
            if len(els) != 1: raise Exception('Ошибка нет кнопки Далее(шаг 7)')
            try: els[0].click()
            except: raise Exception('Ошибка клика кнопки Далее(шаг 7)')
            time.sleep(5)



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

def set_bid_to_dj_domconnect():
    url = url_host + 'api/set_bid_mgts'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    # params = {
        # 'key': 'Q8kGM1HfWz',
        # 'login': 'ESubbotin',
        # 'password': 'AsCbbb14',
        # 'login2': 'MChumakova',
        # 'password2': 'Zse@!5587',
        # 'id_lid': '1255948',
        
        # 'city': 'Москва',           # город
        # 'street': 'улица Винокурова',         # улица
        # 'house': '7/5 кор. 2',          # дом
        # 'apartment': '24',          # квартира  17 18

        # # 'wifi_router': 'D-Link DIR-842/S',  # тип роутера(если название не найдется - выберется первый по списку), если не нужен - оставляем пусто
        # 'wifi_router': '',
        # 'count_tv': '1',  # Количество телевизоров (до 3-х) Если ТВ не нужно - 0
        # 'tv_adapter': 'EKT DID 7005',
        # 'tarif': 'МТС Home. GPON 200 Мбит/с', # тарифный план
        # 'tp_grafic': '3',  # 0 - без назначения в график; 1 - в график на ближайший тс; 2 - в график по dt_grafic; 3 - запрос тс без заведения заявки
        # 'dt_grafic': '16.01.2022 14',
        
        # 'firstname': 'Иван',
        # 'patronymic': 'Степанович',
        # 'lastname': 'Федоров',
        # 'phone': '79011111111',
        # 'comment': 'Тестовая заявка, просьба не обрабатывать',          # коментарий обязательно: подъезд этаж
        # 'bid_number': '',          # номер заявки
    # }
    params = {
        'key': 'Q8kGM1HfWz',
        'login': 'ESubbotin',
        'password': 'AsCbbb14',
        'login2': 'MChumakova',
        'password2': 'Zse@!5587',
        'id_lid': '1255948',
        
        'city': 'Москва',           # город
        'street': 'улица Винокурова',         # улица
        'house': '7/5 кор. 2',          # дом
        'apartment': '24',          # квартира  17 18

        # 'wifi_router': 'D-Link DIR-842/S',  # тип роутера(если название не найдется - выберется первый по списку), если не нужен - оставляем пусто
        'wifi_router': '',
        'count_tv': '1',  # Количество телевизоров (до 3-х) Если ТВ не нужно - 0
        'tv_adapter': 'EKT DID 7005',
        'tarif': 'МТС Home. GPON 200 Мбит/с', # тарифный план
        'tp_grafic': '3',  # 0 - без назначения в график; 1 - в график на ближайший тс; 2 - в график по dt_grafic; 3 - запрос тс без заведения заявки
        'dt_grafic': '16.01.2022 14',
        
        'firstname': 'Иван',
        'patronymic': 'Степанович',
        'lastname': 'Федоров',
        'phone': '79011111111',
        'comment': 'Тестовая заявка, просьба не обрабатывать',          # коментарий обязательно: подъезд этаж
        'bid_number': '',          # номер заявки
    }
    
    try:
        responce = requests.get(url, headers=headers, params=params)
        print(responce.status_code)
        print(responce.text)
    except:
        print('Error: requests.get')

def get_bid_in_dj_domconnect():
    url = url_host + 'api/get_bid_mgts'
    
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
    url = url_host + 'api/set_bid_mgts_status'
    
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

    params = {
        'id': bid_dict.get('id_lid'),
        'fields[UF_CRM_5864F4DAAC508]': f'Заявка: {bid_dict.get("bid_number")}',
        'fields[UF_CRM_1493413514]': 11,
        'fields[UF_CRM_5864F4DA85D5A]': bid_dict.get('tarif'),
        'fields[UF_CRM_1499386906]': 523  # PartnerWEB
    }
    error_message = bid_dict.get("bot_log")
    if error_message:
        params['fields[UF_CRM_5864F4DAAC508]'] = error_message

    try:
        responce = requests.post(url, headers=headers, params=params)
    except:
        pass
        # посмотреть результат https://crm.domconnect.ru/crm/lead/details/1215557/

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

def run_bid_mgts(tlg_chat, tlg_token):
    opsos = 'МГТС'
    
    # личный бот @infra
    TELEGRAM_CHAT_ID = '1740645090'
    TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'
    
    rez, bid_list = get_bid_in_dj_domconnect()
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
        rez, data = set_bid(bid_dict, 'new')
        delete_after = data.get('delete_after')
        if delete_after: rez1, data = set_bid(data, 'delete')
        if rez1: rez += rez1
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
            address = f'{data.get("city")} {data.get("street")} д.{data.get("house")} кв.{data.get("apartment")}'
            fio = f'{data.get("firstname")} {data.get("patronymic")} {data.get("lastname")}'
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'Адрес: {address}\n'
            tlg_mess += f'ФИО: {fio}\n'
            tlg_mess += f'{data.get("bot_log")}\n'
        r = send_telegram(tlg_chat, tlg_token, tlg_mess)
        print(tlg_mess)
        print('TelegramMessage:', r)
    #================================================


if __name__ == '__main__':
    start_time = datetime.now()
    
    # url: https://oao.mgts.ru

    
    # bid_dict = {
        # 'login': 'ESubbotin',
        # 'password': 'AsCbbb14',
        # 'login2': 'MChumakova',
        # 'password2': 'Zse@!5587',
        
        # 'id_lid': '1255948',
        
        # 'city': 'Москва',           # город
        # 'street': 'улица Винокурова',         # улица
        # 'house': '7/5 кор. 2',          # дом
        # 'apartment': '24',          # квартира  17 18
        
        # # 'wifi_router': 'D-Link DIR-842/S',  # тип роутера(если название не найдется - выберется первый по списку), если не нужен - оставляем пусто
        # 'wifi_router': '',
        # 'count_tv': '1',  # Количество телевизоров (до 3-х) Если ТВ не нужно - 0
        # 'tv_adapter': 'EKT DID 7005',
        # 'tarif': 'МТС Home. GPON 200 Мбит/с', # тарифный план
        # 'tp_grafic': '3',  # 0 - без назначения в график; 1 - в график на ближайший тс; 2 - в график по dt_grafic; 3 - запрос тс без заведения заявки
        # 'dt_grafic': '16.01.2022 14',
        
        # 'firstname': '',
        # 'patronymic': '',
        # 'lastname': '',
        # 'phone': '79011111111',
        # 'comment': 'Тестовая заявка, просьба не обрабатывать',          # коментарий обязательно: подъезд этаж
        # 'bid_number': '',          # номер заявки
    # }
    
    
    # e, data = set_bid(bid_dict, 'new')
    # if e: print(e)
    # print('bid_number', data['bid_number'])
    # time.sleep(2)
    
    # delete_after = data.get('delete_after')
    # if delete_after: rez1, data = set_bid(data, 'delete')
    



    
    set_bid_to_dj_domconnect()
    # rez, bid_list = get_bid_in_dj_domconnect()
    # for bid_dict in bid_list:
        # for k, v in bid_dict.items():
            # print(k, v)
    # data = {'id': 1, 'bot_log': 'Заявка принята МГТС'}
    # r = set_bid_status(0, data)
    # print(r)
    
    end_time = datetime.now()
    print('\nDuration: {}'.format(end_time - start_time))
    
    pass
    
    '''
    Повисшие заявки
    
    117449, РФ, г. Москва, Винокурова ул., д.7/5,к.2, кв.22
    
    
    '''
