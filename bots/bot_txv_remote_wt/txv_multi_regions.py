import os, time, json, threading, copy, requests  # pip install requests
from datetime import datetime

# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'

pv_name = 'Мульти_регион'
pv_code = 10


class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        self._stop_event = threading.Event()
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)


def get_txv(query, accesses):
    try:
        lst_threads = []
        lst_available_connect = []
        lst_pv_address = []
        lst_bot_log = []
        for access in accesses:  # Перелистаем доступы
            pv_code = access.get('pv_code')
            time.sleep(1)
            if pv_code == 1:  # Билайн
                try:
                    from txv_beeline import get_txv as get_txv_beeline
                    cur_query = copy.deepcopy(query)  # создадим глубокую копию словаря запроса
                    cur_query['pv_code'] = pv_code
                    cur_query['pv_name'] = access.get('pv_name')
                    cur_query['login'] = access.get('login')
                    cur_query['password'] = access.get('password')
                    cur_query['login_2'] = access.get('login_2')
                    cur_query['password_2'] = access.get('password_2')
                    thread = ThreadWithResult(target=get_txv_beeline, args=(cur_query,))
                    thread.start()  # Запустим поток
                    lst_threads.append(thread)
                except:
                    mess = f'{access.get("pv_name")}: бот недоступен.'
                    lst_available_connect.append(mess)
                    lst_bot_log.append(mess)
                    continue
                continue
            if pv_code == 2:  # ДомРу
                try:
                    from txv_domru import get_txv as get_txv_domru
                    cur_query = copy.deepcopy(query)  # создадим глубокую копию словаря запроса
                    cur_query['pv_code'] = pv_code
                    cur_query['pv_name'] = access.get('pv_name')
                    cur_query['login'] = access.get('login')
                    cur_query['password'] = access.get('password')
                    cur_query['login_2'] = access.get('login_2')
                    cur_query['password_2'] = access.get('password_2')
                    thread = ThreadWithResult(target=get_txv_domru, args=(cur_query,))
                    thread.start()  # Запустим поток
                    lst_threads.append(thread)
                except:
                    mess = f'{access.get("pv_name")}: бот недоступен.'
                    lst_available_connect.append(mess)
                    lst_bot_log.append(mess)
                    continue
                continue
            if pv_code == 3:  # МТС
                try:
                    from txv_mts import get_txv as get_txv_mts
                    cur_query = copy.deepcopy(query)  # создадим глубокую копию словаря запроса
                    cur_query['pv_code'] = pv_code
                    cur_query['pv_name'] = access.get('pv_name')
                    cur_query['login'] = access.get('login')
                    cur_query['password'] = access.get('password')
                    cur_query['login_2'] = access.get('login_2')
                    cur_query['password_2'] = access.get('password_2')
                    thread = ThreadWithResult(target=get_txv_mts, args=(cur_query,))
                    thread.start()  # Запустим поток
                    lst_threads.append(thread)
                except:
                    mess = f'{access.get("pv_name")}: бот недоступен.'
                    lst_available_connect.append(mess)
                    lst_bot_log.append(mess)
                    continue
                continue
            if pv_code == 4:  # Ростелеком
                try:
                    from txv_rostelecom import get_txv as get_txv_rostelecom
                    cur_query = copy.deepcopy(query)  # создадим глубокую копию словаря запроса
                    cur_query['pv_code'] = pv_code
                    cur_query['pv_name'] = access.get('pv_name')
                    cur_query['login'] = access.get('login_2')
                    cur_query['password'] = access.get('password_2')
                    # cur_query['login_2'] = access.get('login_2')
                    # cur_query['password_2'] = access.get('password_2')
                    thread = ThreadWithResult(target=get_txv_rostelecom, args=(cur_query,))
                    thread.start()  # Запустим поток
                    lst_threads.append(thread)
                except:
                    mess = f'{access.get("pv_name")}: бот недоступен.'
                    lst_available_connect.append(mess)
                    lst_bot_log.append(mess)
                    continue
                continue
            if pv_code == 5:  # ТТК
                try:
                    from txv_ttk import get_txv as get_txv_ttk
                    cur_query = copy.deepcopy(query)  # создадим глубокую копию словаря запроса
                    cur_query['pv_code'] = pv_code
                    cur_query['pv_name'] = access.get('pv_name')
                    cur_query['login'] = access.get('login')
                    cur_query['password'] = access.get('password')
                    cur_query['login_2'] = access.get('login_2')
                    cur_query['password_2'] = access.get('password_2')
                    thread = ThreadWithResult(target=get_txv_ttk, args=(cur_query,))
                    thread.start()  # Запустим поток
                    lst_threads.append(thread)
                except:
                    mess = f'{access.get("pv_name")}: бот недоступен.'
                    lst_available_connect.append(mess)
                    lst_bot_log.append(mess)
                    continue
                continue

        # Присоединимся к потокам и дождемся завершения их работы
        for th in lst_threads:
            th.join()
        
        # Обработка результатов работы ботов
        for th in lst_threads:
            rez, cur_query = th.result
            pv_code = cur_query.get('pv_code')
            pv_name = cur_query.get('pv_name')
            if rez: lst_bot_log.append(f'{pv_name}: {rez}')
            # Добавляем в ответ данные по определившимуся адресу ПВ и лог бота
            pv_address = cur_query.get('pv_address')
            if pv_address: lst_pv_address.append(f'{pv_name}: {pv_address}')
            bot_log = cur_query.get('bot_log')
            if bot_log: lst_bot_log.append(f'{pv_name}: {bot_log}')
            # Добавляем в ответ данные по ТхВ с разбором ответов для каждого ПВ
            available_connect = cur_query.get('available_connect')
            if pv_code == 1:  # Билайн
                av_conn = f'{pv_name}: '
                if rez: av_conn += 'Ошибка'
                if available_connect:
                    if available_connect.find('Есть ТхВ') >= 0: av_conn += 'Есть ТхВ'  # Обычно есть ограничения
                    if available_connect.find('Нет ТхВ') >= 0: av_conn += 'Нет ТхВ'  # Обычно есть ограничения
                    if available_connect.find('На адресе есть активный договор') >= 0: av_conn += 'Активный договор'
                lst_available_connect.append(av_conn)
            if pv_code == 2:  # ДомРу
                av_conn = f'{pv_name}: '
                if rez: av_conn += 'Ошибка'
                if available_connect:
                    if available_connect.find('Дом подключен к интернет') >= 0: av_conn += 'Есть ТхВ'
                    if available_connect.find('Дом не подключен к интернет') >= 0: av_conn += 'Нет ТхВ'
                    if available_connect.find('В регионе нет ТхВ') >= 0: av_conn += 'Нет ТхВ'
                lst_available_connect.append(av_conn)
            if pv_code == 3:  # МТС
                av_conn = f'{pv_name}: '
                if rez: av_conn += 'Ошибка'
                if available_connect:
                    if available_connect.find('Возможность подключения') >= 0: av_conn += 'Есть ТхВ'
                    if available_connect.find('Нет технической возможности') >= 0: av_conn += 'Нет ТхВ'
                lst_available_connect.append(av_conn)
            if pv_code == 4:  # Ростелеком
                av_conn = f'{pv_name}: '
                if rez: av_conn += 'Ошибка'
                if available_connect:
                    lst_av_conn = available_connect.split('\n')
                    ok_txv = False
                    for row_av_conn in lst_av_conn:
                        if row_av_conn.find('Домашний интернет') >= 0 and row_av_conn.find('Есть ТхВ') >= 0:
                            av_conn += 'Есть ТхВ'
                            ok_txv = True
                            break
                    if ok_txv == False: av_conn += 'Нет ТхВ'
                lst_available_connect.append(av_conn)
            if pv_code == 5:  # ТТК
                av_conn = f'{pv_name}: '
                if rez: av_conn += 'Ошибка'
                if available_connect:
                    lst_av_conn = available_connect.split('\n')
                    ok_txv = False
                    for row_av_conn in lst_av_conn:
                        if row_av_conn.find('Интернет') >= 0 and row_av_conn.find('Есть Тех.Возм') >= 0:
                            av_conn += 'Есть ТхВ'
                            ok_txv = True
                            break
                    if ok_txv == False: av_conn += 'Нет ТхВ'
                lst_available_connect.append(av_conn)
        
        query['available_connect'] = '\n'.join(lst_available_connect)
        query['pv_address'] = '\n'.join(lst_pv_address)
        query['bot_log'] = '\n'.join(lst_bot_log)
        
    except Exception as e:
        return str(e)[:100], query
   
    return '', query

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
        'id_lid': '1215557',
        
        'region': 'Самарская область',           # город
        'city': 'Самара',           # город
        'street': 'Партизанская улица',         # улица
        'house': '206',          # дом
        'apartment': '10',          # квартира
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

    available_connect = txv_dict.get('available_connect')
    mess_crm = available_connect
    pv_address = txv_dict.get('pv_address')
    if pv_address: mess_crm += f'\n\n{pv_address}\n'

    params = {
        'id': txv_dict.get('id_lid'),
        'fields[UF_CRM_1638779781554][]': mess_crm,  # вся инфа
    }

    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.update'
    try:
        responce = requests.post(url, headers=headers, params=params)
        st_code = responce.status_code
        if st_code != 200: return st_code, ''
        # посмотреть результат https://crm.domconnect.ru/crm/lead/details/1215557/
    except Exception as e:
        return str(e), ''
    return ''
    
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

