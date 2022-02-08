# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q
# from django.core.paginator import Paginator
# from app.forms import NameForm, LizaPhraseForm, GermanPhraseForm, NdzPhraseForm, PzPhraseForm
from domconnect.models import DcCrmGlobVar, DcCrmLid, DcCashSEO, DcSiteSEO, DcSourceSEO
from domconnect.download_lids import run_download_crm
from datetime import datetime, timedelta
from django.http import JsonResponse
import threading
from threading import Thread
import logging, json, copy


logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    format='%(asctime)s:%(name)s:%(message)s'
)
# log = logging.getLogger(__name__)  # запускать в функциях
# log.info('So should this')
# # # # log.debug('This message should go to the log file')
# # # # log.warning('And this, too')


@login_required(login_url='/login/')
def index(request):  # Статистика SEO
    # log = logging.getLogger(__name__)
    # log.info('Start load page')
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}

    label_seo = ''
    # Посмотрим состояние загрузки в глобальной переменной
    gvar_go, _ = DcCrmGlobVar.objects.get_or_create(key='go_download_crm')
    if gvar_go.val_bool: label_seo = 'Идет загрузка лидов ...'
    else: 
        if gvar_go.val_datetime: last_datetime = gvar_go.val_datetime.strftime("%d.%m.%Y %H:%M:%S")
        else: last_datetime = 'Нет данных'
        label_seo = f'Последнее обновление: {last_datetime}'
    context['label_seo'] = label_seo

    # Собираем строку заголовков и основную таблицу
    str_month = ['', 'Янв.', 'Фев.', 'Мар.', 'Апр.', 'Май', 'Июн.', 'Июл.', 'Авг.', 'Сен.', 'Окт.', 'Ноя.', 'Дек.']
    col_date = datetime.today()
    data_month = []
    data_0_table = []
    for _ in range(12):
        s_date = f'01.{col_date.month}.{col_date.year}'
        f_date = datetime.strptime(s_date, '%d.%m.%Y')
        c_data = DcCashSEO.objects.filter(val_date=f_date, num_site=0, num_source=0).order_by('row')
        data_month.append({'head': f'{str_month[col_date.month]} {col_date.year}'})
        c_row = {}
        for j in range(len(c_data)): c_row[c_data[j].row] = c_data[j].val
        data_0_table.append(c_row)
        col_date = col_date - timedelta(days=col_date.day)
    data_month.reverse()
    data_0_table.reverse()

    # Добавляем дополнительные столбцы "График" и "Сравн. мес"
    col_fabula = data_0_table[-1]  # В качестве шаблона новых колонок берем последнюю (свежий месяц)
    if len(col_fabula):
        col_gr = copy.deepcopy(col_fabula)  # словарь с ключами строк таблицы
        col_cm = copy.deepcopy(col_fabula)  # словарь с ключами строк таблицы

        for key, _ in col_fabula.items():
            # gr = []
            gr = 0
            for i in range(12): 
                if len(data_0_table[i]):
                    # gr.append(site_table[i][key])
                    gr = 0
            col_gr[key] = gr
            # Для колонки "Сравн. мес" вычислим значение
            num_new = data_0_table[11].get(key)
            num_old = data_0_table[10].get(key)
            if num_new and num_old:
                cm = round((num_new / num_old - 1) * 100)
                col_cm[key] = cm
        data_0_table.append(col_gr)  # 13 колонка "График"
        data_0_table.append(col_cm)  # 14 колонка "Сравн. мес"

    context['data_month'] = data_month
    context['data_0_table'] = data_0_table

    # with open('data_0_table.json', 'w', encoding='utf-8') as out_file:
    #     json.dump(data_0_table, out_file, ensure_ascii=False, indent=4)

    # Собираем таблицы сайтов с источниками
    data_sites = []
    objs_site = DcSiteSEO.objects.all().order_by('num')
    for obj_site in objs_site:
        item_sites = {'id': obj_site.num, 'name_site': obj_site.site}
        
        # Таблицы сайта по месяцам
        site_table = []  # Список словарей по месяцам сводной таблицы сайта
        col_date = datetime.today()
        for _ in range(12):
            s_date = f'01.{col_date.month}.{col_date.year}'
            f_date = datetime.strptime(s_date, '%d.%m.%Y')
            c_data = DcCashSEO.objects.filter(val_date=f_date, num_site=obj_site.num, num_source=0).order_by('row')
            c_row = {}
            for j in range(len(c_data)): c_row[str(c_data[j].row)] = c_data[j].val
            site_table.append(c_row)
            col_date = col_date - timedelta(days=col_date.day)
        site_table.reverse()

        # Добавляем дополнительные столбцы "График" и "Сравн. мес"
        col_fabula = site_table[-1]  # В качестве шаблона новых колонок берем последнюю (свежий месяц)
        if len(col_fabula):
            col_gr = copy.deepcopy(col_fabula)  # словарь с ключами строк таблицы
            col_cm = copy.deepcopy(col_fabula)  # словарь с ключами строк таблицы

            for key, _ in col_fabula.items():
                # gr = []
                gr = 0
                for i in range(12): 
                    if len(site_table[i]):
                        # gr.append(site_table[i][key])
                        gr = 0
                col_gr[key] = gr
                # Для колонки "Сравн. мес" вычислим значение
                num_new = site_table[11].get(key)
                num_old = site_table[10].get(key)
                if num_new and num_old:
                    cm = round((num_new / num_old - 1) * 100)
                    col_cm[key] = cm
            site_table.append(col_gr)  # 13 колонка "График"
            site_table.append(col_cm)  # 14 колонка "Сравн. мес"
        item_sites['site_table'] = site_table
        
        # Проход по источникам сайта
        source_tables = []
        sources = DcSourceSEO.objects.filter(site=obj_site).order_by('num')
        for source in sources:
            item_source = {'name_source': source.source}
            it_src_month = []
            src_date = datetime.today()
            for _ in range(12):
                s_date = f'01.{src_date.month}.{src_date.year}'
                f_date = datetime.strptime(s_date, '%d.%m.%Y')
                cash_source = DcCashSEO.objects.filter(val_date=f_date, num_site=obj_site.num, num_source=source.num).order_by('row')
                c_row = {}
                for j in range(len(cash_source)): c_row[str(cash_source[j].row)] = cash_source[j].val
                it_src_month.append(c_row)
                src_date = src_date - timedelta(days=src_date.day)
            it_src_month.reverse()
            
            # Добавляем дополнительные столбцы "График" и "Сравн. мес"
            col_fabula = it_src_month[-1]  # В качестве шаблона новых колонок берем последнюю (свежий месяц)
            if len(col_fabula):
                col_gr = copy.deepcopy(col_fabula)  # словарь с ключами строк таблицы
                col_cm = copy.deepcopy(col_fabula)  # словарь с ключами строк таблицы

                for key, _ in col_fabula.items():
                    # gr = []
                    gr = 0
                    for i in range(12): 
                        if len(it_src_month[i]):
                            # gr.append(site_table[i][key])
                            gr = 0
                    col_gr[key] = gr
                    # Для колонки "Сравн. мес" вычислим значение
                    num_new = it_src_month[11].get(key)
                    num_old = it_src_month[10].get(key)
                    if num_new and num_old:
                        cm = round((num_new / num_old - 1) * 100)
                        col_cm[key] = cm
                it_src_month.append(col_gr)  # 13 колонка "График"
                it_src_month.append(col_cm)  # 14 колонка "Сравн. мес"
            
            item_source['months'] = it_src_month
            source_tables.append(item_source)

        item_sites['source_tables'] = source_tables
        
        data_sites.append(item_sites)

    context['data_sites'] = data_sites

    # with open('data_sites.json', 'w', encoding='utf-8') as out_file:
    #     json.dump(data_sites, out_file, ensure_ascii=False, indent=4)

    context['segment'] = 'statseo'
    # log.info('Stop load page')
    return render(request, 'domconnect/statseo.html', context)
    
