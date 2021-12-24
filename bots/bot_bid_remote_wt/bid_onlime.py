import os
import time
import re
from datetime import datetime
import requests  # pip install requests
import json


# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'
url_onlime = 'https://dealer.onlime.ru'  # Рабочий


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
        lst_house[1] = 'корпус'
        return (lst_house[0], ' '.join(lst_house))
    if lst_house[1].find('л') >= 0:
        lst_house[1] = 'литер'
        return (lst_house[0], ' '.join(lst_house))
    if lst_house[1].find('стр') >= 0:
        lst_house[1] = 'строение'
        return (lst_house[0], ' '.join(lst_house))
    
    return ('', 'Номер не распознан')

def get_token(login: str, password: str) -> (str, str):
    url = url_onlime + '/api/dealer/authorize'
    
    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    data = {
        'login': login,
        'password': password,
    }
    try:
        responce = requests.post(url, headers=headers, json=data)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            resp_code = answer.get('resp_code')
            if resp_code != 0: return 'Error', f'get_token: resp_code={resp_code}'
            access_token = answer.get('access_token', 'None')
            # expires_in = answer.get('expires_in')
            return '', access_token
        else:
            return f'Ошибка get_token: responce.status_code: {responce.status_code}\n{responce.text}', ''

        # {"resp_code":0,"access_token":"y9Hhze7_eiigdE1xa91-VCjHVgpvFkg8","expires_in":28800}
    except:
        return 'Ошибка get_token: try: requests.post', ''
   
def get_streets(token: str, street: str) -> (str, list):
    url = url_onlime + '/api/dealer/addr/addrstreets'
    
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Authorization': token,
    }
    params = {
        'txt': street,
    }

    try:
        responce = requests.get(url, headers=headers, params=params)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            if type(answer) == dict:
                resp_code = answer.get('resp_code')
                resp_description = answer.get('resp_description')
                if resp_code and resp_description:
                    if resp_code == 1: return f'Ошибка улица: \"{street}\" не найдена.', []
                    elif resp_code == -1: return f'Ошибка запроса get_streets: {resp_description}', []
                    else: return f'Ошибка get_streets: resp_code: {resp_code}\n{resp_description}', []
                else:
                    return 'Ошибка get_streets: dict: не распознан ответ', []
            elif type(answer) == list:
                return '', answer
            else:
                return 'Ошибка get_streets: json: не распознан ответ', []
        else:
            return f'Ошибка get_streets: responce.status_code: {responce.status_code}\n{responce.text}', []
        
        # [{"code":3090,"name":"Велозаводская улица"}, {"code":3090,"name":"Велозаводская улица"}]
        # {"resp_code":1,"resp_description":"no streets"}
        # {"resp_code":-1,"resp_description":"Необходимо заполнить «Txt».\n"}
    except:
        return 'Ошибка get_streets: try: requests.get', []
    
def get_houses(token: str, street_code: int, house: str) -> (str, list):
    url = url_onlime + '/api/dealer/addr/addrhouses'
    
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Authorization': token,
    }
    params = {
        'code': street_code,
        'txt': house,
    }

    try:
        responce = requests.get(url, headers=headers, params=params)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            if type(answer) == dict:
                resp_code = answer.get('resp_code')
                resp_description = answer.get('resp_description')
                if resp_code and resp_description:
                    if resp_code == 1: return f'Ошибка дом: \"{house}\" не найден.', []
                    elif resp_code == -1: return f'Ошибка запроса get_houses: {resp_description}', []
                    else: return f'Ошибка get_houses: resp_code: {resp_code}\n{resp_description}', []
                else:
                    return 'Ошибка get_houses: dict: не распознан ответ', []
            elif type(answer) == list:
                return '', answer
            else:
                return 'Ошибка get_houses: json: не распознан ответ', []
        else:
            return f'Ошибка get_houses: responce.status_code: {responce.status_code}\n{responce.text}', []
        
        # [{'code': 7511, 'name': '1/1 строение 9'}, {'code': 29874, 'name': '9'}, {'code': 83003, 'name': '9а'}, {'code': 130191, 'name': '9 корпус 2'}]
        # {"resp_code":1,"resp_description":"no streets"}
        # {'resp_code': -1, 'resp_description': 'Необходимо заполнить «Code».\n'}
    except:
        return 'Ошибка get_houses: try: requests.get', []
    