def run_txv_multi_regions(tlg_chat, tlg_token):
    tlg_mess = ''
    
    # личный бот @infra
    TELEGRAM_CHAT_ID = '1740645090'
    TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'
    
    rez, txv_obj = get_txv_in_dj_domconnect(pv_code)
    if rez:
        tlg_mess = f'ТхВ: {pv_name} Ошибка при загрузке запросов из domconnect.ru'
        r = send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, tlg_mess)
        print(tlg_mess, '\nTelegramMessage:', r)
        return
    non_query = False
    if type(txv_obj) == list: non_query = True
    elif type(txv_obj) == dict:
        querys = txv_obj.get('querys', [])  # список словарей с заявками
        accesses = txv_obj.get('accesses', [])  # список словарей с провадерами и доступами
        if len(querys) == 0 or len(accesses) == 0: non_query = True
    else:
        non_query = True
        tlg_mess = f'ТхВ: {pv_name} Неверный формат ответа из domconnect.ru'
        r = send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, tlg_mess)
        print(tlg_mess, '\nTelegramMessage:', r)

    if non_query:
        cur_time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        print(f'{cur_time} {pv_name}: Запросов ТхВ нет')
        return

    # Перелистываем список словарей с заявками
    for query in querys:
        rez, query = get_txv(query, accesses)
        if rez: query['bot_log'] = f'{rez}\n' + query['bot_log']
        e = send_crm_txv(query, pv_name)  # ответ в CRM
        if e:
            crm_mess = f'Ошибка при отправке в СРМ: {e}\n'
            tlg_mess += crm_mess
            query['bot_log'] += crm_mess
        address = f'{query.get("city")} {query.get("street")} д.{query.get("house")} кв.{query.get("apartment")}'
        tlg_mess += f'ТхВ {pv_name}:\n'
        tlg_mess += f'Адрес: {address}\n'
        djdc = ''
        if rez == '':  # заявка успешно создана
            djdc = set_txv_status(3, query)
            tlg_mess += 'Успешно.\n'
        else:  # не прошло
            djdc = set_txv_status(2, query)
            tlg_mess += f'{query.get("bot_log")}\n'
        if djdc: tlg_mess += f'Ошибка при отправке в dj_domconnect: {djdc}'
        r = send_telegram(tlg_chat, tlg_token, tlg_mess[:300])
        print(tlg_mess)
        print('TelegramMessage:', r)
    #================================================


