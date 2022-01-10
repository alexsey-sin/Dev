import os
import time
from datetime import datetime
import requests  # pip install requests
import json
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

url_host = 'http://127.0.0.1:8000/'
# url_host = 'http://django.domconnect.ru/'

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
        # print('spiner')
        els = driver.find_elements(By.XPATH, '//img[@class="preloader"]')
        if not els: break
        time.sleep(1)
    driver.implicitly_wait(10)
    time.sleep(1)

def set_bid(data):
    driver = None
    try:
        # base_url = 'https://oao.mgts.ru'
        
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
            raise Exception('Ошибка нет доступной технологии подключения')
        else: data['available_connect'] = 'Есть ТхВ'
        
        # Жмем кнопку Продажа/Допродажа МТС
        els = driver.find_elements(By.XPATH, '//button[@preorder_type_name="Mts_Sale"]')
        if len(els) != 1: raise Exception('Ошибка нет кнопки Продажа/Допродажа МТС')
        try: els[0].click()
        except: raise Exception('Ошибка нажатия кнопки Продажа/Допродажа МТС')
        time.sleep(2)
        
        # Ждем спинер
        wait_spiner(driver)
        time.sleep(2)
        
        driver.fullscreen_window()
        els = driver.find_elements(By.XPATH, '//div[@class="bs-callout bs-callout-mgts"]')
        # Смотрим определившийся адрес и ТхВ
        for el in els:
            content = el.text
            phr1 = 'Адрес:'
            i1 = content.find(phr1)
            if i1 >= 0:
                data['pv_address'] = content[i1+len(phr1):].strip()

        
        #===========
        time.sleep(10)
        with open('out.html', 'w', encoding='utf-8') as outfile:
            outfile.write(driver.page_source)
        raise Exception('Финиш.')
        #===========

        # #===========
        # time.sleep(10)
        # with open('out.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        # raise Exception('Финиш.')
        # #===========
        
    except Exception as e:
        return str(e), data,
    finally: driver.quit()   
    
    return '', data, 

def set_did_to_dj_domconnect():
    url = url_host + 'api/set_bid_mts'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
        'login': 'ESubbotin',
        'password': 'AsCbbb14',
        'login_2': 'MChumakova',
        'password_2': 'Zse@!5587',
        'id_lid': '1215557',
        
        'city': 'Москва',           # город
        'street': 'проезд Черепановых',         # улица
        'house': '38к1',          # дом
        'apartment': '6',          # квартира

        'tarif': 'ШПД (FTTB) ; ТЛФ (FTTB)', # Название тарифного плана
        'firstname': 'Иван',
        'patronymic': '',
        'lastname': '',
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

def get_did_in_dj_domconnect():
    url = url_host + 'api/get_bid_mts'
    
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
    url = url_host + 'api/set_bid_mts_status'
    
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
        'fields[UF_CRM_1493413514]': 2,
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
            address = f'{data.get("region")} {data.get("city")} {data.get("street")} д.{data.get("house")} кв.{data.get("apartment")}'
            fio = f'{data.get("firstname")} {data.get("patronymic")} {data.get("lastname")}'
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'Адрес: {address}\n'
            tlg_mess += f'ФИО: {fio}\n'
            tlg_mess += f'Ошибка: {data.get("bot_log")}\n'
        r = send_telegram(tlg_chat, tlg_token, tlg_mess)
        print(tlg_mess)
        print('TelegramMessage:', r)
    #================================================


if __name__ == '__main__':
    # start_time = datetime.now()
    
    # url: https://oao.mgts.ru

    
    bid_dict = {
        'login': 'ESubbotin',
        'password': 'AsCbbb14',
        'login_2': 'MChumakova',
        'password_2': 'Zse@!5587',
        
        'id_lid': '1215557',
        'city': 'Москва',           # город
        
        'street': 'улица Винокурова',         # улица
        'house': '7/5 кор. 2',          # дом
        'apartment': '11',          # квартира
        
        # 'street': 'Волоцкой переулок',         # улица
        # 'house': '7к1',          # дом
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
        

        'available_connect': '',  # Возможность подключения
        'tarifs_all': '', # список названий тарифных планов
        'pv_address': '',
    }
    
    
    e, data = set_bid(bid_dict)
    if e: print(e)
    print('pv_address', data['pv_address'])
    # # print(data['tarifs_all'])
    print('available_connect', data['available_connect'])
    
    
    # set_txv_to_dj_domconnect(pv_code)
    # rez, txv_list = get_txv_in_dj_domconnect(pv_code)
    # for txv_dict in txv_list:
        # for k, v in txv_dict.items():
            # print(k, v)
    # data = {'id': 1, 'pv_address': '55632145', 'bot_log': 'Заявка принята МТС'}
    # r = set_txv_status(0, data)
    # print(r)
    
    # end_time = datetime.now()
    # print('\nDuration: {}'.format(end_time - start_time))
    
    pass