def get_entrances(token: str, house: int) -> (str, list):
    url = url_onlime + '/api/dealer/addr/getentrances'
    
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Authorization': token,
    }
    params = {
        'AddressId': house,
    }

    try:
        responce = requests.get(url, headers=headers, params=params)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            resp_code = answer.get('resp_code')
            resp_description = answer.get('resp_description')
            if resp_code == 0:  # норм
                entrances = answer.get('entrances')
                return '', entrances
            elif resp_code == -1: return f'Ошибка запроса get_entrances: {resp_description}', []
            elif resp_code == 1: return 'Ошибка подъезды в доме не найдены.', []
            else:
                return f'Ошибка get_entrances: resp_code: {resp_code} не распознан ответ', []
        else:
            return f'Ошибка get_entrances: responce.status_code: {responce.status_code}\n{responce.text}', []
        
        # {'resp_code': -1, 'resp_description': 'Необходимо заполнить «Address Id».\n'}
        # {'resp_code': 0, 'entrances': [1, 2, 3, 4]}
    except:
        return 'Ошибка get_entrances: try: requests.get', []
    
def get_checkptv(token: str, house: int, entrance: int) -> (str, dict):
    url = url_onlime + '/api/dealer/addr/checkptv'
    
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Authorization': token,
    }
    params = {
        'id_house': house,
        'entrance': entrance,
    }
    try:
        responce = requests.get(url, headers=headers, params=params)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            resp_code = answer.get('resp_code')
            resp_description = answer.get('resp_description')
            if resp_code == 0: return '', answer  # норм
            else: return f'Ошибка get_checkptv: resp_code: {resp_code} {resp_description}', {}
        else:
            return f'Ошибка get_checkptv: responce.status_code: {responce.status_code}\n{responce.text}', {}
        
        # {'resp_code': 0, 'inet': 'Y', 'dvbc': 'Y', 'check': 'N', 'speed100': '0', 'speed1000': '1'}
        # {'resp_code': -1, 'resp_description': 'Необходимо заполнить «Entrance».\n'}
    except:
        return 'Ошибка get_checkptv: try: requests.get', {}
    
def create_order(token: str, data: dict) -> (str, dict):
    url = url_onlime + '/api/dealer/order/createorder'
    
    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Authorization': token,
    }
    try: flat = int(data.get('Flat'))
    except: return 'Ошибка create_order: try: int: flat', {}
    try: entrance = int(data.get('Entrance'))
    except: return 'Ошибка create_order: try: int: entrance', {}
    try: floor = int(data.get('Floor'))
    except: return 'Ошибка create_order: try: int: floor', {}
    
    send_data = {
        'nam': data.get('nam'),           # Имя клиента
        'otc': data.get('otc'),        # Отчество клиента
        'phn_cell': data.get('phn_cell'),   # Номер мобильного телефона клиента, формат число 10 знаков
        'nt': data.get('nt'),           # Примечание (передаётся в CRM)
        'addr': {
            'AddressId': data.get('AddressId'),           # Id дома
            'Flat': flat,           # Номер квартиры
            'Entrance': entrance,           # Номер подъезда
            'Floor': floor,           # Этаж
        }
    }
    try:
        responce = requests.post(url, headers=headers, json=send_data)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            resp_code = answer.get('resp_code')
            resp_description = answer.get('resp_description')
            if resp_code == 0:
                return '', answer  # норм
            else: return f'Ошибка create_order: resp_code: {resp_code} {resp_description}', {}
        else:
            return f'Ошибка create_order: responce.status_code: {responce.status_code}\n{responce.text}', {}
    except:
        return 'Ошибка create_order: try: requests.get', {}
        
    return '', {}

