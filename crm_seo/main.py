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

def get_canalog(from_data):
    # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.catalog.get'
    # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.catalog.list'
    # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.productsection.fields'
    # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.fields'
    # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.userfield.get'
    # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.userfield.list'
    # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.status.entity.items' # Типы источника лида
    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.userfield.get'
    
    # dt_start = datetime.strptime(from_data, '%d.%m.%Y')
    # str_dt_start = dt_start.strftime('%Y-%m-%dT%H:%M:%S')
    # go_next = 0
    # go_total = 0
    # out_lst = []

    # headers = {
        # 'Content-Type': 'application/json',
        # 'Connection': 'Keep-Alive',
        # 'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    # }
    # print(str_dt_start)
    # return '', []
    # while True:
    data = {
        # 'filter': {'FIELD_NAME': 'UF_CRM_1592566018',}
        'id': 1840,
        # 'order': { "DATE_MODIFY": "ASC" },  # Если нужно с сортировкой
        # 'filter': {
            # "CATALOG_ID": 30,
            # # # '<DATE_CREATE': '2021-10-31T23:59:59',
        # },
        # 'select': [           crm.status.entity.items?entityId=SOURCE
            # "ID", 
            # "CATALOG_ID", 
            # "SECTION_ID", 
            # "NAME",
            # "XML_ID",
            # "CODE",
        # ]
    }
    try:
        responce = requests.post(url, json=data)
        # responce = requests.post(url)
        # responce = requests.post(url, headers=headers)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            result = answer.get('result')
            if not result: print('update_typelid no result in answer')
            dct_list = result.get('LIST')
            if not dct_list: print('update_typelid no field LIST in result in answer')
            for dct in dct_list:
                print(dct)
            # for k, v in result.items():
                # print(k,v)
                # print()
            # go_next = answer.get('next')
            # go_total = answer.get('total')
            # out_lst += result
            # if not go_next: break
            # print(dct_list)
            # print(answer)
            # print(go_next, go_total)
        else: return f'Ошибка get_canalog: responce.status_code: {responce.status_code}\n{responce.text}'
    except: return 'Ошибка get_canalog: try: requests.post'
        # time.sleep(1)
        # break
        
    return ''


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
    # start_script_time = datetime.now()

    # Документация: https://dev.1c-bitrix.ru/rest_help/crm/leads/crm_lead_list.php
    # Пример запроса https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.list
    
    
    
    from_date = '01.01.2022'
    e = get_canalog(from_date)
    if e: print(e)
    
    # with open('lids_format.txt', 'w', encoding='utf-8') as out_file:
        # json.dump(data_lids, out_file, ensure_ascii=False, indent=4)
    
    # with open('lids.json', 'w', encoding='utf-8') as out_file:
        # json.dump(data_lids, out_file, ensure_ascii=False)

    # end_script_time = datetime.now()
    # print('\nDuration: {}'.format(end_script_time - start_script_time))


    
    # url = "https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"
    # responce = requests.get(url)
    # if responce.status_code == 200:
        # with open('jquery.min.js', 'w', encoding='utf-8') as outfile:
            # outfile.write(responce.text)
        # print('Ok')


    # from_date = '2022-01-01T04:43:22+03:00'
    # ddd = datetime.strptime(from_date, '%Y-%m-%dT%H:%M:%S%z')
    # print(ddd)

    # with open('lids.json', 'r', encoding='utf-8') as file:  # читаем время создания токена если есть
        # js_lids = json.load(file)
    # # dt_old_str = js.get('time_create')
    
    # y_id = True
    # many = 0
    # for lid in js_lids:
        # f_id = lid.get('UF_CRM_1592566018')
        # if f_id == None or len(f_id) == 0:
            # y_id = False
            # continue
        # if len(f_id) > many: many = len(f_id)
        
    # print(len(js_lids))
    # print('y_id', y_id)
    # print('many', many)


        # * "ID": "1253690",
        # * "TITLE": "Позвонить клиенту: 17.01.2022 14:00:00 - ➕➕ ✏️ Константин С. ⏳ Рузаевка (+00:00), Северная улица 5- ТТК ([Лиза] Звонок без результата, перезвон)",
        # * "STATUS_ID": "42",
        # * "DATE_CREATE": "2022-01-14T12:39:52+03:00",
        # * "DATE_MODIFY": "2022-01-18T14:01:02+03:00",
        # "SOURCE_ID": "98",
        # "ASSIGNED_BY_ID": "11149",
        # "UF_CRM_1493416385": null,
        # "UF_CRM_1499437861": null,
        # "UF_CRM_1580454770": "0",
        # "UF_CRM_1534919765": [],// Группы источников
        # "UF_CRM_1571987728429": "Ростелеком, ТТК",
        # "UF_CRM_1592566018": [// ТИп лида
            # 3116
        # ],
        # "UF_CRM_1493413514": "4",
        # "UF_CRM_1492017494": "Республика Мордовия",
        # "UF_CRM_1492017736": "Рузаевка",
        # "UF_CRM_1498756113": "0",
        # "UF_CRM_1615982450": null,
        # "UF_CRM_1615982567": null,
        # "UF_CRM_1615982644": null,
        # "UF_CRM_1615982716": null,
        # "UF_CRM_1615982795": null,
        # "UF_CRM_1640267556": null
