from domconnect.models import DcCrmGlobVar, DcCrmLid, DcCashSEO, DcSiteSEO, DcCrmDeal, DcSourceSEO
from domconnect.models import DcCatalogProviderSEO, DcCatalogSourceSEO
from django.db.models import Q, Avg
from decimal import Decimal
from datetime import datetime, timedelta
import os, time, logging, requests, json, calendar, copy
from django.http import HttpResponse
import csv, codecs


logging.basicConfig(
    level=logging.INFO,     # DEBUG, INFO, WARNING, ERROR и CRITICAL По возрастанию
    filename='main.log',
    format='%(asctime)s:%(name)s:%(message)s'
)
# logger.info('So should this')
# # # # logger.debug('This message should go to the log file')
# # # # logger.warning('And this, too')
logger = logging.getLogger(__name__)  # запустили логгирование

# date_create = '2021-01-01T00:00:00'
date_create = '2022-04-16T00:00:00'

typesource = {}
typelid = {}
# services = {
#         '191': 'Интернет',
#         '192': 'Цифровое ТВ',
#         '3381': 'Smart TV',
#         '196': 'СИМ-карта',
#         '197': 'Wi-Fi роутер',
#         '546': 'ПЕРЕЕЗД',
#         '193': 'Кабельное ТВ',
#         '195': 'Телефония',
#         '194': 'Спутниковое ТВ',
#         '3402': 'Видеонаблюдение',
# }
##### Основная таблица список строк
row_0_names = [
    'Лиды',
    'Реальные лиды(без ТП)',
    '% реальных лидов',
    'Лиды (все)',
    'Будн. дней',
    'Выходных дней',
    'Лиды с ТхВ',
    '% лидов с ТхВ',
    'Сделки >50',
    '%Лид=>Сд. >50',
    'Конва реал. лид =>сделка >50',
    'Сделки >50 (все)',
    'Сделки 80',
    'Сд. приоритет (БИ и МТС ФЛ)',
    'Доля сделок ПРИОР от сд.>50',
    'Ср. лид/день (будн.)',
    'Ср. лид/день (вых.)',
    'ТП SEO',
    'Расход ТП',
    '% ТП',
    'Подключки по дате лида',
    'Подключки по дате оплаты',
    'ТП IVR Лиза',
    '% ТП IVR',
    '% ТП Лизы от всего ТП',
    'Понедельник',
    'Вторник',
    'Среда',
    'Четверг',
    'Пятница',
    'Суббота',
    'Воскресенье',
]
##### Сводные таблицы сайтов список строк
row_site_names = [
    'Лиды',
    'Конв. пос. => лид',
    'Реальные лиды',
    '% реал. лидов',
    'Лиды ТхВ',
    'Сделки',
    'Конв. лиды => сделка',
    'Конв. посет => сделка',			
    'Сделки >50',
    'Конв. >50',
    'Сделки 80',
    'Сд. приоритет (БИ и МТС ФЛ)',
    'Конв. приоритет',
    'Конв. реал. лид =>сделка',
    'Кол-во звонков',
    'Кол-во заявок',
    '% звонков от заявок',
    '% приор. сделок заявка',
    '% приор. сделок звонок',
    'Конв. посет => лид',
    'Конв. посет => сделка',
    'ТП',
    'ТП IVR',
    'Посетители',
    'Ср. чек (сделки)',
    'Сделки >50',
]
##### Таблицы источников список строк
row_source_names = [
    'Лиды',
    'Сделки',
    'Сделки > 50',
    'Сд. приоритет',
    'Ср. чек',
    'Подключки по дате лида',
    'Подключки по дате оплаты',
    'ТП',
    'ТП IVR',
    'SEO Лиды ТхВ',
    'Сделки',
    'Сделки >50',
]


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal): return str(obj)
        return json.JSONEncoder.default(self, obj)

def run_upgrade_seo(*args, **options):
    # # # # http_request = False
    # # # # if args and isinstance(args[0], object) and type(args[0]) == WSGIRequest: http_request = True

    gvar_go, _ = DcCrmGlobVar.objects.get_or_create(key='go_upgrade_seo')
    if gvar_go.val_bool == True:
        print('Идет процесс обновления данных SEO и расчета.')
        return
    mess = 'Обновение данных SEO запущено.'
    gvar_go.val_bool = True
    gvar_go.val_datetime = datetime.today()
    gvar_go.descriptions = mess
    gvar_go.save()
    logger.info(mess)
    print(mess)

    dounload_catalog()
    download_typesource()
    download_typelid()
    download_deals()
    download_lids()
    calculateSEO()
    make_seo_page()

    mess = 'Расчет и сохранение данных SEO в кэш закончено.'
    gvar_go = DcCrmGlobVar.objects.get(key='go_upgrade_seo')
    gvar_go.val_bool = False
    gvar_go.val_datetime = datetime.today()
    gvar_go.descriptions = mess
    gvar_go.save()
    logger.info(mess)
    print(mess)

def dounload_catalog():
    '''
        Загрузка и обновление каталога провайдеров и источников
        провайдеры
        https://domconnect.ru/api.get_crm_info?apikey=ace5aea03144bfea692ab289f3045bfd6a7f2440da8ba809&type=providers
        источники
        https://domconnect.ru/api.get_crm_info?apikey=ace5aea03144bfea692ab289f3045bfd6a7f2440da8ba809&type=source
    '''
    url = 'https://domconnect.ru/api.get_crm_info?apikey=ace5aea03144bfea692ab289f3045bfd6a7f2440da8ba809&type=providers'
    try:
        responce = requests.post(url)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            response = answer.get('response')
            for res in response:
                name = res.get('NAME')
                prov_id = res.get('STATUS_ID')
                _, _ = DcCatalogProviderSEO.objects.get_or_create(name=name, prov_id=prov_id)
        else: return logger.info(f'Ошибка dounload_catalog: responce.status_code: {responce.status_code}\n{responce.text}')
    except Exception as e: logger.info(f'Ошибка dounload_catalog: try: requests.post {e}')

    url = 'https://domconnect.ru/api.get_crm_info?apikey=ace5aea03144bfea692ab289f3045bfd6a7f2440da8ba809&type=source'
    try:
        responce = requests.post(url)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            response = answer.get('response')
            for res in response:
                name = res.get('NAME')
                source_id = res.get('STATUS_ID')
                _, _ = DcCatalogSourceSEO.objects.get_or_create(name=name, source_id=source_id)
        else: return logger.info(f'Ошибка dounload_catalog: responce.status_code: {responce.status_code}\n{responce.text}')
    except Exception as e: logger.info(f'Ошибка dounload_catalog: try: requests.post {e}')

