import os
import time
from datetime import datetime
import requests  # pip install requests
import json
import copy



# общий канал бот @АТС приоритет
TELEGRAM_CHAT_ID = '-652685335'
TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'

# личный бот @infra
# TELEGRAM_CHAT_ID = '1740645090'
# TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

PERIOD_SCAN = 1 * 60 * 60  # в секундах (1 час)
# PERIOD_BETWEEN = 60
# PERIOD_SCAN = 600  # в секундах


# url_dj_domconnect = 'http://127.0.0.1:8000/mobile/get_mobile_residue'  # тестовый
url_dj_domconnect = 'http://django.domconnect.ru/mobile/get_mobile_residue'  # боевой

url_ats = 'https://atc.domconnect.ru/'  # боевой сервер
# url_ats = 'https://atctest.domconnect.ru/'  # тестовый сервер

# # Ссылки от Павла
# https://atc.domconnect.ru/cli/api_route_display_route_trunks.php
# https://atc.domconnect.ru/cli/api_route_display_routing.php
# https://atc.domconnect.ru/cli/api_route_display_trunks.php
# https://atc.domconnect.ru/cli/api_route_sequence.php

def send_telegram(text: str):
    url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage"
    try:
        r = requests.post(url, data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text
        })
    except:
        pass

def get_trunks():  # Запрос и обработка ответа к atctest.domconnect.ru -> Получение списока транков (телефонов)
    url = url_ats + 'cli/api_route_display_trunks.php'
    out_rez = 0
    out_mess = ''
    trunks = []
    try:
        responce = requests.get(url, timeout=(2, 2))  # timeout=(время_подключение, время_чтения) в сек
        if responce.status_code == 200:
            lst_trunk = responce.text.split('<br>')
            for trunk in lst_trunk:
                key_id = 'ID:'
                key_name = 'NAME:'
                key_cid = 'CID:'
                i_key_id = trunk.find(key_id)
                i_key_name = trunk.find(key_name)
                i_key_cid = trunk.find(key_cid)
                if i_key_id < 0 or i_key_name < 0 or i_key_cid < 0:
                    out_mess += f'Error parsing trunk: {trunk}\n'
                    out_rez = 2
                    continue
                id_tr = trunk[i_key_id + len(key_id):i_key_name].strip()
                name_tr = trunk[i_key_name + len(key_name):i_key_cid].strip()
                cid_tr = trunk[i_key_cid + len(key_cid):].strip()
                trunk_dict = {'id': id_tr, 'name': name_tr, 'cid': cid_tr}
                trunks.append(trunk_dict)
        else:
            out_mess = f'Error: responce.status_code: {responce.status_code}\n'
            return 1, out_mess, trunks
    except:
        return 1, 'Error: requests.get\n', trunks

    return 0, out_mess, trunks
    
def get_residue_trunks(trunks):  # Запрос и обработка ответа к django.domconnect.ru -> получение остатков минут
    out_mess = ''
    data = {'nums': []}
    # Коррекция номера и создание списка для запроса
    for trunk in trunks:
        str_num = trunk.get('cid')
        if len(str_num) == 10:
            str_num = f'7{str_num}'
        elif len(str_num) == 12:
            str_num = str_num[1:]
        trunk['cid'] = str_num
        data['nums'].append(str_num)
    try:
        responce = requests.get(url_dj_domconnect, params={'key': 'Q8kGM1HfWz'}, json=data)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            if answer and type(answer) == dict:
                for num, residue in answer.items():
                    for trunk in trunks:
                        if trunk['cid'] == num:
                            if type(residue) == int:
                                trunk['residue'] = residue
                            else:
                                out_mess += f'{num}: {residue}\n'
                                trunk['residue'] = 0
                                # trunks.remove(trunk)
                            break
            else:
                out_mess = 'Error: answer or type(answer)'
                return 1, out_mess, trunks
        else:
            out_mess = f'Error: responce.status_code: {responce.status_code}'
            return 1, out_mess, trunks
    except:
        return 1, 'Error: requests.get', trunks
    
    if out_mess:
        return 2, out_mess, trunks
    return 0, out_mess, trunks