if __name__ == '__main__':
    # start_time = datetime.now()
    
    # личный бот @infra
    TELEGRAM_CHAT_ID = '1740645090'
    TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

    run_txv_multi_regions(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)

    # set_txv_to_dj_domconnect(pv_code)
    
    # threads = []
    # thread = ThreadWithResult(target=test, name='thread 2', args=(3,))
    # thread.start()  # Запустим поток
    # threads.append(thread)
    
    # thread = ThreadWithResult(target=test, name='thread 3', args=(8,))
    # thread.start()  # Запустим поток
    # threads.append(thread)
    
    # thread = threading.Thread(target=test, name='thread 2', args=(3,))
    # thread.start()  # Запустим поток
    # threads.append(thread)
    
    # thread = threading.Thread(target=test, name='thread 3', args=(8,))
    # thread.start()  # Запустим поток
    # threads.append(thread)
    
    # cnt = 5
    # while cnt > 0:
        # time.sleep(1)
        # cnt -= 1
    
    # lst_thr = []
    # print('потоков:', threading.active_count())
    # for thr in threading.enumerate():
        # name = thr.getName()
        # if name != 'MainThread':
            # lst_thr.append(name)
            # thr.kill()
    # print('kill:', lst_thr)
    # print('потоков:', threading.active_count())
        # is_run = True
        # for th in threads:
    
    # for th in threads:
        # isA = th.is_alive()
        # if th.name != 'MainThread' and isA:
            # print('the live:', th.name, isA)
            # terminate()


    # print('потоков:', threading.active_count())
    # data = {'id': 1, 'pv_address': '55632145', 'bot_log': 'Заявка принята С'}
    # r = set_txv_status(0, data)
    # print(r)
    # Билайн, ДомРу, МТС, Ростелеком, ТТК

    
    pass
    
    # end_time = datetime.now()
    # time_str = '\nDuration: {}'.format(end_time - start_time)
    # print(time_str)
    # # limit_request_line

    # def test(n):
        # ff = n
        # print(f'start of {ff}')
        # while n > 0:
            # time.sleep(1)
            # n -= 1
        # print(f'stop of {ff}')