def edit_order(token: str, id_order: int, config_plans: str) -> str:
    url = url_onlime + '/api/dealer/order/editorder'
    
    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Authorization': token,
    }
    
    send_data = {
        'id': id_order,
        'config': config_plans,           # Тарифные планы и оборудование
    }
    # print('config_plans', config_plans)
    try:
        responce = requests.post(url, headers=headers, json=send_data)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            resp_code = answer.get('resp_code')
            resp_description = answer.get('resp_description')
            if resp_code == 0: return ''  # норм
            else: return f'Ошибка edit_order: resp_code: {resp_code} {resp_description}'
        else:
            return f'Ошибка edit_order: responce.status_code: {responce.status_code}\n{responce.text}'
    except:
        return 'Ошибка edit_order: try: requests.get'
        
    return ''

def get_orders(token: str, id_order: int) -> (str, dict):
    url = url_onlime + '/api/dealer/order/getorders'
    
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Authorization': token,
    }
    params = {
        'order_id': id_order,
    }
    try:
        responce = requests.get(url, headers=headers, params=params)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            resp_code = answer.get('resp_code')
            resp_description = answer.get('resp_description')
            if resp_code == 0: return '', answer  # норм
            else: return f'Ошибка get_orders: resp_code: {resp_code} {resp_description}', {}
        else:
            return f'Ошибка get_orders: responce.status_code: {responce.status_code}\n{responce.text}', {}
        
    except:
        return 'Ошибка get_orders: try: requests.get', {}
    
def get_list(token: str, id_order: int) -> (str, dict):
    url = url_onlime + '/api/dealer/order/getlist'
    
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Authorization': token,
    }
    params = {
        'order_id': id_order,
    }
    try:
        responce = requests.get(url, headers=headers, params=params)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            resp_code = answer.get('resp_code')
            resp_description = answer.get('resp_description')
            if resp_code == 0: return '', answer  # норм
            else: return f'Ошибка get_list: resp_code: {resp_code} {resp_description}', {}
        else:
            return f'Ошибка get_list: responce.status_code: {responce.status_code}\n{responce.text}', {}
        
    except:
        return 'Ошибка get_list: try: requests.get', {}
    
def get_catalogue(token: str) -> (str, dict):
    url = url_onlime + '/api/dealer/order/getcatalogue'
    
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Authorization': token,
    }
    try:
        responce = requests.get(url, headers=headers)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            resp_code = answer.get('resp_code')
            resp_description = answer.get('resp_description')
            if resp_code == 0: return '', answer  # норм
            else: return f'Ошибка get_catalogue: resp_code: {resp_code} {resp_description}', {}
        else:
            return f'Ошибка get_catalogue: responce.status_code: {responce.status_code}\n{responce.text}', {}
        
    except:
        return 'Ошибка get_catalogue: try: requests.get', {}
    
def get_curent_config(token: str, id_order: int) -> (str, dict):
    url = url_onlime + '/api/dealer/order/getcurrentconfig'
    
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Authorization': token,
    }
    params = {
        'contract': id_order,
    }
    try:
        responce = requests.get(url, headers=headers, params=params)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            resp_code = answer.get('resp_code')
            resp_description = answer.get('resp_description')
            if resp_code == 0: return '', answer  # норм
            else: return f'Ошибка get_curent_config: resp_code: {resp_code} {resp_description}', {}
        else:
            return f'Ошибка get_curent_config: responce.status_code: {responce.status_code}\n{responce.text}', {}
        
    except:
        return 'Ошибка get_curent_config: try: requests.get', {}
    
def get_order_status(token: str, id_order: int) -> (str, dict):
    url = url_onlime + '/api/dealer/order/getorderstatus'
    
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Authorization': token,
    }
    params = {
        'order_id': id_order,
    }
    try:
        responce = requests.get(url, headers=headers, params=params)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            resp_code = answer.get('resp_code')
            resp_description = answer.get('resp_description')
            if resp_code == 0: return '', answer  # норм
            else: return f'Ошибка get_order_status: resp_code: {resp_code} {resp_description}', {}
        else:
            return f'Ошибка get_order_status: responce.status_code: {responce.status_code}\n{responce.text}', {}
        
    except:
        return 'Ошибка get_order_status: try: requests.get', {}
    