def get_routes():  # Запрос и обработка ответа к atctest.domconnect.ru -> Получение групп транков
    url = url_ats + 'cli/api_route_display_routing.php'
    out_rez = 0
    out_mess = ''
    routes = []

    try:
        responce = requests.get(url, timeout=(2, 2))  # timeout=(время_подключение, время_чтения) в сек
        if responce.status_code == 200:
            lst_routes = responce.text.split('<br>')
            for route in lst_routes:
                key_id = 'ID:'
                key_name = 'NAME:'
                i_key_id = route.find(key_id)
                i_key_name = route.find(key_name)
                if i_key_id < 0 or i_key_name < 0:
                    out_mess += f'Error parsing route: {route}\n'
                    out_rez = 2
                    continue
                id_rt = route[i_key_id + len(key_id):i_key_name].strip()
                name_rt = route[i_key_name + len(key_name):].strip()
                route_dict = {'id': id_rt, 'name': name_rt}
                routes.append(route_dict)
        else:
            out_mess = f'Error: responce.status_code: {responce.status_code}\n'
            return 1, out_mess, routes
    except:
        return 1, 'Error: requests.get\n', routes

    return 0, out_mess, routes
    
def get_route_trunks(route_trunks):  # Запрос и обработка ответа к atctest.domconnect.ru -> Получение текущего состояния групп транков
    url = url_ats + 'cli/api_route_display_route_trunks.php'
    out_rez = 0
    out_mess = ''

    try:
        responce = requests.get(url, timeout=(2, 2))  # timeout=(время_подключение, время_чтения) в сек
        if responce.status_code == 200:
            lst_route_trunk = responce.text.split('<br>')
            for rt_trunk in lst_route_trunk:
                # print(rt_trunk)
                key_route_id = 'ROUTE_ID:'
                key_trunk_id = 'TRUNK_ID:'
                key_seq = 'SEQ:'
                i_key_route_id = rt_trunk.find(key_route_id)
                i_key_trunk_id = rt_trunk.find(key_trunk_id)
                i_key_seq = rt_trunk.find(key_seq)
                if i_key_route_id < 0 or i_key_trunk_id < 0 or i_key_seq < 0:
                    out_mess += f'Error parsing route_trunks: {rt_trunk}\n'
                    out_rez = 2
                    continue
                route_id = rt_trunk[i_key_route_id + len(key_route_id):i_key_trunk_id].strip()
                trunk_id = rt_trunk[i_key_trunk_id + len(key_trunk_id):i_key_seq].strip()
                seq = rt_trunk[i_key_seq + len(key_seq):].strip()
                route_trunk_dict = {'trunk_id': trunk_id, 'seq': seq}
                # найдем эту группу
                for rt_tr in route_trunks:
                    if rt_tr['id'] == route_id:
                        if rt_tr.get('trunks') == None: rt_tr['trunks'] = []
                        rt_tr['trunks'].append(route_trunk_dict)
        else:
            print(responce.status_code)
            out_mess = f'Error: responce.status_code: {responce.status_code}\n'
            return 1, out_mess, route_trunks
    except:
        return 1, 'Error: requests.get\n', route_trunks


    return 0, out_mess, route_trunks

def checking_priorities(route_trunks, trunks_residue):
    out_rez = 0
    out_mess = ''

    change_list = []
    for route_trunk in route_trunks:  # Проход по каждой группе транков
        route_id = route_trunk['id']
        trunks = route_trunk['trunks']
        for trunk in trunks:
            trunk_id = trunk['trunk_id']
            trunk['residue'] = 0
            # к каждому транку добавляем значение residue
            # к каждому транку добавляем поле residue
            for tr_resd in trunks_residue:
                if tr_resd['id'] == trunk_id:
                    trunk['residue'] = tr_resd['residue']
        
        # создадим глубокую копию списка
        new_trunks = copy.deepcopy(trunks)
        # отсортируем группу по доступным минутам (residue) по убыванию
        new_trunks.sort(key=lambda x: x['residue'], reverse=True)
        
        # проставим новые приоритеты
        for i in range(len(new_trunks)):
            new_trunks[i]['seq'] = str(i)
        
        # Проверим на несовпадение направлений отсортированной группы и старого варианта
        for trunk in trunks:
            # найдем этот транк в отсортированной группе
            for new_trunk in new_trunks:
                if trunk['trunk_id'] == new_trunk['trunk_id']:
                    if trunk['seq'] != new_trunk['seq']:
                        # именена очередность!
                        new_seq = {}
                        new_seq['route_id'] = route_id
                        new_seq['trunk_id'] = trunk['trunk_id']
                        new_seq['seq'] = new_trunk['seq']
                        change_list.append(new_seq)
        
    if change_list:
        out_rez, out_mess = change_seq(change_list)
    return out_rez, out_mess

