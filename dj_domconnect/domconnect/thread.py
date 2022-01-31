from domconnect.models import DcCrmGlobVar, DcCrmLid, DcCashSEO
from django.db.models import Q
import time
import logging
import requests
import json
from datetime import datetime, timedelta
import calendar


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
    print('stop thread')
    calculateSEO()
    print('finish_calculateSEO')
    
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
                # '>DATE_CREATE': '2022-01-01T00:00:00',  # '2021-10-01T00:00:00'
                '>DATE_CREATE': '2021-10-01T00:00:00',  # '2021-10-01T00:00:00'
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
    
    mess = f'Загрузка завершена. Обработано лидов: {cnt_ok}. Ошибок: {cnt_err}'
    gvar_go, _ = DcCrmGlobVar.objects.get_or_create(key='go_download_crm')
    gvar_go.val_bool = False
    gvar_go.val_datetime = datetime.today()
    gvar_go.descriptions = mess
    gvar_go.save()
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

def calculateSEO():
    log = logging.getLogger(__name__)  # запустили логгирование

    ask_date = datetime.today()
    last_month = 0
    last_year = 0
    dcCash = DcCashSEO.objects.all()
    if len(dcCash):
        last_record = dcCash.latest('val_date')
        last_month = last_record.val_date.month
        last_year = last_record.val_date.year
    log.info(f'Последняя запись кэш {last_month}.{last_year}')

    for _ in range(12):
        dct = calculate_1_table(ask_date)
        save_cash(1, dct, ask_date)
        if last_month == ask_date.month and last_year == ask_date.year: break
        ask_date = ask_date - timedelta(days=ask_date.day)
        if len(dct) == 0: break
    log.info(f'Запись кэш завершена.')

def save_cash(table, in_dct, ask_date):
    str_save_date = f'01.{ask_date.month}.{ask_date.year}'
    save_date = datetime.strptime(str_save_date, '%d.%m.%Y')
    for cell, val in in_dct.items():
        row = cell.split('_')[1]
        rec, _ = DcCashSEO.objects.get_or_create(val_date=save_date, table=table, row=row)
        rec.val = val
        rec.save()