def set_account_crm(token: str, id_order: int) -> str:
    url = url_onlime + '/api/dealer/order/setaccount'
    
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Authorization': token,
    }
    params = {
        'id': id_order,
        'account': 'new',
    }

    try:
        responce = requests.get(url, headers=headers, params=params)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            resp_code = answer.get('resp_code')
            resp_description = answer.get('resp_description')
            if resp_code == 0: return ''  # норм
            else: return f'Ошибка set_account_crm: resp_code: {resp_code} {resp_description}'
        else:
            return f'Ошибка set_account_crm: responce.status_code: {responce.status_code}\n{responce.text}'
        
    except:
        return 'Ошибка set_account_crm: try: requests.get'
    
def send_order_crm(token: str, id_order: int) -> str:
    url = url_onlime + '/api/dealer/order/sendorder'
    
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Authorization': token,
    }
    params = {
        'id': id_order,
    }

    try:
        responce = requests.get(url, headers=headers, params=params)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            resp_code = answer.get('resp_code')
            resp_description = answer.get('resp_description')
            if resp_code == 0: return ''  # норм
            else: return f'Ошибка send_order_crm: resp_code: {resp_code} {resp_description}'
        else:
            return f'Ошибка send_order_crm: responce.status_code: {responce.status_code}\n{responce.text}'
        
    except:
        return 'Ошибка send_order_crm: try: requests.get'
    
def drop_order(token: str, id_order: int) -> str:
    url = url_onlime + '/api/dealer/order/droporder'
    
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Authorization': token,
    }
    params = {
        'id': id_order,
    }

    try:
        responce = requests.get(url, headers=headers, params=params)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            resp_code = answer.get('resp_code')
            resp_description = answer.get('resp_description')
            if resp_code == 0: return f'Заявка {id_order} удалена.'  # норм
            else: return f'Ошибка drop_order: resp_code: {resp_code} {resp_description}'
        else:
            return f'Ошибка drop_order: responce.status_code: {responce.status_code}\n{responce.text}'
        
    except:
        return 'Ошибка drop_order: try: requests.get'
    

def go_logoff(token: str) -> (str):
    url = url_onlime + '/api/dealer/user/logoff'
    
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Authorization': token,
    }
    try:
        responce = requests.get(url, headers=headers)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            
            resp_code = answer.get('resp_code')
            resp_description = answer.get('resp_description')
            if resp_code == 0: return ''  # норм
            elif resp_code == -1 or resp_code == 1: return f'Ошибка запроса go_logoff: {resp_description}'
            else: return f'Ошибка go_logoff: resp_code: {resp_code} не распознан ответ'
        else:
            return f'Ошибка go_logoff: responce.status_code: {responce.status_code}\n{responce.text}'
        
        # {'resp_code': 0, 'inet': 'Y', 'dvbc': 'Y', 'check': 'N', 'speed100': '0', 'speed1000': '1'}
        # {'resp_code': -1, 'resp_description': 'Необходимо заполнить «Entrance».\n'}
    except:
        return 'Ошибка go_logoff: try: requests.get'
    