def change_seq(change_list):
    url = url_ats + 'cli/api_route_sequence.php'
    out_rez = 0
    out_mess = ''
    cnt_change = 0
    
    try:
        for ch_row in change_list:
            cnt_change += 1
            new_url = f'{url}?route_id={ch_row["route_id"]}&trunk_id={ch_row["trunk_id"]}&seq={ch_row["seq"]}&action=update'
            responce = requests.post(new_url, timeout=(2, 2))  # timeout=(время_подключение, время_чтения) в сек
            if responce.status_code != 200:
                out_mess = f'Error: POST responce.status_code: {responce.status_code}\n'
                return 1, out_mess, routes
                
        if cnt_change:
            # Делаем запрос на перезагрузку атс
            new_url = url_ats + 'cli/apply_config.php'
            responce = requests.get(new_url)  # timeout=(время_подключение, время_чтения) в сек
            if responce.status_code != 200:
                out_mess = f'Error: POST запрос перезагрузка АТС status_code: {responce.status_code}\n'
                return 1, out_mess, routes
            
            out_mess = f'Изменена очередность {cnt_change} транков'
    except:
        return 1, 'Error: requests.post\n'
    
    return out_rez, out_mess


def run_ats():
    out_rez = 0
    out_mess = ''
    
    # Запрашиваем список транков (телефонов)
    rez, rez_str, trunks = get_trunks()
    if rez: return rez, f'get_trunks(): {rez_str}'  # Если  что-то не так
    
    # Запрашиваем доступные минуты
    rez, rez_str, trunks = get_residue_trunks(trunks)
    if rez: print(rez_str)  # Если  что-то не так
    if rez == 1:  # Критическая ошибка
        return rez, f'get_residue_trunks(): {rez_str}\nВозможно нет доступа к АТС'  # Если  что-то не так
    elif rez == 2:  # Предупреждение
        pass  # Убираем отладочную информацию
        # out_mess += f'get_residue_trunks(): {rez_str}'

    # Запрашиваем список групп (ROUTE)
    rez, rez_str, routes = get_routes()
    if rez: return rez, f'get_routes(): {rez_str}'  # Если  что-то не так
    
    # Запрашиваем текущее состояние настроек route_trunks
    rez, rez_str, route_trunks = get_route_trunks(routes)
    if rez: return rez, f'get_route_trunks(): {rez_str}'  # Если  что-то не так

    # Меняем приоритеты транков
    rez, rez_str = checking_priorities(route_trunks, trunks)
    if rez: return rez, f'checking_priorities(): {rez_str}'  # Если  что-то не так
    out_mess += rez_str
    return out_rez, out_mess  # Если  есть сообщение
    
def make_report(rez, rez_str):
    if rez_str:
        tlg_mess = f'ATS - смена приоритетов транков\n{rez_str}'
        send_telegram(tlg_mess)


if __name__ == '__main__':
    
    while True:
        start_time = datetime.now()
        #===============================================#
        if start_time.hour >= 6 and start_time.hour < 23:
            # start ats
            str_time = start_time.strftime('%H:%M %d.%m.%Y')
            print(f'{str_time} Start')
            rez, rez_str = run_ats()
            make_report(rez, rez_str)
        time.sleep(5)
        #===============================================#
        cur_time = datetime.now()
        
        passed = (cur_time - start_time).seconds
        left = PERIOD_SCAN - passed
        if left > 0:
            time.sleep(left)

'''
    Демон находится /etc/systemd/system/ats_bot.service
    
    [Unit]
    Description=ATS domconnect bot
    After=network.target
    [Service]
    User=root
    Group=root
    WorkingDirectory=/var/www/bot_ats/
    EnvironmentFile=/etc/environment
    ExecStart=/var/www/bot_ats/venv/bin/python3 main.py
    ExecReload=/var/www/bot_ats/venv/bin/python3 main.py
    StandardOutput=syslog
    StandardError=syslog
    Restart=always
    RestartSec=15
    [Install]
    WantedBy=multi-user.target



'''