def calculate_1_table(ask_date):
    cur_day = ask_date.day      # Номер дня
    cur_month = ask_date.month  # Номер меяца
    cur_year = ask_date.year    # Номер года
    cnt_days_in_month = calendar.monthrange(cur_year, cur_month)[1] # Количество дней в месяце

    working_days = len([x for x in calendar.Calendar().itermonthdays2(cur_year, cur_month) if x[0] !=0 and x[1] < 5])  # Количество рабочих дней в месяце
    weekenddays = cnt_days_in_month - working_days  # выходных дней
    coef_forecast = cnt_days_in_month / cur_day  # Коэфициент полного месяца (для прогноза если месяйц не полный)
    
    out_dict = {}
    lids_all = DcCrmLid.objects.filter(create_date__year=cur_year, create_date__month=cur_month)
    count_lids_all = lids_all.count()
    if count_lids_all:
        lids_seo = lids_all.filter(crm_1592566018='SEO')
        lids_seo_conv = lids_seo.filter(crm_1493416385__gt=50, status_id__contains='CONVERTED')  # Подключаем (SOURCE)
        # (1) Лиды
        cell_01 = round(lids_seo.count() * coef_forecast)
        # (4) Лиды (все)
        cell_04 = round(count_lids_all * coef_forecast)
        # (5) Будн. дней 
        cell_05 = working_days
        # (6) Выходных дней 
        cell_06 = weekenddays
        # (7) Лиды с ТхВ 
        cell_07 = lids_seo.exclude(Q(crm_1571987728429='')|Q(crm_1571987728429=None)).count()  # Провайдеры ДК (длина больше 0)
        # (8) % лидов с ТхВ
        if cell_01: cell_08 = round((cell_07 / cell_01) * 100, 2)
        # (9) Сделки >50
        cell_09 = round(lids_seo_conv.count() * coef_forecast)
        # (10) %Лид=>Сд. >50
        cell_10 = round((cell_09 / cell_01) * 100, 2)
        # (12) Сделки >50 (все)
        cell = lids_all.filter(crm_1493416385__gt=50, status_id__contains='CONVERTED').count()
        cell_12 = round(cell* coef_forecast)
        # (13) Сделки 80
        # https://docs.google.com/spreadsheets/d/1fPFxlhAje5V_kdlSHpLytBbgE6SiBaWtfsrFjw1XYv8/edit#gid=1803529933
        # ('Билайн', 'МТС [кроме МСК и МО]', 'Ростелеком [кроме МСК]', 'МГТС [МСК и МО]')
        cell = lids_seo_conv.filter(crm_1493413514__in=['OTHER', '2', '3', '11']).count()  # Провайдер (INDUSTRY)
        cell_13 = round(cell * coef_forecast)
        # (14) Сд. приоритет (БИ и МТС ФЛ)
        # ('Билайн', 'МТС [кроме МСК и МО]')
        cell = lids_seo_conv.filter(crm_1493413514__in=['OTHER', '2']).count()  # Провайдер (INDUSTRY)
        cell_14 = round(cell * coef_forecast)
        # (15) Доля сделок ПРИОР от сд. >50
        cell_15 = round((cell_14 / cell_09) * 100, 2)
        # (16) Ср. лид/день (будн.)
        cell = lids_seo.filter(create_date__week_day__range=(2,6)).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_16 = round(cell / working_days)
        # (17) Ср. лид/день (вых.)
        cell = lids_seo.filter(create_date__week_day__in=(1,7)).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_17 = round(cell / weekenddays)
        # (18) ТП SEO
        # ('ТП_пр', 'ТП_нраб', 'ТП_моб') https://docs.google.com/spreadsheets/d/1fPFxlhAje5V_kdlSHpLytBbgE6SiBaWtfsrFjw1XYv8/edit#gid=1803529933
        cell_tp_seo = lids_seo.filter(status_id__in=['1', '16', '21', '31', '32', '33']).count()  # Статус (STATUS)
        cell_18 = round(cell_tp_seo * coef_forecast)
        # (19) Расход ТП
        cell_19 = round(cell_tp_seo * 3.4)
        # (20) % ТП
        cell_20 = round((cell_tp_seo / cell_01) * 100, 2)
        # (21) Подключки
        cell_21 = 0
        # (22) ТП IVR Лиза  (ТП_IVR)
        cell_tp_ivr_seo = lids_seo.filter(status_id='52').count()  # Статус (STATUS)
        cell_22 = round(cell_tp_ivr_seo * coef_forecast)
        # (23) % ТП IVR 
        cell_23 = round((cell_tp_ivr_seo / cell_01) * 100, 2)
        # (2) Реальные лиды (без ТП)
        if cell_01: cell_02 = cell_01 - cell_18 - cell_22
        if cell_02:
            # (3) % реальных лидов
            cell_03 = round((cell_02 / cell_01) * 100, 2)
            # (11) Конва реал. лид => сделка >50
            cell_11 = round((cell_09 / cell_02) * 100, 2)
        # (24) % ТП Лизы от всего ТП
        cell_24 = round((cell_22 / (cell_22 + cell_18)) * 100, 2)

        # (25) Понедельник
        cell = lids_all.filter(create_date__week_day=2).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_25 = round(cell * coef_forecast)
        # (26) Вторник
        cell = lids_all.filter(create_date__week_day=3).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_26 = round(cell * coef_forecast)
        # (27) Среда
        cell = lids_all.filter(create_date__week_day=4).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_27 = round(cell * coef_forecast)
        # (28) Четверг
        cell = lids_all.filter(create_date__week_day=5).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_28 = round(cell * coef_forecast)
        # (29) Пятница
        cell = lids_all.filter(create_date__week_day=6).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_29 = round(cell * coef_forecast)
        # (30) Суббота
        cell = lids_all.filter(create_date__week_day=7).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_30 = round(cell * coef_forecast)
        # (31) Воскресенье
        cell = lids_all.filter(create_date__week_day=1).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_31 = round(cell * coef_forecast)

        out_dict['cell_01'] = cell_01
        out_dict['cell_02'] = cell_02
        out_dict['cell_03'] = cell_03
        out_dict['cell_04'] = cell_04
        out_dict['cell_05'] = cell_05
        out_dict['cell_06'] = cell_06
        out_dict['cell_07'] = cell_07
        out_dict['cell_08'] = cell_08
        out_dict['cell_09'] = cell_09
        out_dict['cell_10'] = cell_10
        out_dict['cell_11'] = cell_11
        out_dict['cell_12'] = cell_12
        out_dict['cell_13'] = cell_13
        out_dict['cell_14'] = cell_14
        out_dict['cell_15'] = cell_15
        out_dict['cell_16'] = cell_16
        out_dict['cell_17'] = cell_17
        out_dict['cell_18'] = cell_18
        out_dict['cell_19'] = cell_19
        out_dict['cell_20'] = cell_20
        out_dict['cell_21'] = cell_21
        out_dict['cell_22'] = cell_22
        out_dict['cell_23'] = cell_23
        out_dict['cell_24'] = cell_24
        out_dict['cell_25'] = cell_25
        out_dict['cell_26'] = cell_26
        out_dict['cell_27'] = cell_27
        out_dict['cell_28'] = cell_28
        out_dict['cell_29'] = cell_29
        out_dict['cell_30'] = cell_30
        out_dict['cell_31'] = cell_31

    return out_dict