def get_key_crm():
    gvar_key, create = DcCrmGlobVar.objects.get_or_create(key='key_crm')
    key_crm = ''
    if create:
        key_crm = '371/ao3ct8et7i7viajs'
        gvar_key.val_str = key_crm
        gvar_key.save()
    else:
        key_crm = gvar_key.val_str
    return key_crm

def download_typesource():  # Обновление Типов источника лида
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
                    logger.info(f'Ошибка download_typesource: error status_id: {status_id}')
                    continue
                typesource[status_id] = res.get('NAME')
        else: return logger.info(f'Ошибка download_typesource: responce.status_code: {responce.status_code}\n{responce.text}')
    except Exception as e: logger.info(f'Ошибка download_typesource: try: requests.post {e}')

def download_typelid():  # Обновление Типов лида
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
        else: return logger.info(f'Ошибка download_typelid: responce.status_code: {responce.status_code}\n{responce.text}')
    except Exception as e: logger.info(f'Ошибка download_typelid: try: requests.post {e}')

def download_deals():
    key_crm = get_key_crm()
    url = f'https://crm.domconnect.ru/rest/{key_crm}/crm.deal.list'
    
    str_from_modify = ''
    last_modify_lid = DcCrmDeal.objects.order_by('modify_date').last()
    if last_modify_lid:
        from_modify = last_modify_lid.modify_date
        if type(from_modify) == datetime:
            from_modify = from_modify - timedelta(seconds=1)
            str_from_modify = from_modify.strftime('%Y-%m-%dT%H:%M:%S')

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
        gvar_go = DcCrmGlobVar.objects.get(key='go_upgrade_seo')
        if gvar_go.val_bool == False: break
        if go_next == None: go_next = 0 
        data = {
            'start': go_next,
            'order': {'DATE_MODIFY': 'ASC'},  # С сортировкой
            'filter': {
                'STAGE_ID': 'WON',  # Подключен. Оплачен провайдером** только для РОПа
                '>DATE_CREATE': date_create,  # '2021-10-01T00:00:00'
            },
            'select': [
                'ID',
                'SOURCE_ID',
                'DATE_CREATE',
                'DATE_MODIFY',
                'UF_CRM_5904FB99DBF0C',  # Дата подключения
                'UF_CRM_5EECA3B76309E',  # Дата лида
                'UF_CRM_5903C16BCEE3A',  # Услуги  []
                'UF_CRM_5903C16BDAA69',  # Сумма тарифа
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
                print('deals', go_next, go_total)
                ok, err = append_deals(result)
                cnt_ok += ok; cnt_err += err
                if not go_next: break
            else: logger.info(f'Ошибка download_deals: responce.status_code: {responce.status_code}\n{responce.text}')
        except Exception as e: logger.info(f'Ошибка download_deals: try: requests.post {e}')
        time.sleep(1)
    
    logger.info(f'Загрузка завершена. Обработано сделок: {cnt_ok}. Ошибок: {cnt_err}')

def append_deals(deals):
    cnt_err = 0
    cnt_ok = 0
    for new_deal in deals:
        err = True
        try:
            deal, _ = DcCrmDeal.objects.get_or_create(id_deal=new_deal.get('ID'))
            deal.create_date = datetime.strptime(new_deal.get('DATE_CREATE')[:-6], '%Y-%m-%dT%H:%M:%S')  # "2022-01-01T04:43:22+03:00"
            deal.modify_date = datetime.strptime(new_deal.get('DATE_MODIFY')[:-6], '%Y-%m-%dT%H:%M:%S')
            val_field = new_deal.get('SOURCE_ID')
            if val_field:
                if not val_field in typesource: deal.source_id = val_field
                else: deal.source_id = typesource[val_field]
            val_field = new_deal.get('UF_CRM_5904FB99DBF0C')  # Дата подключения
            if val_field: deal.crm_5904FB99DBF0C = datetime.strptime(val_field[:-6], '%Y-%m-%dT%H:%M:%S')
            val_field = new_deal.get('UF_CRM_5EECA3B76309E')  # Дата лида
            if val_field: deal.crm_5EECA3B76309E = datetime.strptime(val_field[:-6], '%Y-%m-%dT%H:%M:%S')
            val_field = new_deal.get('UF_CRM_5903C16BCEE3A')  # Услуги  []
            if val_field:
                val_field = [str(x) for x in val_field]
                deal.crm_5903C16BCEE3A = ';'.join(val_field)
            val_field = new_deal.get('UF_CRM_5903C16BDAA69')  # Сумма тарифа
            if val_field: deal.crm_5903C16BDAA69 = val_field
            deal.save()
            err = False
            cnt_ok += 1
        except Exception as e:
            DcCrmDeal.objects.filter(id_deal=new_deal.get('ID')).delete()
            logger.info(f'Ошибка append_deals: {new_deal.get("ID")} try: {e}')
        if err: cnt_err += 1
    return cnt_ok, cnt_err

def download_lids():
    key_crm = get_key_crm()
    url = f'https://crm.domconnect.ru/rest/{key_crm}/crm.lead.list'
    
    str_from_modify = ''
    last_modify_lid = DcCrmLid.objects.order_by('modify_date').last()
    if last_modify_lid:
        from_modify = last_modify_lid.modify_date
        if type(from_modify) == datetime:
            from_modify = from_modify - timedelta(seconds=1)
            str_from_modify = from_modify.strftime('%Y-%m-%dT%H:%M:%S')

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
        gvar_go = DcCrmGlobVar.objects.get(key='go_upgrade_seo')
        if gvar_go.val_bool == False: break
        if go_next == None: go_next = 0 
        data = {
            'start': go_next,
            'order': {'DATE_MODIFY': 'ASC'},  # С сортировкой
            'filter': {
                '>DATE_CREATE': date_create,  # '2021-10-01T00:00:00'
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
                print('lids', go_next, go_total)
                ok, err = append_lids(result)
                cnt_ok += ok; cnt_err += err
                if not go_next: break
            else: logger.info(f'Ошибка download_lids: responce.status_code: {responce.status_code}\n{responce.text}')
        except Exception as e: logger.info(f'Ошибка download_lids: try: requests.post {e}')
        time.sleep(1)
    
    logger.info(f'Загрузка завершена. Обработано лидов: {cnt_ok}. Ошибок: {cnt_err}')

def append_lids(lids):
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
            if val_field:
                 if len(val_field) > 0: lid.crm_1534919765 = val_field[0]
            val_field = new_lid.get('UF_CRM_1571987728429')
            if val_field: lid.crm_1571987728429 = val_field
            val_field = new_lid.get('UF_CRM_1592566018')
            if val_field:
                if len(val_field) > 0:
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
        except Exception as e:
            DcCrmLid.objects.filter(id_lid=new_lid.get('ID')).delete()
            logger.info(f'Ошибка append_lids: {new_lid.get("ID")} try: {e}')
        if err: cnt_err += 1
    return cnt_ok, cnt_err

def calculateSEO():
    # Расчетная дата будет начиная со вчера. Т.о. в расчет не берутся сегодняшние данные как неполные
    calc_date = datetime.today() - timedelta(days=1)
    last_month = 0
    last_year = 0
    dcCash = DcCashSEO.objects.all()
    if len(dcCash):
        last_record = dcCash.latest('val_date')
        last_month = last_record.val_date.month
        last_year = last_record.val_date.year

    # Вычислим количество месяцев (столбцов) для вывода начиная с 01.01.2021г.
    date_start = datetime(2020, 12, 31)
    num_months = (calc_date.year - date_start.year) * 12 + calc_date.month - date_start.month
    
    for _ in range(num_months):
        empty_data_month = True
        # Расчет основной таблицы (Метка SEO)
        dct = calculate_0_table(calc_date)
        if len(dct) > 0:
            empty_data_month = False
            # Сохранение в кэш основной таблицы (Метка SEO)
            save_cash(0, 0, dct, calc_date)

        # Берем список сайтов
        objs_site = DcSiteSEO.objects.all().order_by('num')
        for obj_site in objs_site:
            site_num = obj_site.num
            try: site_provider = DcCatalogProviderSEO.objects.get(name=obj_site.provider).prov_id
            except: site_provider = obj_site.provider
            lst_res_source = []  # Результирующий список результатов вычислений источников
            # По каждому сайту берем список источников
            sources = obj_site.sources.order_by('num')
            for src in sources:
                source_name = src.source
                source_num = src.num
                # По каждому источнику делаем вычисления
                dct_source = calculate_source_table(calc_date, source_name, site_provider)
                if len(dct_source) > 0:
                    empty_data_month = False
                    # Костыль !!!
                    if site_num == 4:  # сайт https://mtsru.ru/
                        dct_cost = calculate_source_table(calc_date, source_name, '11')
                        dct_source['cell_13'] = dct_cost['cell_12']
                    # Сохранение в кэш таблицы источника
                    save_cash(site_num, source_num, dct_source, calc_date)
                    lst_res_source.append(dct_source)

            if len(lst_res_source) > 0:
                dct_site = calculate_site_table(lst_res_source)
                if len(dct_site) > 0:
                    empty_data_month = False
                    # Сохранение в кэш таблицы источника
                    save_cash(site_num, 0, dct_site, calc_date)
        
        if last_month == calc_date.month and last_year == calc_date.year: break
        calc_date = calc_date - timedelta(days=calc_date.day)
        if empty_data_month: break

def save_cash(num_site, num_source, in_dct, calc_date):
    str_save_date = f'01.{calc_date.month}.{calc_date.year}'
    save_date = datetime.strptime(str_save_date, '%d.%m.%Y')
    for cell, val in in_dct.items():
        row = cell.split('_')[1]
        rec, _ = DcCashSEO.objects.get_or_create(val_date=save_date, num_site=num_site, num_source=num_source, row=row)
        rec.val = val
        rec.save()

def calculate_0_table(ask_date):
    yest_date = datetime.today() - timedelta(days=1)
    # Является ли запрашиваемый месяц текущим
    is_current_month = False
    if yest_date.year == ask_date.year and yest_date.month == ask_date.month: is_current_month = True

    cur_month = ask_date.month  # Номер меяца
    cur_year = ask_date.year    # Номер года
    cnt_days_in_month = calendar.monthrange(cur_year, cur_month)[1] # Количество дней в месяце
    working_days = len([x for x in calendar.Calendar().itermonthdays2(cur_year, cur_month) if x[0] !=0 and x[1] < 5])  # Количество рабочих дней в месяце
    weekenddays = cnt_days_in_month - working_days  # выходных дней
    
              
    out_dict = {}
    if is_current_month:  # __lte <= ;  __gte >=
        lids_all = DcCrmLid.objects.filter(create_date__year=cur_year, create_date__month=cur_month, create_date__day__lte=ask_date.day).exclude(status_id__in=[17, 24])  # '!STATUS_ID': [17, 24],    # Дубль и ошибка в телефоне
    else:
        lids_all = DcCrmLid.objects.filter(create_date__year=cur_year, create_date__month=cur_month).exclude(status_id__in=[17, 24])  # '!STATUS_ID': [17, 24],    # Дубль и ошибка в телефоне
    count_lids_all = lids_all.count()
    if count_lids_all == 0: return out_dict

    lids_seo = lids_all.filter(crm_1592566018='SEO')
    lids_seo_conv = lids_seo.filter(crm_1493416385__gt=50, status_id__contains='CONVERTED')  # Подключаем (SOURCE)
    
    cell_02 = cell_03 = cell_08 = cell_10 = cell_11 = cell_15 = cell_20 = cell_24 = cell_25  = 0
    # (1) Лиды
    cell_01 = lids_seo.count()
    # (4) Лиды (все)
    cell_04 = count_lids_all
    # (5) Будн. дней 
    cell_05 = working_days
    # (6) Выходных дней 
    cell_06 = weekenddays
    # (7) Лиды с ТхВ
    cell_07 = lids_seo.exclude(Q(crm_1571987728429='')|Q(crm_1571987728429=None)).count()  # Провайдеры ДК (длина больше 0)
    # (8) % лидов с ТхВ
    if cell_01: cell_08 = round((cell_07 / cell_01) * 100, 2)
    # (9) Сделки >50
    cell_09 = lids_seo_conv.count()
    # (10) %Лид=>Сд. >50
    if cell_01: cell_10 = round((cell_09 / cell_01) * 100, 2)
    # (12) Сделки >50 (все)
    cell_12 = lids_all.filter(crm_1493416385__gt=50, status_id__contains='CONVERTED').count()
    # (13) Сделки 80
    # https://docs.google.com/spreadsheets/d/1fPFxlhAje5V_kdlSHpLytBbgE6SiBaWtfsrFjw1XYv8/edit#gid=1803529933
    # ('Билайн', 'МТС [кроме МСК и МО]', 'Ростелеком [кроме МСК]', 'МГТС [МСК и МО]')
    cell_13 = lids_seo_conv.filter(crm_1493413514__in=['OTHER', '2', '3', '11']).count()  # Провайдер (INDUSTRY)
    # (14) Сд. приоритет (БИ и МТС ФЛ)
    # ('Билайн', 'МТС [кроме МСК и МО]')
    cell_14 = lids_seo_conv.filter(crm_1493413514__in=['OTHER', '2']).count()  # Провайдер (INDUSTRY)
    # (15) Доля сделок ПРИОР от сд. >50
    if cell_09: cell_15 = round((cell_14 / cell_09) * 100, 2)
    # (16) Ср. лид/день (будн.)
    cell = lids_seo.filter(create_date__week_day__range=(2,6)).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
    cell_16 = round(cell / working_days)
    # (17) Ср. лид/день (вых.)
    cell = lids_seo.filter(create_date__week_day__in=(1,7)).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
    cell_17 = round(cell / weekenddays)
    # (18) ТП SEO
    # ('ТП_пр', 'ТП_нраб', 'ТП_моб') https://docs.google.com/spreadsheets/d/1fPFxlhAje5V_kdlSHpLytBbgE6SiBaWtfsrFjw1XYv8/edit#gid=1803529933
    cell_18 = lids_seo.filter(status_id__in=['1', '16', '21', '31', '32', '33']).count()  # Статус (STATUS)
    # (19) Расход ТП
    cell_19 = round(cell_18 * 3.4)
    # (20) % ТП
    if cell_01: cell_20 = round((cell_18 / cell_01) * 100, 2)
    else: cell_20 = 0
    # (21) Подключки по дате лида
    if is_current_month:
        cell_21 = DcCrmDeal.objects.filter(crm_5EECA3B76309E__year=cur_year, crm_5EECA3B76309E__month=cur_month, crm_5EECA3B76309E__day__lte=ask_date.day).count()
    else:
        cell_21 = DcCrmDeal.objects.filter(crm_5EECA3B76309E__year=cur_year, crm_5EECA3B76309E__month=cur_month).count()
    # (22) Подключки по дате оплаты
    if is_current_month:
        cell_22 = DcCrmDeal.objects.filter(crm_5904FB99DBF0C__year=cur_year, crm_5904FB99DBF0C__month=cur_month, crm_5904FB99DBF0C__day__lte=ask_date.day).count()
    else:
        cell_22 = DcCrmDeal.objects.filter(crm_5904FB99DBF0C__year=cur_year, crm_5904FB99DBF0C__month=cur_month).count()
    # (23) ТП IVR Лиза  (ТП_IVR)
    cell_23 = lids_seo.filter(status_id='52').count()  # Статус (STATUS)
    # (24) % ТП IVR 
    if cell_01: cell_24 = round((cell_23 / cell_01) * 100, 2)
    # (2) Реальные лиды (без ТП)
    if cell_01: cell_02 = cell_01 - cell_18 - cell_23
    if cell_02:
        # (3) % реальных лидов
        if cell_01: cell_03 = round((cell_02 / cell_01) * 100, 2)
        # (11) Конва реал. лид => сделка >50
        if cell_02: cell_11 = round((cell_09 / cell_02) * 100, 2)
    # (25) % ТП Лизы от всего ТП
    if (cell_23 + cell_18): cell_25 = round((cell_23 / (cell_23 + cell_18)) * 100, 2)

    # (26) Понедельник
    cell_26 = lids_all.filter(create_date__week_day=2).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
    # (27) Вторник
    cell_27 = lids_all.filter(create_date__week_day=3).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
    # (28) Среда
    cell_28 = lids_all.filter(create_date__week_day=4).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
    # (29) Четверг
    cell_29 = lids_all.filter(create_date__week_day=5).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
    # (30) Пятница
    cell_30 = lids_all.filter(create_date__week_day=6).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
    # (31) Суббота
    cell_31 = lids_all.filter(create_date__week_day=7).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
    # (32) Воскресенье
    cell_32 = lids_all.filter(create_date__week_day=1).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)

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
    out_dict['cell_32'] = cell_32

    return out_dict

def calculate_source_table(ask_date, ask_source, ask_provider):
    yest_date = datetime.today() - timedelta(days=1)
    # Является ли запрашиваемый месяц текущим
    is_current_month = False
    if yest_date.year == ask_date.year and yest_date.month == ask_date.month: is_current_month = True

    cur_month = ask_date.month  # Номер меяца
    cur_year = ask_date.year    # Номер года
    
    out_dict = {}
    if is_current_month:
        lids_all = DcCrmLid.objects.filter(create_date__year=cur_year, create_date__month=cur_month, create_date__day__lte=ask_date.day, source_id=ask_source)
    else:
        lids_all = DcCrmLid.objects.filter(create_date__year=cur_year, create_date__month=cur_month, source_id=ask_source)
    count_lids_all = lids_all.count()
    if count_lids_all == 0: return out_dict

    # (1) Лиды
    cell_01 = count_lids_all
    # (2) Сделки
    cell_conv = lids_all.filter(status_id__contains='CONVERTED')
    cell_02 = cell_conv.count()
    # (3) Сделки > 50
    cell_conv_sum = cell_conv.filter(crm_1493416385__gt=50)
    cell_03 = cell_conv_sum.count()
    # (4) Сд. приоритет
    # Провайдер=('МТС [кроме МСК и МО]' или 'Билайн')
    cell_04 = cell_conv.filter(crm_1499437861='', crm_1493413514__in=['2', 'OTHER']).count()
    # (5) Ср. чек
    dct = cell_conv.aggregate(avg=Avg('crm_1493416385'))
    avg = dct.get('avg')
    if avg: cell_05 = round(avg)
    else: cell_05 = 0
    # (6) Подключки по дате лида
    if is_current_month:
        cell_06 = DcCrmDeal.objects.filter(crm_5EECA3B76309E__year=cur_year, crm_5EECA3B76309E__month=cur_month, crm_5EECA3B76309E__day__lte=ask_date.day, source_id=ask_source).count()
    else:
        cell_06 = DcCrmDeal.objects.filter(crm_5EECA3B76309E__year=cur_year, crm_5EECA3B76309E__month=cur_month, source_id=ask_source).count()
    # (7) Подключки по дате оплаты
    if is_current_month:
        cell_07 = DcCrmDeal.objects.filter(crm_5904FB99DBF0C__year=cur_year, crm_5904FB99DBF0C__month=cur_month, crm_5904FB99DBF0C__day__lte=ask_date.day, source_id=ask_source).count()
    else:
        cell_07 = DcCrmDeal.objects.filter(crm_5904FB99DBF0C__year=cur_year, crm_5904FB99DBF0C__month=cur_month, source_id=ask_source).count()
    # (8) ТП
    # ('ТП_пр' или 'ТП_нраб' или 'ТП_моб')
    cell_08 = lids_all.filter(status_id__in=['1', '16', '21', '31', '32', '33']).count()
    # (9) ТП IVR
    # ('ТП IVR')
    cell_09 = lids_all.filter(status_id__in=['52',]).count()
    # (10) SEO Лиды ТхВ
    cell_10 = lids_all.exclude(Q(crm_1571987728429='')).count()
    # (11) Сделки 80
    # https://docs.google.com/spreadsheets/d/1fPFxlhAje5V_kdlSHpLytBbgE6SiBaWtfsrFjw1XYv8/edit#gid=1803529933
    # ('Билайн', 'МТС [кроме МСК и МО]', 'Ростелеком [кроме МСК]', 'МГТС [МСК и МО]')
    cell_11 = cell_conv_sum.filter(crm_1493413514__in=['OTHER', '2', '3', '11']).count()   # Провайдер (INDUSTRY)
    # (12) Сделки >50
    # # # # # провайдер из переменной ask_provider(список). Для мультибрендовых источников - несколько значений
    # # # # # lst = ask_provider.split(';')
    # # # # # cell_12 = cell_conv_sum.filter(crm_1493413514__in=lst).count()  # Провайдер (INDUSTRY)
    cell_12 = cell_conv_sum.filter(crm_1493413514=ask_provider).count()  # Провайдер (INDUSTRY)

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

    return out_dict

def calculate_site_table(lst_res_source):
    # На входе список словарей от источников
    # Собираем данные для таблицы сайта
    out_dict = {}
    count_source = len(lst_res_source)
    if count_source == 0: return out_dict

    cell_01 = 0
    cell_02 = 0
    cell_03 = 0
    cell_04 = 0
    cell_05 = 0
    cell_06 = 0
    cell_07 = 0
    cell_08 = 0
    cell_09 = 0
    cell_10 = 0
    cell_11 = 0
    cell_12 = 0
    cell_13 = 0
    cell_14 = 0
    cell_15 = 0
    cell_16 = 0
    cell_17 = 0
    cell_18 = 0
    cell_19 = 0
    cell_20 = 0
    cell_21 = 0
    cell_22 = 0
    cell_23 = 0
    cell_24 = 0  # Посетители
    cell_25 = 0
    cell_26 = 0
    cell_27 = 0  # Для костыля по МГТС
    cost = False

    # Соберем суммы значений по источникам
    for src in lst_res_source:
        cell_01 += src['cell_01']
        cell_05 += src['cell_10']
        cell_06 += src['cell_02']
        cell_09 += src['cell_03']
        cell_11 += src['cell_11']
        cell_12 += src['cell_04']
        cell_22 += src['cell_08']
        cell_23 += src['cell_09']
        cell_25 += src['cell_05']
        cell_26 += src['cell_12']
        val_cost = src.get('cell_13')
        if val_cost != None:
            cost = True
            cell_27 += val_cost

    cell_25 = round(cell_25 / count_source)

    # Если поле "Посетители" есть - посчитать здесь

    # (2) Конв. пос. => лид
    if cell_24: cell_02 = round((cell_01 / cell_24) * 100, 2)
    # (3) Реальные лиды
    cell_03 = cell_01 - cell_22
    # (4) % реал. лидов
    if cell_01: cell_04 = round((cell_03 / cell_01) * 100, 2)
    # (7) Конв. лиды => сделка
    if cell_01: cell_07 = round((cell_06 / cell_01) * 100, 2)
    # (8) Конв. посет => сделка
    if cell_24: cell_08 = round((cell_06 / cell_24) * 100, 2)
    # (10) Конв. >50
    if cell_01: cell_10 = round((cell_09 / cell_01) * 100, 2)
    # (13) Конв. >50
    if cell_01: cell_13 = round((cell_12 / cell_01) * 100, 2)
    # (14) Конв. реальный лид
    if cell_03: cell_14 = round((cell_12 / cell_03) * 100, 2)
    # (16) Кол-во заявок
    cell_16 = lst_res_source[0]['cell_01']
    # (15) Кол-во звонков
    cell_15 = cell_01 - cell_16
    # (17) % звонков от заявок 
    if cell_16: cell_17 = round((cell_15 / cell_16) * 100, 2)
    # (18) % приор. сделок заявка
    if cell_16: cell_18 = round((cell_12 / cell_16) * 100, 2)
    # (19) % приор. сделок звонок
    if cell_15: cell_19 = round((cell_12 / cell_15) * 100, 2)
    # (20) Конв. посет => лид
    if cell_24: cell_20 = round((cell_01 / cell_24) * 100, 2)
    # (21) Конв. посет => лид
    if cell_24: cell_21 = round((cell_06 / cell_24) * 100, 2)

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
    if cost:
        out_dict['cell_27'] = cell_27
    return out_dict

def make_seo_page():
    try:
        out_data = {}

        # Расчетная дата будет начиная со вчера. Т.о. в расчет не берутся сегодняшние данные как неполные
        calc_date = datetime.today() - timedelta(days=1)

        # Вычислим коэфициент для прогноза на текущий месяц
        cur_day = calc_date.day      # Номер дня
        cur_month = calc_date.month  # Номер меяца
        cur_year = calc_date.year    # Номер года
        cnt_days_in_month = calendar.monthrange(cur_year, cur_month)[1] # Количество дней в месяце
        coef_forecast = Decimal(cnt_days_in_month / cur_day)  # Коэфициент полного месяца (для прогноза если месяйц не полный)

        # Вычислим количество месяцев (столбцов) для вывода начиная с 01.01.2021г.
        date_start = datetime(2020, 12, 31)
        num_months = (cur_year - date_start.year) * 12 + cur_month - date_start.month

        # Собираем строку заголовков и основную таблицу
        str_month = ['', 'Янв.', 'Фев.', 'Мар.', 'Апр.', 'Май', 'Июн.', 'Июл.', 'Авг.', 'Сен.', 'Окт.', 'Ноя.', 'Дек.']
        col_date = copy.deepcopy(calc_date)
        data_month = []
        data_0_table = []
        for _ in range(num_months):  # old=12
            s_date = f'01.{col_date.month}.{col_date.year}'
            f_date = datetime.strptime(s_date, '%d.%m.%Y')
            c_data = DcCashSEO.objects.filter(val_date=f_date, num_site=0, num_source=0).order_by('row')
            data_month.append(f'{str_month[col_date.month]} {col_date.year}')
            c_row = {}
            if col_date.month == cur_month and col_date.year == cur_year: forecast = True
            else: forecast = False
            for j in range(len(c_data)):
                val = c_data[j].val
                if forecast and j not in [2, 4, 5, 7, 9, 10, 14, 19, 23, 24]:
                    c_row[c_data[j].row] = round(val * coef_forecast, 2)
                else: c_row[c_data[j].row] = val
            data_0_table.append(c_row)
            col_date = col_date - timedelta(days=col_date.day)
        data_month.reverse()
        data_month += ['График', 'Сравн. мес', f'{str_month[cur_month]} ФАКТ']
        data_0_table.reverse()

        # Добавляем дополнительные столбцы "График", "Сравн. мес" и "месяц ФАКТ"
        col_fabula = {}  # Шаблон новых колонок
        for i in range(1, len(row_0_names)+1): col_fabula[i] = ''
        col_gr = copy.deepcopy(col_fabula)  # словарь с ключами строк таблицы
        col_cm = copy.deepcopy(col_fabula)  # словарь с ключами строк таблицы
        col_ft = copy.deepcopy(col_fabula)  # словарь с ключами строк таблицы

        s_date = f'01.{cur_month}.{cur_year}'
        f_date = datetime.strptime(s_date, '%d.%m.%Y')
        obj_cur_month = DcCashSEO.objects.filter(val_date=f_date, num_site=0, num_source=0)
        for key, _ in col_fabula.items():
            gr = []
            for i in range(num_months): 
                val = data_0_table[i].get(key)
                try: val = int(val)
                except: val = 0
                gr.append(val)
            col_gr[key] = gr
            # Для колонки "Сравн. мес" вычислим значение
            col_cm[key] = 0
            num_new = data_0_table[num_months-1].get(key)
            num_old = data_0_table[num_months-2].get(key)
            if num_new != None and num_old != None and num_old != 0:
                cm = round((num_new / num_old - 1) * 100)
                col_cm[key] = cm
            try: col_ft[key] = obj_cur_month.get(row=key).val
            except: col_ft[key] = ''
        data_0_table.append(col_gr)  # 13 колонка "График"
        data_0_table.append(col_cm)  # 14 колонка "Сравн. мес"
        data_0_table.append(col_ft)  # 14 колонка "месяц ФАКТ"

        out_data['data_month'] = data_month
        out_data['data_0_table'] = data_0_table

        # with open('data_0_table.json', 'w', encoding='utf-8') as out_file:
        #     json.dump(data_0_table, out_file, ensure_ascii=False, indent=4)

        # Собираем таблицы сайтов с источниками
        data_sites = []
        objs_site = DcSiteSEO.objects.all().order_by('num')
        for obj_site in objs_site:
            item_sites = {'id': obj_site.num, 'url_site': obj_site.site, 'name_site': obj_site.name}
            
            # Таблицы сайта по месяцам
            site_table = []  # Список словарей по месяцам сводной таблицы сайта
            col_date = copy.deepcopy(calc_date)
            for _ in range(num_months):
                s_date = f'01.{col_date.month}.{col_date.year}'
                f_date = datetime.strptime(s_date, '%d.%m.%Y')
                c_data = DcCashSEO.objects.filter(val_date=f_date, num_site=obj_site.num, num_source=0).order_by('row')
                c_row = {}
                if col_date.month == cur_month and col_date.year == cur_year: forecast = True
                else: forecast = False
                for j in range(len(c_data)):
                    val = c_data[j].val
                    if forecast and j not in [1, 3, 6, 7, 9, 12, 13, 16, 17, 18, 19, 20]:
                        c_row[c_data[j].row] = round(val * coef_forecast, 2)
                    else: c_row[c_data[j].row] = val
                site_table.append(c_row)
                col_date = col_date - timedelta(days=col_date.day)
            site_table.reverse()

            # Добавляем дополнительные столбцы "График" и "Сравн. мес" и "месяц ФАКТ"
            col_fabula = {}  # Шаблон новых колонок
            for i in range(1, len(row_site_names)+1): col_fabula[i] = ''
            if obj_site.num == 4: col_fabula[len(row_site_names)+1] = ''
            s_date = f'01.{cur_month}.{cur_year}'
            f_date = datetime.strptime(s_date, '%d.%m.%Y')
            obj_cur_month = DcCashSEO.objects.filter(val_date=f_date, num_site=obj_site.num, num_source=0)
            col_gr = copy.deepcopy(col_fabula)  # словарь с ключами строк таблицы
            col_cm = copy.deepcopy(col_fabula)  # словарь с ключами строк таблицы
            col_ft = copy.deepcopy(col_fabula)  # словарь с ключами строк таблицы

            for key, _ in col_fabula.items():
                gr = []
                for i in range(num_months): 
                    val = site_table[i].get(key)
                    try: val = int(val)
                    except: val = 0
                    gr.append(val)
                col_gr[key] = gr
                # Для колонки "Сравн. мес" вычислим значение
                col_cm[key] = 0
                num_new = site_table[num_months-1].get(key)
                num_old = site_table[num_months-2].get(key)
                if num_new != None and num_old != None and num_old != 0:
                    cm = round((num_new / num_old - 1) * 100)
                    col_cm[key] = cm
                try: col_ft[key] = obj_cur_month.get(row=key).val
                except: col_ft[key] = ''
            site_table.append(col_gr)  # 13 колонка "График"
            site_table.append(col_cm)  # 14 колонка "Сравн. мес"
            site_table.append(col_ft)  # 14 колонка "месяц ФАКТ"
            item_sites['site_table'] = site_table
            
            # Проход по источникам сайта
            source_tables = []
            sources = DcSourceSEO.objects.filter(site=obj_site).order_by('num')
            for source in sources:
                item_source = {'name_source': str(source.source)}
                it_src_month = []
                src_date = copy.deepcopy(calc_date)
                for _ in range(num_months):
                    s_date = f'01.{src_date.month}.{src_date.year}'
                    f_date = datetime.strptime(s_date, '%d.%m.%Y')
                    cash_source = DcCashSEO.objects.filter(val_date=f_date, num_site=obj_site.num, num_source=source.num).order_by('row')
                    c_row = {}
                    if src_date.month == cur_month and src_date.year == cur_year: forecast = True
                    else: forecast = False
                    for j in range(len(cash_source)):
                        val = cash_source[j].val
                        if forecast and j not in [4,]:
                            c_row[cash_source[j].row] = round(val * coef_forecast, 2)
                        else: c_row[cash_source[j].row] = val
                        # c_row[str(cash_source[j].row)] = cash_source[j].val
                    it_src_month.append(c_row)
                    src_date = src_date - timedelta(days=src_date.day)
                it_src_month.reverse()

                # Добавляем дополнительные столбцы "График" и "Сравн. мес"
                col_fabula = {}  # Шаблон новых колонок
                for i in range(1, len(row_source_names)+1): col_fabula[i] = ''
                s_date = f'01.{cur_month}.{cur_year}'
                f_date = datetime.strptime(s_date, '%d.%m.%Y')
                obj_cur_month = DcCashSEO.objects.filter(val_date=f_date, num_site=obj_site.num, num_source=source.num)
                col_gr = copy.deepcopy(col_fabula)  # словарь с ключами строк таблицы
                col_cm = copy.deepcopy(col_fabula)  # словарь с ключами строк таблицы
                col_ft = copy.deepcopy(col_fabula)  # словарь с ключами строк таблицы

                for key, _ in col_fabula.items():
                    gr = []
                    for i in range(num_months): 
                        val = it_src_month[i].get(key)
                        try: val = int(val)
                        except: val = 0
                        gr.append(val)
                    col_gr[key] = gr
                    # Для колонки "Сравн. мес" вычислим значение
                    col_cm[key] = 0
                    num_new = it_src_month[num_months-1].get(key)
                    num_old = it_src_month[num_months-2].get(key)
                    if num_new != None and num_old != None and num_old != 0:
                        cm = round((num_new / num_old - 1) * 100)
                        col_cm[key] = cm
                    try: col_ft[key] = obj_cur_month.get(row=key).val
                    except: col_ft[key] = ''
                it_src_month.append(col_gr)  # 13 колонка "График"
                it_src_month.append(col_cm)  # 14 колонка "Сравн. мес"
                it_src_month.append(col_ft)  # 14 колонка "месяц ФАКТ"
                
                item_source['months'] = it_src_month
                source_tables.append(item_source)

            item_sites['source_tables'] = source_tables
            
            data_sites.append(item_sites)

        out_data['data_sites'] = data_sites

        try:
            folder_path = 'seo_archive'
            filename = calc_date.strftime(f'{folder_path}/%d-%m-%Y.json')
            if not os.path.exists(folder_path): #Если пути не существует создаем его
                os.makedirs(folder_path)
            with open(filename, 'w', encoding='utf-8') as out_file:
                json.dump(out_data, out_file, ensure_ascii=False, cls=DecimalEncoder)
        except: raise Exception('Ошибка записи кэш2 в файл')
    except Exception as e:
        logger.error(f'Ошибка make_seo_page: try: {e}')

def make_csv_text(in_data, fname):
    filename = f'{fname}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response, lineterminator='\n', delimiter=';')

    try:
        ##### Основная таблица
        in_data['data_month'].pop(-2)
        in_data['data_month'].pop(-2)
        num_col = len(in_data['data_month'])
        in_data['data_month'].insert(0, '')

        writer.writerow(in_data['data_month'])
        in_data['data_0_table'].pop(-2)
        in_data['data_0_table'].pop(-2)
        num_row = len(row_0_names)
        tbl_0 = [[''] * num_col for i in range(num_row)]  # [num_row][num_col]
        # Собираем промежуточную таблицу
        for i in range(num_col):  # Проход по столбцам
            col = in_data['data_0_table'][i]
            if col:
                for j in range(num_row):  # Проход по строкам
                    val = col.get(str(j+1))
                    if val: tbl_0[j][i] = val
        # Собираем строки
        for j in range(len(tbl_0)):
            r_lst = [row_0_names[j],] + tbl_0[j]
            writer.writerow(r_lst)
        writer.writerow([])

        ##### Сводные таблицы сайтов
        for site in in_data['data_sites']:
            id_site = site.get('id')
            if id_site == 4: num_row_sites = len(row_site_names) + 1
            else: num_row_sites = len(row_site_names)
            url_site = site.get('url_site')
            writer.writerow([url_site,])
            writer.writerow(in_data['data_month'])
            site_table = site.get('site_table')  # {}
            site_table.pop(-2)
            site_table.pop(-2)

            tbl_site = [[''] * num_col for i in range(num_row_sites)]  # [num_row][num_col]
            # Собираем промежуточную таблицу
            for i in range(num_col):  # Проход по столбцам
                col = site_table[i]
                if col:
                    for j in range(num_row_sites):  # Проход по строкам
                        val = col.get(str(j+1))
                        if val: tbl_site[j][i] = val
            # Собираем строки
            len_tbl_site = len(tbl_site)  # количество строк в таблице
            for j in range(len_tbl_site):
                # Название строки
                if id_site == 4:  # Костыль !!! МГТС
                    if j == (len_tbl_site - 1): row_name = 'Сделки >50 МГТС'
                    else: row_name = row_site_names[j]
                    if j == (len_tbl_site - 2): row_name += f' {site.get("name_site")}'
                else:
                    row_name = row_site_names[j]
                    if j == (len_tbl_site - 1): row_name += f' {site.get("name_site")}'
                # Добавляем содержимое ячеек строки
                r_lst = [row_name,] + tbl_site[j]
                writer.writerow(r_lst)
            writer.writerow([])

            # Добавляем по каждому сайту таблицы с источниками
            writer.writerow([f'Источники {url_site}',])
            writer.writerow(in_data['data_month'])

            source_tables = site.get('source_tables')  # []
            for source in source_tables:
                if id_site == 4: num_row_source = len(row_source_names) + 1
                else: num_row_source = len(row_source_names)
                name_source = source.get('name_source')
                writer.writerow([name_source,])
                source_table = source.get('months')
                source_table.pop(-2)
                source_table.pop(-2)
                
                tbl_source = [[''] * num_col for i in range(num_row_source)]  # [num_row][num_col]
                # Собираем промежуточную таблицу
                for i in range(num_col):  # Проход по столбцам
                    col = source_table[i]
                    if col:
                        for j in range(num_row_source):  # Проход по строкам
                            val = col.get(str(j+1))
                            if val: tbl_source[j][i] = val
                # Собираем строки
                len_tbl_source = len(tbl_source)  # количество строк в таблице
                for j in range(len_tbl_source):
                    # Название строки
                    if id_site == 4:  # Костыль !!! МГТС
                        if j == (len_tbl_source - 1): row_name = 'Сделки >50 МГТС'
                        else: row_name = row_source_names[j]
                        if j == (len_tbl_source - 2): row_name += f' {site.get("name_site")}'
                    else:
                        row_name = row_source_names[j]
                        if j == (len_tbl_source - 1): row_name += f' {site.get("name_site")}'
                    # Добавляем содержимое ячеек строки
                    r_lst = [row_name,] + tbl_source[j]
                    writer.writerow(r_lst)
                writer.writerow([])

    except Exception as e:
        logger.error(f'Ошибка make_csv_text: try: {e}')
        print(e)

    return response
