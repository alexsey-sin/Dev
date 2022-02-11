import os
import time
import re
from datetime import datetime
import calendar
import requests  # pip install requests
import json


# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'
url_onlime = 'https://dealer.onlime.ru'  # Рабочий



def get_token(login: str, password: str):
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

def get_catalog():
    # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.catalog.get'
    # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.catalog.list'
    # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.productsection.fields'
    # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.fields'  # типы и структура полей
    # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.userfield.get'
    # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.userfield.list'
    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.status.entity.items' # Типы источника лида
    
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
    # select = [
        # 'ID', 
        # 'TITLE', 
        # 'STATUS_ID', 
        # 'DATE_CREATE',
        # 'DATE_MODIFY',
        # 'SOURCE_ID',
        # 'ASSIGNED_BY_ID',
        # 'UF_CRM_1493416385',  # Сумма тарифа
        # 'UF_CRM_1499437861',  # ИНН/Организация
        # 'UF_CRM_1580454770',  # Звонок?
        # 'UF_CRM_1534919765',  # Группы источников
        # 'UF_CRM_1571987728429',  # Провайдеры ДК
        # 'UF_CRM_1592566018',  # ТИп лида
        # 'UF_CRM_1493413514',  # Провайдер
        # 'UF_CRM_1492017494',  # Область
        # 'UF_CRM_1492017736',  # Город
        # 'UF_CRM_1498756113',  # Юр. лицо

        # 'UF_CRM_1615982450',  # utm_source
        # 'UF_CRM_1615982567',  # utm_medium
        # 'UF_CRM_1615982644',  # utm_campaign
        # 'UF_CRM_1615982716',  # utm_term                
        # 'UF_CRM_1615982795',  # utm_content                
        # 'UF_CRM_1640267556',  # utm_group 
    # ]

    # data = {
        # # 'filter': {'FIELD_NAME': 'UF_CRM_1592566018',}
        # 'id': 1840,
        # # 'order': { "DATE_MODIFY": "ASC" },  # Если нужно с сортировкой
        # # 'filter': {
            # # "CATALOG_ID": 30,
            # # # # '<DATE_CREATE': '2021-10-31T23:59:59',
        # # },
        # # 'select': [           crm.status.entity.items?entityId=SOURCE
            # # "ID", 
            # # "CATALOG_ID", 
            # # "SECTION_ID", 
            # # "NAME",
            # # "XML_ID",
            # # "CODE",
        # # ]
    # }
    data = {'entityId': 'SOURCE'}
    try:
        responce = requests.post(url, json=data)
        # responce = requests.post(url)
        # responce = requests.post(url, headers=headers)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            result = answer.get('result')
            for dct in result:
                name = dct.get('NAME')
                id = dct.get('STATUS_ID')
                print('ID', id, 'name:', name)
            print('Всего: ', len(result))
                # if name == 'Подключаем': print(name, 'ID', dct.get('ID'))  #  8
            # if not result: print('update_typelid no result in answer')
            # dct_list = result.get('LIST')
            # if not dct_list: print('update_typelid no field LIST in result in answer')
                # print()
            # for k, v in result.items():
                # if k in select:
                    # print(k,v)
                    # print()
            # go_next = answer.get('next')
            # go_total = answer.get('total')
            # out_lst += result
            # if not go_next: break
            # print(dct_list)
            # print(answer)
            # print(result)
            # print(go_next, go_total)
        else: return f'Ошибка get_catalog: responce.status_code: {responce.status_code}\n{responce.text}'
    except: return 'Ошибка get_catalog: try: requests.post'
        # time.sleep(1)
        # break
        
    return ''

def get_company():
    # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.deal.list'
    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.deal.fields'
    
    # data = {
        # # 'filter': {'FIELD_NAME': 'UF_CRM_1592566018',}
        # 'id': 1840,
        # # 'order': { "DATE_MODIFY": "ASC" },  # Если нужно с сортировкой
        # # 'filter': {
            # # "CATALOG_ID": 30,
            # # # # '<DATE_CREATE': '2021-10-31T23:59:59',
        # # },
        # # 'select': [           crm.status.entity.items?entityId=SOURCE
            # # "ID", 
            # # "CATALOG_ID", 
            # # "SECTION_ID", 
            # # "NAME",
            # # "XML_ID",
            # # "CODE",
        # # ]
    # }
    # data = {'entityId': 'SOURCE'}
    try:
        # responce = requests.post(url, json=data)
        responce = requests.post(url)
        # responce = requests.post(url, headers=headers)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            # result = answer.get('result')
            # for dct in result:
                # name = dct.get('NAME')
                # id = dct.get('STATUS_ID')
                # print('ID', id, 'name:', name)
            # print('Всего: ', len(result))
                # if name == 'Подключаем': print(name, 'ID', dct.get('ID'))  #  8
            # if not result: print('update_typelid no result in answer')
            # dct_list = result.get('LIST')
            # if not dct_list: print('update_typelid no field LIST in result in answer')
                # print()
            # for k, v in result.items():
                # if k in select:
                    # print(k,v)
                    # print()
            # go_next = answer.get('next')
            # go_total = answer.get('total')
            # out_lst += result
            # if not go_next: break
            # print(dct_list)
            # print(json.dump(answer, indent=2))
            # print(result)
            # print(go_next, go_total)

            with open('deals.json', 'w', encoding='utf-8') as out_file:
                json.dump(answer, out_file, ensure_ascii=False, indent=4)

        else: return f'Ошибка get_catalog: responce.status_code: {responce.status_code}\n{responce.text}'
    except: return 'Ошибка get_catalog: try: requests.post'
        # time.sleep(1)
        # break
        
    return ''