def calculate_source_table(ask_date):
    cur_day = ask_date.day      # Номер дня
    cur_month = ask_date.month  # Номер меяца
    cur_year = ask_date.year    # Номер года
    cnt_days_in_month = calendar.monthrange(cur_year, cur_month)[1] # Количество дней в месяце

    # working_days = len([x for x in calendar.Calendar().itermonthdays2(cur_year, cur_month) if x[0] !=0 and x[1] < 5])  # Количество рабочих дней в месяце
    # weekenddays = cnt_days_in_month - working_days  # выходных дней
    coef_forecast = cnt_days_in_month / cur_day  # Коэфициент полного месяца (для прогноза если месяйц не полный)
    
    print('ask_date', ask_date, coef_forecast)
    out_dict = {}
    lids_all = DcCrmLid.objects.filter(create_date__year=cur_year, create_date__month=cur_month)
    count_lids_all = lids_all.count()
    if count_lids_all:
        lids_seo = lids_all.filter(crm_1592566018='SEO')
        lids_seo_conv = lids_seo.filter(crm_1493416385__gt=50, status_id__contains='CONVERTED')  # Подключаем (SOURCE)
        # (1) Лиды
        cell_01 = round(lids_seo.count() * coef_forecast)
        # (4) Лиды (все)
        cell_04 = round(count_lids_all * coef_forecast)
        # (5) Будн. дней 
        cell_05 = working_days
        # (6) Выходных дней 
        cell_06 = weekenddays
        # (7) Лиды с ТхВ 
        cell_07 = lids_seo.exclude(Q(crm_1571987728429='')|Q(crm_1571987728429=None)).count()  # Провайдеры ДК (длина больше 0)
        # (8) % лидов с ТхВ
        if cell_01: cell_08 = round((cell_07 / cell_01) * 100, 2)
        # (9) Сделки >50
        cell_09 = round(lids_seo_conv.count() * coef_forecast)
        # (10) %Лид=>Сд. >50
        cell_10 = round((cell_09 / cell_01) * 100, 2)
        # (12) Сделки >50 (все)
        cell = lids_all.filter(crm_1493416385__gt=50, status_id__contains='CONVERTED').count()
        cell_12 = round(cell* coef_forecast)
        # (13) Сделки 80
        # https://docs.google.com/spreadsheets/d/1fPFxlhAje5V_kdlSHpLytBbgE6SiBaWtfsrFjw1XYv8/edit#gid=1803529933
        # ('Билайн', 'МТС [кроме МСК и МО]', 'Ростелеком [кроме МСК]', 'МГТС [МСК и МО]')
        cell = lids_seo_conv.filter(crm_1493413514__in=['OTHER', '2', '3', '11']).count()  # Провайдер (INDUSTRY)
        cell_13 = round(cell * coef_forecast)
        # (14) Сд. приоритет (БИ и МТС ФЛ)
        # ('Билайн', 'МТС [кроме МСК и МО]')
        cell = lids_seo_conv.filter(crm_1493413514__in=['OTHER', '2']).count()  # Провайдер (INDUSTRY)
        cell_14 = round(cell * coef_forecast)
        # (15) Доля сделок ПРИОР от сд. >50
        cell_15 = round((cell_14 / cell_09) * 100, 2)
        # (16) Ср. лид/день (будн.)
        cell = lids_seo.filter(create_date__week_day__range=(2,6)).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_16 = round(cell / working_days)
        # (17) Ср. лид/день (вых.)
        cell = lids_seo.filter(create_date__week_day__in=(1,7)).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_17 = round(cell / weekenddays)
        # (18) ТП SEO
        # ('ТП_пр', 'ТП_нраб', 'ТП_моб') https://docs.google.com/spreadsheets/d/1fPFxlhAje5V_kdlSHpLytBbgE6SiBaWtfsrFjw1XYv8/edit#gid=1803529933
        cell_tp_seo = lids_seo.filter(status_id__in=['1', '16', '21', '31', '32', '33']).count()  # Статус (STATUS)
        cell_18 = round(cell_tp_seo * coef_forecast)
