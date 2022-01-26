# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q
# from django.core.paginator import Paginator
# from app.forms import NameForm, LizaPhraseForm, GermanPhraseForm, NdzPhraseForm, PzPhraseForm
from domconnect.models import DcCrmGlobVar, DcCrmLid, DcCashSEO
from domconnect.thread import thread_download_crm, calculateSEO
from datetime import datetime
import calendar
from datetime import timedelta
from django.http import JsonResponse
import threading
from threading import Thread
import logging
import json


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
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}

    label_seo = ''
    # Посмотрим состояние загрузки в глобальной переменной
    gvar_go, _ = DcCrmGlobVar.objects.get_or_create(key='go_download_crm')
    if gvar_go.val_bool: label_seo = 'Идет загрузка лидов ...'
    else: label_seo = f'Последнее обновление: {gvar_go.val_datetime.strftime("%d.%m.%Y %H:%M:%S")}'
    context['label_seo'] = label_seo

    str_month = ['', 'Янв.', 'Фев.', 'Мар.', 'Апр.', 'Май', 'Июн.', 'Июл.', 'Авг.', 'Сен.', 'Окт.', 'Ноя.', 'Дек.']
    col_date = datetime.today()
    col_month = []
    col_rercent = [2, 7, 9, 10, 14, 22, 23]  # Номера строк с процентами
    col_many = [18, ]  # Номера строк с деньгами
    for i in range(12):
        s_date = f'01.{col_date.month}.{col_date.year}'
        print(s_date)
        f_date = datetime.strptime(s_date, '%d.%m.%Y')
        c_data = DcCashSEO.objects.filter(val_date=f_date, table=1).order_by('row')
        c_row = {'head': f'{str_month[col_date.month]} {col_date.year}'}
        for j in range(len(c_data)):
            if j in col_rercent: c_row[str(c_data[j].row)] = f'{round(c_data[j].val,2)}%'
            elif j in col_many: c_row[str(c_data[j].row)] = f'{round(c_data[j].val)}р.'
            else: c_row[str(c_data[j].row)] = str(round(c_data[j].val))
            # print(r_data.row, r_data.val)
        # print(c_row)
        col_month.append(c_row)
        # break
    
        col_date = col_date - timedelta(days=col_date.day)
    col_month.reverse()
    
    with open('col_month.json', 'w', encoding='utf-8') as out_file:
        json.dump(col_month, out_file, ensure_ascii=False, indent=4)

    # print(col_month)
    context['col_month'] = col_month










    context['segment'] = 'statseo'
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
        th = Thread(target=thread_download_crm, name=thread_name, args=(str_from_modify, ))
        th.start()
        response['is_run'] = True
    return JsonResponse(response)

@login_required(login_url='/login/')
def deleteAllLids(request):
    count = DcCrmLid.objects.all().count()
    DcCrmLid.objects.all().delete()

    context = {
        'result': 'Ok',
        'message': f'Записи удалены. ({count})',
        'result_style': 'success',
    }
    return render(request, 'domconnect/show_mess_and_redirect.html', context)

