import os
import time
from datetime import datetime
import requests  # pip install requests
import json


# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'

url_onlime = 'https://dealer.onlime.ru'
opsos = 'Онлайм'
pv_code = 6

    
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
            elif resp_code == -1 or resp_code == 1: return f'Ошибка запроса get_checkptv: {resp_description}', {}
            else: return f'Ошибка get_checkptv: resp_code: {resp_code} не распознан ответ', {}
        else:
            return f'Ошибка get_checkptv: responce.status_code: {responce.status_code}\n{responce.text}', {}
        
        # {'resp_code': 0, 'inet': 'Y', 'dvbc': 'Y', 'check': 'N', 'speed100': '0', 'speed1000': '1'}
        # {'resp_code': -1, 'resp_description': 'Необходимо заполнить «Entrance».\n'}
    except:
        return 'Ошибка get_checkptv: try: requests.get', {}
    
def get_getcatalogue(token: str) -> (str, dict):
    url = url_onlime + '/api/dealer/order/getcatalogue'
    
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        'Authorization': token,
    }
    # params = {
        # 'id_house': house,
        # 'entrance': entrance,
    # }
    try:
        # responce = requests.get(url, headers=headers, params=params)
        responce = requests.get(url, headers=headers)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            
            print(answer)
            return '', {}
            # resp_code = answer.get('resp_code')
            # resp_description = answer.get('resp_description')
            # if resp_code == 0: return '', answer  # норм
            # elif resp_code == -1 or resp_code == 1: return f'Ошибка запроса get_getcatalogue: {resp_description}', {}
            # else: return f'Ошибка get_getcatalogue: resp_code: {resp_code} не распознан ответ', {}
        # else:
            # return f'Ошибка get_getcatalogue: responce.status_code: {responce.status_code}\n{responce.text}', {}
        
        # {'resp_code': 0, 'inet': 'Y', 'dvbc': 'Y', 'check': 'N', 'speed100': '0', 'speed1000': '1'}
        # {'resp_code': -1, 'resp_description': 'Необходимо заполнить «Entrance».\n'}
    except:
        return 'Ошибка get_getcatalogue: try: requests.get', {}
    
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
def get_txv(data):
    try:
        data['pv_address'] = 'Адрес не определен.'
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
        rez, ch_ptv = get_checkptv(token, house_code, entrances[0])
        if rez: raise Exception(rez)
        data['pv_address'] = 'Адрес распознан.'
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
        if not str_ptv: str_ptv = 'Нет ТхВ'
        data['available_connect'] = str_ptv
        time.sleep(0.1)

        # # Получаем каталог Тарифы, услуги
        # rez, ch_ptv = get_getcatalogue(token)
        # if rez: raise Exception(rez)

        # Выходим из аккаунта
        rez = go_logoff(token)
        if rez: raise Exception(rez)

        # # checkPTV	/api/dealer/addr/checkptv	Проверка технической возможности


        
    except Exception as e:
        return str(e), data
    finally: pass
   
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
        'login': 'inetme12',
        'password': 'RxIT9oxP',
        'id_lid': '1215557',
        
        'city': 'Москва',           # город
        'street': 'улица Винокурова',         # улица
        # 'street': 'Волжский Бульвар 95',         # улица
        # 'street': 'ffkjsnsycvbt',         # улица
        # 'street': 'ул. Ленина',         # улица
        # 'street': 'Ленина',         # улица
        'house': '7/5 кор. 2',          # дом
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
    if pv_address: restrictions += f'{opsos} определил адрес: {pv_address}\n'
    
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

