from domconnect.models import DcCrmGlobVar, DcCrmLid
import time
import logging
import requests
import json
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    format='%(asctime)s:%(name)s:%(message)s'
)
# log = logging.getLogger(__name__)  # запускать в функциях
# log.info('So should this')
# # # # log.debug('This message should go to the log file')
# # # # log.warning('And this, too')



typesource = {}
typelid = {}


def thread_download_crm(str_from_modify):
    print(f'start thread {str_from_modify}')
    download_typesource()
    download_typelid()
    download_lids(str_from_modify)

    # for k, v in typesource.items():
    #     print(k, v)
    # for k, v in typelid.items():
    #     print(k, v)
 
    print('stop thread')
    
def download_typesource():  # Обновление Типов источника лида
    log = logging.getLogger(__name__)  # запустили логгирование
    key_crm = get_key_crm()
    url = f'https://crm.domconnect.ru/rest/{key_crm}/crm.status.entity.items'
    data = {'entityId': 'SOURCE'}

    try:
        responce = requests.post(url, json=data)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            result = answer.get('result')
            for res in result:
                status_id = res.get('STATUS_ID')
                if not status_id:
                    log.info(f'Ошибка download_typesource: error status_id: {status_id}')
                    continue
                typesource[status_id] = res.get('NAME')
        else: return log.info(f'Ошибка download_typesource: responce.status_code: {responce.status_code}\n{responce.text}')
    except Exception as e: log.info(f'Ошибка download_typesource: try: requests.post {e}')

def download_typelid():  # Обновление Типов лида
    log = logging.getLogger(__name__)  # запустили логгирование
    '''
        Чтобы найти значения поля UF_CRM_1592566018
        делаем запрос
        https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.userfield.list
        из ответа узнаем ID поля => 1840
        делаем запрос
        https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.userfield.get?id=1840
        В поле LIST список допустимых значений

    '''
    key_crm = get_key_crm()
    url = f'https://crm.domconnect.ru/rest/{key_crm}/crm.lead.userfield.get'
    data = {'id': 1840}

    try:
        responce = requests.post(url, json=data)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            result = answer.get('result')
            field_list = result.get('LIST')
            for f_lst in field_list:
                id_tl = f_lst.get('ID')
                val_tl = f_lst.get('VALUE')
                typelid[id_tl] = val_tl
        else: return log.info(f'Ошибка download_typelid: responce.status_code: {responce.status_code}\n{responce.text}')
    except Exception as e: log.info(f'Ошибка download_typelid: try: requests.post {e}')

def download_lids(str_from_modify):
    log = logging.getLogger(__name__)  # запустили логгирование
    gvar_url, create = DcCrmGlobVar.objects.get_or_create(key='url_download_crm')
    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.list'
    if create:
        gvar_url.val_str = url
        gvar_url.save()
    else:
        url = gvar_url.val_str
    

    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }

    go_next = 0
    go_total = 0
    cnt_err = 0
    cnt_ok = 0
    while True:
        gvar_go, _ = DcCrmGlobVar.objects.get_or_create(key='go_download_crm')
        if gvar_go.val_bool == False: break
        if go_next == None: go_next = 0 
        data = {
            'start': go_next,
            'order': {'DATE_MODIFY': 'ASC'},  # С сортировкой
            'filter': {
                # '>DATE_CREATE': '2020-01-01T00:00:00',  # '2021-10-01T00:00:00'
                '>DATE_CREATE': '2022-01-01T00:00:00',  # '2021-10-01T00:00:00'
                # '>DATE_CREATE': '2021-10-01T00:00:00',  # '2021-10-01T00:00:00'
                '!STATUS_ID': [17, 24],    # Дубль и ошибка в телефоне
            },
            'select': [
                'ID', 
                'TITLE', 
                'STATUS_ID', 
                'DATE_CREATE',
                'DATE_MODIFY',
                'SOURCE_ID',
                'ASSIGNED_BY_ID',
                'UF_CRM_1493416385',  # Сумма тарифа
                'UF_CRM_1499437861',  # ИНН/Организация
                'UF_CRM_1580454770',  # Звонок?
                'UF_CRM_1534919765',  # Группы источников
                'UF_CRM_1571987728429',  # Провайдеры ДК
                'UF_CRM_1592566018',  # ТИп лида
                'UF_CRM_1493413514',  # Провайдер
                'UF_CRM_1492017494',  # Область
                'UF_CRM_1492017736',  # Город
                'UF_CRM_1498756113',  # Юр. лицо

                'UF_CRM_1615982450',  # utm_source
                'UF_CRM_1615982567',  # utm_medium
                'UF_CRM_1615982644',  # utm_campaign
                'UF_CRM_1615982716',  # utm_term                
                'UF_CRM_1615982795',  # utm_content                
                'UF_CRM_1640267556',  # utm_group 
            ]
        }
        if str_from_modify:
            data['filter']['>DATE_MODIFY'] = str_from_modify
        try:
            responce = requests.post(url, headers=headers, json=data)
            if responce.status_code == 200:
                answer = json.loads(responce.text)
                result = answer.get('result')
                go_next = answer.get('next')
                go_total = answer.get('total')
                print(go_next, go_total)
                ok, err = append_lids(result)
                cnt_ok += ok; cnt_err += err
                if not go_next: break
            else: log.info(f'Ошибка download_lids: responce.status_code: {responce.status_code}\n{responce.text}')
        except Exception as e: log.info(f'Ошибка download_lids: try: requests.post {e}')
        gvar_cur, _ = DcCrmGlobVar.objects.get_or_create(key='cur_num_download_crm')
        gvar_cur.val_int = go_next
        gvar_cur.save()
        gvar_tot, _ = DcCrmGlobVar.objects.get_or_create(key='tot_num_download_crm')
        gvar_tot.val_int = go_total
        gvar_tot.save()
        time.sleep(1)
    
    gvar_go, _ = DcCrmGlobVar.objects.get_or_create(key='go_download_crm')
    gvar_go.val_bool = False
    gvar_go.save()
    mess = f'Обработано лидов: {cnt_ok}. Ошибок: {cnt_err}'
    log.info(mess)