# =========================================================
def set_bid(data):
    token = ''
    id_order = 0
    
    try:
        login = data.get('login')
        if not login: raise Exception('Ошибка не задан логин')
        password = data.get('password')
        if not password: raise Exception('Ошибка не задан пароль')
        
        # Получаем токен
        rez, token = get_token(login, password)
        if rez: raise Exception(rez, token)
        time.sleep(0.1)
        
        # Получаем код улицы
        street = data.get('street').strip()
        if not street: raise Exception('Ошибка не задана улица')
        rez, streets = get_streets(token, street)
        if rez: raise Exception(rez)
        street_code = 0
        if len(streets) == 1:
            street_code = streets[0].get('code')
        elif len(streets) == 0: raise Exception('Ошибка блока определения улицы.')
        else:
            lst_streets = []
            f_cnt = 0
            f_ind = 0
            for i in range(len(streets)):
                name_street = streets[i].get('name')
                if name_street == street:
                    f_cnt += 1
                    f_ind = i
                lst_streets.append(name_street)
            if f_cnt == 1: street_code = streets[f_ind].get('code')
            elif f_cnt > 1:
                raise Exception(f'Ошибка множественный выбор по названию улицы: \"{street}\".')
            else: 
                str_streets = '; '.join(lst_streets)
                raise Exception(f'Ошибка укажите улицу точнее. Возможны варианты:\n{str_streets}')
        if not street_code: raise Exception('Ошибка код улицы не определен.')
        time.sleep(0.1)
        # print('street_code:', street_code)
        
        # Получаем код дома
        house = data.get('house').strip()
        if not house: raise Exception('Ошибка не задан дом')
        c_house = ordering_house(house)
        if not c_house[0]: raise Exception(f'Ошибка распознавания дома: {c_house[1]}: \"{house}\".')
        rez, houses = get_houses(token, street_code, c_house[0])
        if rez: raise Exception(rez)
        house_code = 0
        if len(houses) == 1: house_code = houses[0].get('code')
        elif len(houses) == 0: raise Exception('Ошибка блока определения дома.')
        else:
            lst_houses = []
            f_cnt = 0
            f_ind = 0
            for i in range(len(houses)):
                name_house = houses[i].get('name')
                # print(houses[i].get('code'), name_house)
                if name_house == c_house[1]:
                    f_cnt += 1
                    f_ind = i
                lst_houses.append(name_house)
            if f_cnt == 1: house_code = houses[f_ind].get('code')
            elif f_cnt > 1:
                raise Exception(f'Ошибка множественный выбор по номеру дома: \"{house}\".')
            else: 
                str_houses = '; '.join(lst_houses)
                raise Exception(f'Ошибка укажите дом точнее. Возможны варианты:\n{str_houses}')
        if not house_code: raise Exception('Ошибка код дома не определен.')
        time.sleep(0.1)
        # print('house_code:', house_code)
        
        # Получаем подъезды
        rez, entrances = get_entrances(token, house_code)
        if rez: raise Exception(rez)
        if len(entrances) == 0: raise Exception('Ошибка нет номеров подъездов.')
        time.sleep(0.1)
        # print('entrances:', entrances)

        # Получаем ТхВ
        entrance = data.get('entrances')
        rez, ch_ptv = get_checkptv(token, house_code, entrance)
        if rez: raise Exception(rez)
        inet = ch_ptv.get('inet')
        dvbc = ch_ptv.get('dvbc')
        check = ch_ptv.get('check')
        speed100 = ch_ptv.get('speed100', '')
        speed1000 = ch_ptv.get('speed1000', '')
        str_ptv = ''
        if speed100: speed100 = '100Мбит '
        if speed1000: speed1000 = '1000Мбит '
        if inet == 'Y': str_ptv += f'Интернет {speed100}{speed1000}Есть ТхВ\n'
        if dvbc == 'Y': str_ptv += 'Цифровое ТВ Есть ТхВ\n'
        if check == 'Y': str_ptv += 'Требуется уточнение технической возможности\n'
        if not str_ptv:
            str_ptv = 'Нет ТхВ'
            raise Exception('Нет ТхВ.')
        
        time.sleep(0.1)

        order_data = {}
        order_data['nam'] = data.get('firstname')  # Имя клиента
        order_data['otc'] = data.get('patronymic')  # Отчество клиента
        order_data['phn_cell'] = data.get('phone')[1:]   # Номер мобильного телефона клиента, формат число 10 знаков
        order_data['nt'] = data.get('comment')  # Примечание (передаётся в CRM)
        order_data['AddressId'] = house_code  # Id дома
        order_data['Flat'] = data.get('apartment')  # Номер квартиры
        order_data['Entrance'] = entrance  # Номер подъезда
        order_data['Floor'] = data.get('floor')  # Этаж
        
        rez, cr_order = create_order(token, order_data)
        if rez: raise Exception(rez)
        time.sleep(0.1)
        accounts = cr_order.get('accounts')
        if accounts: print('accounts:', accounts)
        id_order = cr_order.get('id')
        data['bid_number'] = id_order
        print('id_order:', id_order)
            
        # Создание счета
        rez = set_account_crm(token, id_order)
        if rez: raise Exception(rez)
        time.sleep(0.1)
        
        # # print(json.dumps(serv_codes, indent=4))
        
        # # Запрос статуса текущей конфигурации по договору абонента
        # rez, cur_config = get_curent_config(token, id_order)  # не работает, нужен contract
        # if rez: raise Exception(rez)
        # print(json.dumps(cur_config, indent=4))
        
        # Запрос каталога услуг и тарифов
        rez, gt_catalog = get_catalogue(token)
        if rez: raise Exception(rez)
        time.sleep(0.1)

        # Получение доступных услуг, акций, тарифов
        rez, gt_list = get_list(token, id_order)
        if rez: raise Exception(rez)
        time.sleep(0.1)
        serv_codes = gt_list.get('codes')

        tarifs_eq = bid_dict.get('tarifs_eq')
        if not tarifs_eq: print('no tarifs_eq')

        # Ищем код тарифа по названию (Работаем только с тарифами интернет)
        rateplans = gt_catalog.get('rateplans')
        if not rateplans: print('no rateplans')
        lst_inet = rateplans.get('INET')
        if not lst_inet: print('no lst_inet')
        tar_code = ''
        for inet in lst_inet:
            name = inet.get('name')
            if name == tarifs_eq.strip(): tar_code = inet.get('code'); break
        if not tar_code: print('no tar_code')
        # Проверим на доступность тарифа по этому адресу
        if tar_code not in serv_codes: raise Exception(f'Тарифный план {tarifs_eq} не доступен по этому адресу.')

        plan = {
          'inet': {
            'rateplan': {
              'code': tar_code
            }
          },
          'dvbc': {},
          'eq': [],
        }
        str_plans = json.dumps(plan)
        rez = edit_order(token, id_order, str_plans)
        if rez: raise Exception(rez)
        time.sleep(0.1)
        print(str_plans)
        
        # raise Exception()
        
        # # Заводим тарифы
        # tarifs_eq = data.get('tarifs_eq')
        # if tarifs_eq:
            # rez = edit_order(token, id_order, tarifs_eq)
            # if rez: raise Exception(rez)
        # str_catalog = json.dumps(gt_catalog, indent=4).encode('utf8')
        # # Сохраняем в файл словарь gt_catalog отформатированный с отступами
        # with open('catalog.txt', 'w', encoding='utf-8') as of: json.dump(gt_catalog, of, ensure_ascii=False, indent=4)
        
        # # Запрос статуса текущей конфигурации по договору абонента
        # rez, cur_config = get_curent_config(token, id_order)
        # if rez: raise Exception(rez)
        # print(json.dumps(cur_config, indent=4))

        # # Отправляем заявку в СРМ
        # rez = send_order_crm(token, id_order)
        # if rez: raise Exception(rez)

        
        # # Посмотреть статус
        # rez, st_order = get_order_status(token, id_order)
        # if rez: raise Exception(rez)
        # print('st_order:', st_order)


        # # Удаление заявки
        # rez = drop_order(token, id_order)
        # print(rez)
            
            
    # То есть жизненный цикл заявки выглядит так:
    # checkPTV ->CreateOrder -> editOrder (контакт. Данные и адрес) -> setAcc ->getList(order_id) -> getCurrentConfig(order_id)-> editOrder (набор 
    # услуг) ->sendOrder
    except Exception as e:
        if token and id_order:
            rez = drop_order(token, id_order)
            if rez: print(rez)
        return str(e), data
    finally:
        # Выходим из аккаунта
        if token: go_logoff(token)
    
    return '', data