def run_txv_onlime(tlg_chat, tlg_token):
    tlg_mess = ''
    
    rez, txv_list = get_txv_in_dj_domconnect(pv_code)
    if rez:
        tlg_mess = 'Ошибка при загрузке запросов из domconnect.ru'
        r = send_telegram(tlg_chat, tlg_token, tlg_mess)
        print('TelegramMessage:', r)
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
    
    # Документация: https://dealer.onlime.ru/beta/apidocs/
    # login: inetme12
    # password: RxIT9oxP

    
    # txv_dict = {
        # 'pv_code': pv_code,
        # 'login': 'inetme12',
        # 'password': 'RxIT9oxP',
        # 'id_lid': '1215557',
        
        # 'city': 'Москва',           # город
        # 'street': 'улица Винокурова',         # улица
        # # 'street': 'Волжский Бульвар 95',         # улица
        # # 'street': 'ffkjsnsycvbt',         # улица
        # # 'street': 'ул. Ленина',         # улица
        # # 'street': 'Ленина',         # улица
        # 'house': '7/5 кор. 2',          # дом
        # 'apartment': '6',          # квартира

        # 'available_connect': '',  # Возможность подключения
        # 'tarifs_all': '', # список названий тарифных планов
        # 'pv_address': '',
    # }
    
    
    # e, data = get_txv(txv_dict)
    # if e: print(e)
    # print(data['pv_address'])
    # print(data['available_connect'])
    # print(data['tarifs_all'])
    
    
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
    

    # Калужская область	Калуга	улица Ленина 31
    # Санкт-Петербург Санкт-Петербург улица Маршала Казакова 78к1
    # Ярославская область Ярославль проспект Толбухина 31



    

    
    
    pass
    
    end_time = datetime.now()
    time_str = '\nDuration: {}'.format(end_time - start_time)
    print(time_str)
    # limit_request_line
    # улица Винокурова 7/5 корпус 2; 17 корпус 3; 17 корпус 1; 17 корпус 4; 17 корпус 2; 7/5 корпус 3; 7/5 корпус 1
    # Ошибка укажите улицу точнее. Возможны варианты:
    # 4 (пос. Совхоза им. Ленина) микрорайон; Ленина (Балашиха) просп.; Ленина (Балашиха) ул.; Ленина (Внуково) улица; Ленина (Высоковск) улица; Ленина (дп Загорянский) улица; Ленина (Запрудня) улица; Ленина (Истра) улица; Ленина (Климовск) улица; Ленина (Коломна) улица; Ленина (Королёв) улица; Ленина (Красногорск) улица; Ленина (Лобня) улица; Ленина (Лосино-Петровский) улица; Ленина (Лыткарино) улица; Ленина (мкр.Климовск) улица; Ленина (мкр.Саввино) улица; Ленина (Ногинск) улица; Ленина (Озёры) улица; Ленина (Орехово-Зуево) улица; Ленина (Подольск) проспект; Ленина (пос. Большевик) улица; Ленина (пос. Минвнешторга) улица; Ленина (пос.Авсюнино) улица; Ленина (пос.Кокошкино) улица; Ленина (пос.Обухово) улица; Ленина (пос.Правдинский) улица; Ленина (пос.Сергиевский) улица; Ленина (Протвино) улица; Ленина (Реутов) ул.; Ленина (рп Октябрьский) улица; Ленина (село Красная Пахра) улица; Ленина (село Красная Пахра) улица; Ленина (Сергиев Пасад); Ленина (Сходня) улица; Ленина (Щёлково) улица; Ленина (Электрогорск) улица; Ленина (Электросталь) проспект; пос.Совхоза им.Ленина (Видное); ул. Ленина; ул. Ленина; ул. Ленина; улица Ленина (Кашира); улица Ленина (Клин); улица Ленина (Крюково) (Зеленоград)

    # Duration: 0:00:00.866294

    # c:\Dev\bots\bot_txv_remote_wt>python txv_onlime.py
    # Ошибка укажите улицу точнее. Возможны варианты:
    # ул. Ленина; ул. Ленина; ул. Ленина

    # Duration: 0:00:00.825041

    # c:\Dev\bots\bot_txv_remote_wt>python txv_onlime.py
    # 501684 ул. Ленина
    # 501239 ул. Ленина
    # 502008 ул. Ленина
    # Ошибка укажите улицу точнее. Возможны варианты:
    # ул. Ленина; ул. Ленина; ул. Ленина