def append_lids(lids):
    log = logging.getLogger(__name__)  # запустили логгирование
    cnt_err = 0
    cnt_ok = 0
    for new_lid in lids:
        err = True
        try:
            lid, _ = DcCrmLid.objects.get_or_create(id_lid=new_lid.get('ID'))
            lid.title = new_lid.get('TITLE')
            lid.status_id = new_lid.get('STATUS_ID')
            lid.create_date = datetime.strptime(new_lid.get('DATE_CREATE')[:-6], '%Y-%m-%dT%H:%M:%S')  # "2022-01-01T04:43:22+03:00"
            lid.modify_date = datetime.strptime(new_lid.get('DATE_MODIFY')[:-6], '%Y-%m-%dT%H:%M:%S')
            val_field = new_lid.get('SOURCE_ID')
            if val_field:
                if not val_field in typesource: lid.source_id = val_field
                else: lid.source_id = typesource[val_field]
            val_field = new_lid.get('ASSIGNED_BY_ID')
            if val_field: lid.assigned_by_id = val_field
            val_field = new_lid.get('UF_CRM_1493416385')
            if val_field: lid.crm_1493416385 = int(val_field)
            val_field = new_lid.get('UF_CRM_1499437861')
            if val_field: lid.crm_1499437861 = val_field
            val_field = new_lid.get('UF_CRM_1580454770')
            if val_field: lid.crm_1580454770 = bool(val_field)
            val_field = new_lid.get('UF_CRM_1534919765')
            if val_field and len(val_field) > 0: lid.crm_1534919765 = val_field[0]
            val_field = new_lid.get('UF_CRM_1571987728429')
            if val_field: lid.crm_1571987728429 = val_field
            val_field = new_lid.get('UF_CRM_1592566018')
            if val_field and len(val_field) > 0:
                val_field = str(val_field[0])
                if val_field not in typelid: lid.crm_1592566018 = val_field
                else: lid.crm_1592566018 = typelid[val_field]
            val_field = new_lid.get('UF_CRM_1493413514')
            if val_field: lid.crm_1493413514 = val_field
            val_field = new_lid.get('UF_CRM_1492017494')
            if val_field: lid.crm_1492017494 = val_field
            val_field = new_lid.get('UF_CRM_1492017736')
            if val_field: lid.crm_1492017736 = val_field
            val_field = new_lid.get('UF_CRM_1498756113')
            if val_field: lid.crm_1498756113 = bool(val_field)
            val_field = new_lid.get('UF_CRM_1615982450')
            if val_field: lid.crm_1615982450 = val_field
            val_field = new_lid.get('UF_CRM_1615982567')
            if val_field: lid.crm_1615982567 = val_field
            val_field = new_lid.get('UF_CRM_1615982644')
            if val_field: lid.crm_1615982644 = val_field
            val_field = new_lid.get('UF_CRM_1615982716')
            if val_field: lid.crm_1615982716 = val_field
            val_field = new_lid.get('UF_CRM_1615982795')
            if val_field: lid.crm_1615982795 = val_field
            val_field = new_lid.get('UF_CRM_1640267556')
            if val_field: lid.crm_1640267556 = val_field
            lid.save()
            err = False
            cnt_ok += 1
        except Exception as e: log.info(f'Ошибка append_lids: try: {e}')
        if err: cnt_err += 1
    return cnt_ok, cnt_err

def get_key_crm():
    key = '371/ao3ct8et7i7viajs'
    gvar_key, create = DcCrmGlobVar.objects.get_or_create(key='key_crm')
    if create:
        gvar_key.val_str = key
        gvar_key.save()
    else:
        key = gvar_key.val_str
    return key