@login_required(login_url='/login/')
def dataCrm(request):  # Данные SEO
    log = logging.getLogger(__name__)  # запустили логгирование

    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}

    # calculateSEO()
    # print('cnt_lids_all', cnt_lids_all)
    # log.info(f'cnt_lids_all: {cnt_lids_all}')
    # log.info(f'cnt_lids_seo: {cnt_lids_seo}')


    context['segment'] = 'datacrm'
    return render(request, 'domconnect/datacrm.html', context)
    
@login_required(login_url='/login/')
def dataAjax(request):
    thread_name = 'DownLoadLidsFromCRM'
    if not request.GET: return JsonResponse({})

    str_from_modify = ''
    last_modify_lid = DcCrmLid.objects.order_by('modify_date').last()
    if last_modify_lid:
        from_modify = last_modify_lid.modify_date
        if type(from_modify) == datetime:
            from_modify = from_modify - timedelta(seconds=1)
            str_from_modify = from_modify.strftime('%Y-%m-%dT%H:%M:%S')

    # Проверим идет ли загрузка
    is_run = False
    for thread in threading.enumerate():
        if thread.getName() == thread_name: is_run = True; break
    response = {'is_run': is_run}
    
    # Посмотрим нужны ли данные по загрузке
    get_state = request.GET.get('get_state')
    if get_state:
        gvar_cur, _ = DcCrmGlobVar.objects.get_or_create(key='cur_num_download_crm')
        gvar_tot, _ = DcCrmGlobVar.objects.get_or_create(key='tot_num_download_crm')
        response['val_current'] = gvar_cur.val_int
        response['val_total'] = gvar_tot.val_int
        
    is_stop = request.GET.get('stop')
    if is_stop:
        gvar_go, _ = DcCrmGlobVar.objects.get_or_create(key='go_download_crm')
        gvar_go.val_bool = False
        gvar_go.val_datetime = datetime.today()
        gvar_go.save(update_fields=['val_bool'])

    is_start = request.GET.get('start')
    if is_start and not is_run:
        # Разрешим загрузку в глобальной переменной
        gvar_go, _ = DcCrmGlobVar.objects.get_or_create(key='go_download_crm')
        gvar_go.val_bool = True
        gvar_go.val_datetime = datetime.today()
        gvar_go.descriptions = 'Загрузка запущена'
        gvar_go.save(update_fields=['val_bool'])

        # Обнулим глоб. переменную текущей позиции
        gvar_cur, _ = DcCrmGlobVar.objects.get_or_create(key='cur_num_download_crm')
        gvar_cur.val_int = 0
        gvar_cur.save(update_fields=['val_int'])

        # Запустим поток загрузки
        th = Thread(target=run_download_crm, name=thread_name, args=(str_from_modify, ))
        th.start()
        response['is_run'] = True
    return JsonResponse(response)


