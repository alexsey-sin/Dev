import os
import time
from datetime import datetime
import requests  # pip install requests
from requests.auth import HTTPProxyAuth
import json
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'
opsos = 'МГТС'
pv_code = 7

    
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

def wait_spiner(driver):
    driver.implicitly_wait(0)
    while True:
        els = driver.find_elements(By.XPATH, '//img[@class="preloader"]')
        if not els: break
        time.sleep(1)
    driver.implicitly_wait(10)
    time.sleep(1)

def get_txv(data):
    driver = None
    try:
        # base_url = 'https://oao.mgts.ru'
        try:
            login = data.get('login')
            pass_1 = data.get('password')
            if not login or not pass_1: raise Exception('Не задан первичный логин/пароль')
            base_url = f'https://{login}:{pass_1}@oao.mgts.ru'

            EXE_PATH = 'driver/chromedriver.exe'
            driver = webdriver.Chrome(executable_path=EXE_PATH)
            time.sleep(1)
            driver.implicitly_wait(10)
            driver.get(base_url)
        except: raise Exception('Ошибка первичной авторизации')
        #===========
        time.sleep(3)
        
        ###################### Login ######################
        els = driver.find_elements(By.ID, 'loginform-username')
        if len(els) != 1: raise Exception('Ошибка нет поля login/Ошибка первичной авторизации')
        log_2 = data.get('login_2')
        try:
            if log_2: els[0].send_keys(log_2)
            else: raise Exception('Ошибка не задан второй логин')
        except: raise Exception('Ошибка ввода логин')
        time.sleep(1)

        els = driver.find_elements(By.ID, 'loginform-password')
        if len(els) != 1: raise Exception('Ошибка нет поля пароль')
        pass_2 = data.get('password_2')
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
        
        # Разберем поле Улица
        street = data.get('street')
        if not street: raise Exception('Ошибка не заполнено поле улица')
        c_street = ordering_street(street)
        if not c_street: raise Exception(f'Ошибка {street} не распознано')
        
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
        if len(els) != 1: raise Exception('Ошибка нет поля ввода улица')
        els_li = els[0].find_elements(By.TAG_NAME, 'li')
        f_lst = []
        el_lst = []
        for el_li in els_li:
            name_street = el_li.text
            # print(name_street)
            if name_street == c_street[1]:
                el_lst.append(el_li)
                f_lst.append(name_street)
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
                    else: raise Exception('Ошибка нет радиокнопки выбора нового клиента')
                
        if not f_techn:
            data['available_connect'] = 'Нет ТхВ'
        else: data['available_connect'] = 'Есть ТхВ'
        
        # Смотрим адрес (для бота ТхВ) если нет адреса - ошибку не выкидываем - просто выходим
        els_1 = driver.find_elements(By.XPATH, '//div[contains(@class, "customer bs-callout bs-callout-mgts")]')
        for el_1 in els_1:
            els_2 = el_1.find_elements(By.XPATH, './/div[contains(@class, "rowCustomer")]')
            for el_2 in els_2:
                if el_2.text.find('Адрес установки') >= 0:
                    els_3 = el_2.find_elements(By.XPATH, './/div[contains(@class, "rowDataCustomer")]')
                    if len(els_3): data['pv_address'] = els_3[0].text.strip()
                        

        time.sleep(2)
       
        
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
        
        # 'login': 'ESubbotin',
        # 'password': 'AsCbbb14',
        # 'login_2': 'MChumakova',
        # 'password_2': 'Zse@!5587',
        
        'login': 'MChumakova',
        'password': 'Qhvv@!4817',
        'login_2': 'ESubbotin',
        'password_2': 'NbVDa5Ty',
        'id_lid': '1215557',
        
        'city': 'Москва',           # город
        'street': 'проезд Черепановых',         # улица
        'house': '38к1',          # дом
        'apartment': '6',          # квартира

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

def run_txv_mgts(tlg_chat, tlg_token):
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
    # start_time = datetime.now()
    
    # url: https://oao.mgts.ru


    # 'login': 'MChumakova',
    # 'password': 'Dn4xVB#B',
    # 'login_2': 'MChumakova',
    # 'password_2': 'Qhvv@!4817',


    # 'login': 'ESubbotin',
    # 'password': 'sr@8Cjmu',
    # 'login_2': 'ESubbotin',
    # 'password_2': 'NbVDa5Ty',



    # txv_dict = {
        # 'pv_code': pv_code,
        # 'login': 'ESubbotin',
        # 'password': 'sr@8Cjmu',
        # 'login_2': 'MChumakova',
        # 'password_2': 'Qhvv@!4817',
        
        # # 'id_lid': '1215557',
        # 'city': 'Москва',           # город
        
        # # 'street': 'улица Винокурова',         # улица
        # # 'house': '7/5 кор. 2',          # дом
        # # 'apartment': '6',          # квартира
        
        # 'street': 'проезд Шокальского',         # улица
        # 'house': '35',          # дом
        # 'apartment': '6',          # квартира
        
        # # 'street': 'Щёлковское шоссе',         # улица
        # # 'house': '95',          # дом
        # # 'apartment': '6',          # квартира
        
        # # 'street': 'Липовая аллея',         # улица
        # # 'house': '16',          # дом
        # # 'apartment': '6',          # квартира
        
        # # 'street': 'проезд Черепановых',         # улица
        # # 'house': '38к1',          # дом
        # # 'apartment': '6',          # квартира
        
        # # 'street': 'Лужнецкая набережная',         # улица
        # # 'house': '24с17',          # дом
        # # 'apartment': '6',          # квартира
        
        # # 'street': 'Биржевая площадь',         # улица
        # # 'house': '1',          # дом
        # # 'apartment': '6',          # квартира
        
        # # 'street': 'Никитский бульвар',         # улица
        # # 'house': '11/12с1',          # дом
        # # 'apartment': '6',          # квартира
        
        # # 'street': 'Зелёный проспект',         # улица
        # # 'house': '44',          # дом
        # # 'apartment': '6',          # квартира
        

        # 'available_connect': '',  # Возможность подключения
        # 'tarifs_all': '', # список названий тарифных планов
        # 'pv_address': '',
    # }
    
    
    # e, data = get_txv(txv_dict)
    # if e: print(e)
    # print('pv_address', data['pv_address'])
    # # print(data['tarifs_all'])
    # print('available_connect', data['available_connect'])
    
    
    # set_txv_to_dj_domconnect(pv_code)
    # rez, txv_list = get_txv_in_dj_domconnect(pv_code)
    # for txv_dict in txv_list:
        # for k, v in txv_dict.items():
            # print(k, v)
    # data = {'id': 1, 'pv_address': '55632145', 'bot_log': 'Заявка принята МТС'}
    # r = set_txv_status(0, data)
    # print(r)
    
    # rez, stre = search_for_an_entry(lst_street, 'Светла')
    # rez = search_for_an_entry(lst_reg, 'ярославль')
    # rez = search_for_an_entry(lst_reg, 'Санкт-Петербург')
    
    
    
    pass
    
    # end_time = datetime.now()
    # time_str = '\nDuration: {}'.format(end_time - start_time)
    # print(time_str)
    # limit_request_line