def get_source():
    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.status.entity.items' # Типы источника лида
    
    out_dct = []
    data = {'entityId': 'SOURCE'}
    try:
        responce = requests.post(url, json=data)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            result = answer.get('result')
            for dct in result:
                name = dct.get('NAME')
                st_id = dct.get('STATUS_ID')
                out_dct.append('ID: %20s      NAME: %s' % (st_id, name))
                # out_dct.append({'ID': st_id, 'NAME': name})
                # print('ID: %20s      NAME: %s' % (st_id, name))
            print('Всего: ', len(result))
            # print(answer)
            # print(result)

            with open('source_id.txt', 'w', encoding='utf-8') as outfile:
                outfile.write('\n'.join(out_dct))
                # json.dump(out_dct, outfile, ensure_ascii=False, indent=4)


        else: return f'Ошибка get_source: responce.status_code: {responce.status_code}\n{responce.text}'
    except: return 'Ошибка get_source: try: requests.post'
        
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

def get_field_deals():
    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.deal.fields'
    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    try:
        responce = requests.post(url, headers=headers)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            result = answer.get('result')
            return result
        else:
            print(responce.status_code)
            print(responce.text)
            return f'Ошибка get_field_deals: responce.status_code: {responce.status_code}\n{responce.text}'
    except:
        return 'Ошибка get_field_deals: try: requests.post'

def get_deals(from_data):
    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.deal.list'
    
    # dt_start = datetime.strptime(from_data, '%d.%m.%Y')
    # str_dt_start = dt_start.strftime('%Y-%m-%dT%H:%M:%S')
    go_next = 0
    go_total = 0
    out_lst = []

    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    while True:
        data = {
            'start': go_next,
            'order': { "DATE_MODIFY": "ASC" },  # Если нужно с сортировкой
            'filter': {
                '>DATE_CREATE': from_data,  # '2021-10-01T00:00:00'
                # '<DATE_CREATE': '2021-10-31T23:59:59',
            },
            'select': [
                "ID",
                "SOURCE_ID",
                "DATE_CREATE",
                'DATE_MODIFY',
                "UF_CRM_5904FB99DBF0C",  # Дата подключения
                "UF_CRM_5EECA3B76309E",  # Дата лида
                "UF_CRM_5903C16BCEE3A",  # Услуги  []
                "UF_CRM_5903C16BDAA69",  # Сумма тарифа
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
                return f'Ошибка get_deals: responce.status_code: {responce.status_code}\n{responce.text}', []
        except:
            return 'Ошибка get_deals: try: requests.post', []
        time.sleep(1)
    return '', out_lst


if __name__ == '__main__':
    pass
    # start_script_time = datetime.now()

    # Документация: https://dev.1c-bitrix.ru/rest_help/crm/leads/crm_lead_list.php
    # Лиды
    # Пример запроса https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.list
    # Сделки
    # Пример запроса https://dev.1c-bitrix.ru/rest_help/crm/cdeals/crm_deal_list.php
    

    # from_date = '2022-02-08T00:00:00'
    # # e = get_catalog()
    # # e = get_source()
    # e, lst_deal = get_deals(from_date)
    # if e: print(e)
    
    e = get_field_deals()
    if e:
        with open('deals_all_fields.json', 'w', encoding='utf-8') as out_file:
            json.dump(e, out_file, ensure_ascii=False, indent=4)

    # cur_day = datetime.today().day
    # cur_month = datetime.today().month
    # cur_year = datetime.today().year
    # cnt_days_in_cur_month = calendar.monthrange(cur_year, cur_month)[1]
    # # print(cnt_days_in_cur_month)
    # # print(cur_day, cur_month, cur_year)
    # print(datetime.today().isoweekday())
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