################################################################################################
# API
@login_required(login_url='/login/')
def deleteAllLids(request):  # Удаление всех лидов
    count = DcCrmLid.objects.all().count()
    DcCrmLid.objects.all().delete()

    context = {
        'result': 'Ok',
        'message': f'Записи лидов удалены. ({count})',
        'result_style': 'success',
    }
    return render(request, 'domconnect/show_mess_and_redirect.html', context)

@login_required(login_url='/login/')
def deleteCash(request):  # Удаление данных из таблицы кэш
    count = DcCashSEO.objects.all().count()
    DcCashSEO.objects.all().delete()

    context = {
        'result': 'Ok',
        'message': f'Записи кэш удалены. ({count})',
        'result_style': 'success',
    }
    return render(request, 'domconnect/show_mess_and_redirect.html', context)

@login_required(login_url='/login/')
def upgradeSiteSource(request):  # Удаление и загрузка данных таблиц Site и Source из файла
    log = logging.getLogger(__name__)  # запустили логгирование
    err = ''
    try:
        with open('SiteSource.json', 'r', encoding='utf-8') as file:
            js_data = json.load(file)
        if not js_data or len(js_data) == 0: raise Exception('Нет данных для обновления.')
        DcSiteSEO.objects.all().delete()
        DcSourceSEO.objects.all().delete()
        # Перебираем сайты с вложенными источниками и заносим в базу
        for dct_site in js_data:
            num =  dct_site.get('num')
            site = dct_site.get('site')
            provider = dct_site.get('provider')
            sources = dct_site.get('sources')
            if not num or not site or not provider or not sources:
                raise Exception('Ошибка данных сайта для обновления.')
            obj_site, _ = DcSiteSEO.objects.get_or_create(num=num, site=site, provider=provider)
            if not obj_site: raise Exception('Ошибка сохранения сайта.')
            for rec in sources:
                num = rec.get('num')
                source = rec.get('source')
                if not num or not source: raise Exception('Ошибка данных источника для обновления.')
                obj_source, _ = DcSourceSEO.objects.get_or_create(num=num, source=source, site=obj_site)
                if not obj_source: raise Exception('Ошибка сохранения источника.')
        
    except Exception as e:
        err = f'Ошибка upgradeSiteSource: try: {e}'
        log.info(err)
    if err:
        context = {
            'result': 'Error',
            'message': f'{err}',
            'result_style': 'danger',
        }
    else:
        context = {
            'result': 'Ok',
            'message': 'Записи Site Source обновлены.',
            'result_style': 'success',
        }
    return render(request, 'domconnect/show_mess_and_redirect.html', context)