def set_did_to_dj_domconnect():
    url = url_host + 'api/set_bid_onlime'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
        'login': 'inetme12',
        'password': 'RxIT9oxP',
        'id_lid': '1215557',
        
        'city': 'Москва',           # город
        'street': 'улица Винокурова',         # улица
        'house': '7/5 кор. 2',          # дом
        'entrances': '1',           # подъезд
        'floor': '1',           # этаж
        'apartment': '6',          # квартира
        'tarifs_eq': 'ONLIME_95', # тарифный план и оборудование
        
        'firstname': 'Иван',
        'patronymic': 'Иванович',
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
    url = url_host + 'api/get_bid_onlime'
    
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
    url = url_host + 'api/set_bid_onlime_status'
    
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
    if bot_log: params['bot_log'] = bot_log
    
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
        'fields[UF_CRM_1493413514]': 2,
        'fields[UF_CRM_1499386906]': 523  # PartnerWEB
    }
    error_message = bid_dict.get("bot_log")
    if error_message:
        params['fields[UF_CRM_5864F4DAAC508]'] = error_message

    try:
        responce = requests.post(url, headers=headers, params=params)
    except:
        pass
    # https://crm.domconnect.ru/crm/lead/details/1215557/

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

def run_bid_onlime(tlg_chat, tlg_token):
    opsos = 'Онлайм'
    
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
            fio = f'{data.get("firstname")} {data.get("patronymic")}'
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'Адрес: {address}'
            tlg_mess += f'ФИО: {fio}\n'
            tlg_mess += f'Ошибка: {data.get("bot_log")}\n'
        r = send_telegram(tlg_chat, tlg_token, tlg_mess)
        print(tlg_mess)
        print('TelegramMessage:', r)
    #================================================


