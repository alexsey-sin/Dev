import os
import sys
import time
from datetime import datetime
import requests  # pip install requests
import json
import copy


url_ats = 'https://atc.domconnect.ru/'  # боевой сервер
# url_ats = 'https://atctest.domconnect.ru/'  # тестовый сервер

def get_route_trunks():  # Запрос и обработка ответа к atctest.domconnect.ru -> Получение текущего состояния групп транков
    url = url_ats + 'cli/api_route_display_route_trunks.php'

    try:
        responce = requests.get(url, timeout=(2, 2))  # timeout=(время_подключение, время_чтения) в сек
        if responce.status_code == 200:
            print('Текущее состояние групп транков.')
            lst_route_trunk = responce.text.split('<br>')
            for rt_trunk in lst_route_trunk:
                print(rt_trunk, ';')
        else:
            print(f'Error: responce.status_code: {responce.status_code}')
    except:
        print('Error: requests.get')

def get_routes():  # Запрос и обработка ответа к atctest.domconnect.ru -> Получение групп транков
    url = url_ats + 'cli/api_route_display_routing.php'

    try:
        responce = requests.get(url, timeout=(2, 2))  # timeout=(время_подключение, время_чтения) в сек
        if responce.status_code == 200:
            print('Список групп транков.')
            lst_routes = responce.text.split('<br>')
            for route in lst_routes:
                print(route, ';')
        else:
            print(f'Error: responce.status_code: {responce.status_code}')
    except:
        print('Error: requests.get')

def get_trunks():  # Запрос и обработка ответа к atctest.domconnect.ru -> Получение списока транков (телефонов)
    url = url_ats + 'cli/api_route_display_trunks.php'

    try:
        responce = requests.get(url, timeout=(2, 2))  # timeout=(время_подключение, время_чтения) в сек
        if responce.status_code == 200:
            print('Список транков (телефонов).')
            lst_trunk = responce.text.split('<br>')
            for trunk in lst_trunk:
                print(trunk, ';')
        else:
            print(f'Error: responce.status_code: {responce.status_code}')
    except:
        print('Error: requests.get')


if __name__ == '__main__':
    pass
    # Перезагрузка атс

    # new_url = url_ats + 'cli/apply_config.php'
    # print(new_url)
    # responce = requests.get(new_url)  # timeout=(время_подключение, время_чтения) в сек
    # print(responce.status_code)
    # print(responce.text)
    
    
    # out_rez = 0
    # out_mess = ''
    
    # url_ats = 'https://atc.domconnect.ru/'  # боевой сервер
    # new_url = url_ats + 'cli/apply_config.php'
    # print(new_url)
    # print()
    # responce = requests.post(new_url)
    # print(responce.status_code)
    # print(responce.text)
    
    
    # # Запрашиваем приоритеты в группах
    # get_route_trunks()

    # # Запрашиваем группы транков
    # get_routes()


    # # Запрашиваем список транков (телефонов), timeout=(2, 2)
    # get_trunks()
    
    
    ####################################################################
    # Вывод всей информации в файл
    orig_stdout = sys.stdout
    f = open('out.txt', 'w')
    sys.stdout = f
    
    get_route_trunks()
    get_routes()
    get_trunks()
    
    sys.stdout = orig_stdout
    f.close()
