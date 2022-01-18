import os
import time
import re
from datetime import datetime
import requests  # pip install requests
import json


# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'
url_onlime = 'https://dealer.onlime.ru'  # Рабочий



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

def get_lids(from_data):
    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.list'
    
    dt_start = datetime.strptime(from_data, '%d.%m.%Y')
    str_dt_start = dt_start.strftime('%Y-%m-%dT%H:%M:%S')
    go_next = 0
    go_total = 0
    out_lst = []

    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    # print(str_dt_start)
    # return '', []
    while True:
        data = {
            'start': go_next,
            'order': { "DATE_MODIFY": "ASC" },  # Если нужно с сортировкой
            'filter': {
                '>DATE_CREATE': str_dt_start,  # '2021-10-01T00:00:00'
                # '<DATE_CREATE': '2021-10-31T23:59:59',
            },
            'select': [
                "ID", 
                "TITLE", 
                "STATUS_ID", 
                "DATE_CREATE",
                "DATE_MODIFY",
                "SOURCE_ID",
                "ASSIGNED_BY_ID",
                "UF_CRM_1493416385",  # Сумма тарифа
                "UF_CRM_1499437861",  # ИНН/Организация
                "UF_CRM_1580454770",  # Звонок?
                "UF_CRM_1534919765",  # Группы источников
                "UF_CRM_1571987728429",  # Провайдеры ДК
                "UF_CRM_1592566018",  # ТИп лида
                "UF_CRM_1493413514",  # Провайдер
                "UF_CRM_1492017494",  # Область
                "UF_CRM_1492017736",  # Город
                "UF_CRM_1498756113",  # Юр. лицо

                "UF_CRM_1615982450",  # utm_source
                "UF_CRM_1615982567",  # utm_medium
                "UF_CRM_1615982644",  # utm_campaign
                "UF_CRM_1615982716",  # utm_term                
                "UF_CRM_1615982795",  # utm_content                
                "UF_CRM_1640267556",  # utm_group 
            ]
        }
        try:
            responce = requests.post(url, headers=headers, json=data)
            if responce.status_code == 200:
                answer = json.loads(responce.text)
                result = answer.get('result')
                go_next = answer.get('next')
                go_total = answer.get('total')
                out_lst += result
                if not go_next: break
                print(go_next, go_total)
            else:
                return f'Ошибка get_lids: responce.status_code: {responce.status_code}\n{responce.text}', []
        except:
            return 'Ошибка get_lids: try: requests.post', []
        time.sleep(1)
    return '', out_lst


if __name__ == '__main__':
    start_script_time = datetime.now()

    # Документация: https://dev.1c-bitrix.ru/rest_help/crm/leads/crm_lead_list.php
    # Пример запроса https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.list
    
    
    
    from_date = '01.01.2022'
    e, data_lids = get_lids(from_date)
    if e: print(e)
    
    with open('lids_format.txt', 'w', encoding='utf-8') as out_file:
        json.dump(data_lids, out_file, ensure_ascii=False, indent=4)
    
    with open('lids.json', 'w', encoding='utf-8') as out_file:
        json.dump(data_lids, out_file, ensure_ascii=False)

    end_script_time = datetime.now()
    print('\nDuration: {}'.format(end_script_time - start_script_time))
    
    
    
    



