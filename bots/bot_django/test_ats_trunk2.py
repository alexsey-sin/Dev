import os, sys, time, json, copy
from datetime import datetime
import requests  # pip install requests
import ats_trunk


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
    # # Вывод всей информации в файл
    # orig_stdout = sys.stdout
    # f = open('out.txt', 'w')
    # sys.stdout = f
    
    # get_route_trunks()
    # get_routes()
    # get_trunks()
    
    # sys.stdout = orig_stdout
    # f.close()
    
    out_file = open('out2.txt', 'w', encoding='utf-8')
    # Запрашиваем список транков (телефонов)
    rez, rez_str, trunks = ats_trunk.get_trunks()
    if rez:  # Если  что-то не так
        print(f'ATS-TRUNK: get_trunks(): {rez_str}')
        exit(0)
    out_file.write('\nСписки транков.\n')
    json.dump(trunks, out_file, ensure_ascii=False, indent=4)

    # Запрашиваем доступные минуты
    rez, rez_str, trunks = ats_trunk.get_residue_trunks(trunks)
    if rez: out_file.write(f'ATS-TRUNK: {rez_str}')  # Если  что-то не так
    out_file.write('\nДоступные минуты.\n')
    json.dump(trunks, out_file, ensure_ascii=False, indent=4)
    
    # Запрашиваем список групп (ROUTE)
    rez, rez_str, routes = ats_trunk.get_routes()
    if rez:  # Если  что-то не так
        out_file.write(f'ATS-TRUNK: get_routes(): {rez_str}')
        exit(0)
    out_file.write('\nСписок групп.\n')
    json.dump(routes, out_file, ensure_ascii=False, indent=4)
    
    # Запрашиваем текущее состояние настроек route_trunks
    rez, rez_str, route_trunks = ats_trunk.get_route_trunks(routes)
    if rez:  # Если  что-то не так
        out_file.write(f'ATS-TRUNK: get_route_trunks(): {rez_str}')
        exit(0)
    out_file.write('\nТекущее состояние настроек.\n')
    json.dump(route_trunks, out_file, ensure_ascii=False, indent=4)
    

    # Проверим приоритеты транков
    change_list, new_trunks = ats_trunk.checking_priorities(route_trunks, trunks)
    out_file.write('\nПриоритеты транков Новые.\n')
    json.dump(new_trunks, out_file, ensure_ascii=False, indent=4)
    out_file.write('\nИзменения.\n')
    json.dump(change_list, out_file, ensure_ascii=False, indent=4)

    out_file.write('\n\n')
    out_file.write('==============================================================\n')
    out_file.write('Сводная таблица.\n')
    for route in new_trunks:
        out_file.write(f'ROUTE {route.get("id")} {route.get("name")}\n')
        tranks = route.get("trunks")
        for tr in tranks:
            out_file.write(f'\tid: {tr.get("trunk_id")} cid: {tr.get("cid")} min: {tr.get("residue")} seq: {tr.get("seq")}\n')
        out_file.write('\n')
    out_file.write('==============================================================\n')
    out_file.write('Изменения.\n')
    for ch in change_list:
        out_file.write(f'route: {ch.get("route_id")} trunk: {ch.get("trunk_id")} seq: {ch.get("seq")}\n')
    
    out_file.write('==============================================================\n')
    
    out_file.close()