if __name__ == '__main__':
    # Документация: https://dealer.onlime.ru/beta/apidocs/
    # Ручная заводка заявки https://dealer.onlime.ru/beta/order/
    # login: inetme12
    # password: RxIT9oxP

    # # личный бот @infra
    # TELEGRAM_CHAT_ID = '1740645090'
    # TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'
    # run_bid_ttk(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
    
    bid_dict = {
        'login': 'inetme12',
        'password': 'RxIT9oxP',
        'id_lid': '1215557',
        
        # 'city': 'Москва',           # город
        # 'street': '6-я Кожуховская улица',         # улица
        # 'house': '10',          # дом
        # 'entrances': '1',           # подъезд
        # 'floor': '1',           # этаж
        # 'apartment': '6',          # квартира
        'city': 'Москва',           # город
        'street': 'улица Винокурова',         # улица
        'house': '7/5 кор. 2',          # дом
        'entrances': '1',           # подъезд
        'floor': '1',           # этаж
        'apartment': '6',          # квартира

        'tarifs_eq': 'Технологии доступа 100', # тарифный план и оборудование
        
        'firstname': 'Иван',
        'patronymic': '',
        'phone': '79012732350',
        'comment': 'Тестовая заявка, просьба не обрабатывать',          # коментарий обязательно: подъезд этаж
        'bid_number': '',          # номер заявки
    }
    e, data = set_bid(bid_dict)
    if e: print(e)
    print(data['bid_number'])       #     1053562
    
    


        # # # # Получаем токен
    # rez, token = get_token('inetme12', 'RxIT9oxP')
    # if rez: raise Exception(rez, token)
    # time.sleep(0.1)
    # print('token:', token)
    
    # tarifs_eq = bid_dict.get('tarifs_eq')
    # if not tarifs_eq: print('no tarifs_eq')

    # rez, gt_catalog = get_catalogue(token)
    # if rez: print(rez)
    # # Ищем код тарифа по названию (Работаем только с тарифами интернет)
    # rateplans = gt_catalog.get('rateplans')
    # if not rateplans: print('no rateplans')
    # lst_inet = rateplans.get('INET')
    # if not lst_inet: print('no lst_inet')
    # tar_code = ''
    # for inet in lst_inet:
        # name = inet.get('name')
        # if name == tarifs_eq.strip(): tar_code = inet.get('code'); break
    # if not tar_code: print('no tar_code')
    
    # print('tar_code:', tar_code)
    


    
    # Здесь подгрузим доступный список по заявке    
        # # Получение доступных услуг, акций, тарифов
        # rez, gt_list = get_list(token, id_order)
    

    # rez, gt_list = get_list(token, 1053562)
    # if rez: print(rez)
    # print('gt_list:', gt_list)   # Список тарифов
    
    # rez, gt_order = get_orders(token, 1053562)
    # if rez: print(rez)
    # print('gt_order:', gt_order)   # gt_order: {'resp_code': 0, 'paging': {'page': 1, 'size': 50, 'pages': 1, 'rows': 1}, 'Orders': [{'order_id': '1053562', 'no_crm': None, 'fam': '', 'nam': 'Иван', 'otc': '', 'client': 'Иван', 'phn_cell': '9011111113', 'phn_city': None, 'email': '', 'nt': 'Тестовая заявка, просьба не обрабатывать', 'nt_crm': None, 'inf': '', 'dt_reg': '23.12.2021 17:49:06', 'account': '0', 'CRMContractID': '0', 'agent': 'Иванов Глеб', 'partner': 'Web-дилер ИП Старковски', 'status': 'Новая', 'id_status': 0, 'stsid': 0, 'index': None, 'entrance': 1, 'intercom': '', 'floor': 1, 'flat': 6, 'address': 'улица Винокурова', 'house': ' 7/5 корп. 2', 'id_houses': 6068}]}


    # rez = send_order_crm(token, 1053562)
    # if rez: print(rez)


    # rez, st_order = get_order_status(token, 1053562)
    # if rez: print(rez)
    # print('st_order:', st_order)   # st_order: {'resp_code': 0, 'Orders': [{'id': '1053562', 'idStatus': 0, 'Status': 'Новая', 'UpdateDate': '2021-12-23 17:49:06', 'nam': 'Иван', 'phn_cell': '9011111113'}]}




    # # Удаление заявки
    # rez = drop_order(token, 1053597)
    # print(rez)
    
    
    # rateplans = ch_ptv.get('rateplans')
    # with open('out.txt', 'w', encoding='utf-8') as outfile:
        # outfile.write(dd)
    
    # set_did_to_dj_domconnect()
    # rez, bid_list = get_did_in_dj_domconnect()
    # for bid_dict in bid_list:
        # for k, v in bid_dict.items():
            # print(k, v)
    # data = {'id': 1, 'bid_number': '55632145', 'bot_log': 'Заявка принята'}
    # set_bid_status(3, data)
    
    
    # Ошибка send_order_crm: resp_code: -2 Не найдена бронь на окно.
    
    # # # # Сохраняем в файл словарь gt_catalog отформатированный с отступами
    # # # with open('catalog.txt', 'w', encoding='utf-8') as of: json.dump(gt_catalog, of, ensure_ascii=False, indent=4)

    pass
    '''
    Онлайм. API ЛКД Вопросы по работе сервисов.
    Авторизация проходит успешно. Проверка ТхВ возможна.
    Заявки создается. И удаление заявок работает.
    Но отредактировать её и отправить в СРМ не получается.
        Сервис editOrder
        в поле config (формат 	string) отправляем к примеру 
            {"inet": {"rateplan": {"code": "INET2021_100"}}, "dvbc": {}, "eq": []}
            или
            {"inet": {"rateplan": {"code": "INET2021_100"}}}
        в формате строки. Запрос принимается без ошибок, но изменения в заявке не происходят.

        Сервис getCurrentConfig
        Не доступен т.к. требуется единственный параметр contract (Номер договора)
        которого на тапе создания и редактирования заявки нет есть только id заявки.

        Сервис sendOrder (отправка заявки в СРМ)
        Не работает.
        Запрос всегда возвращается с кодом ошибки resp_code: -2 "Не найдена бронь на окно."
        
        Сервисы getListJobs, getJobs, releaseJobs (работа с графиками)
        Нет доступа. 
        Запросы возвращается с кодом ошибки resp_code: -2 "У вас нет доступа к графикам."
        
    Данные вопросы изложены на странице
    https://docs.google.com/spreadsheets/d/1fPFxlhAje5V_kdlSHpLytBbgE6SiBaWtfsrFjw1XYv8/edit#gid=1162938285
    (вкладка API ввод заявок)
    '''