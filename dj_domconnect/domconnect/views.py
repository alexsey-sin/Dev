# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q
# from django.core.paginator import Paginator
# from app.forms import NameForm, LizaPhraseForm, GermanPhraseForm, NdzPhraseForm, PzPhraseForm
from domconnect.models import DcCrmGlobVar, DcCrmLid
from domconnect.thread import thread_download_crm
from datetime import datetime
import calendar
from datetime import timedelta
from django.http import JsonResponse
import threading
from threading import Thread
import logging


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

    now = datetime.now()
    cur_day = now.day      # Номер текущего дня
    cur_month = now.month  # Номер текущего меяца
    cur_year = now.year    # Номер текущего года
    cnt_days_in_cur_month = calendar.monthrange(cur_year, cur_month)[1] # Количество дней в текущем месяце
    # Количество рабочих дней в текущем месяце
    cal = calendar.Calendar()
    working_days = len([x for x in cal.itermonthdays2(cur_year, cur_month) if x[0] !=0 and x[1] < 5])
    weekenddays = cnt_days_in_cur_month - working_days  # выходных дней

    # Названия ячеек cell_01_02_12   => №таблицы_№строки_№столбца
    # Все лиды за текущий месяц
    lids_all = DcCrmLid.objects.filter(create_date__year=cur_year, create_date__month=cur_month)
    count_lids_all = lids_all.count()
    if count_lids_all:
        lids_seo = lids_all.filter(crm_1592566018='SEO')
        lids_seo_conv = lids_seo.filter(crm_1493416385__gt=50, status_id__contains='CONVERTED')  # Подключаем (SOURCE)
        # (1) Лиды
        cell_01_01_12 = round((lids_seo.count() / cur_day) * cnt_days_in_cur_month)
        # (4) Лиды (все)
        cell_01_04_12 = round((count_lids_all / cur_day) * cnt_days_in_cur_month)
        # (5) Будн. дней 
        cell_01_05_12 = working_days
        # (6) Выходных дней 
        cell_01_06_12 = weekenddays
        # (7) Лиды с ТхВ 
        cell_01_07_12 = lids_seo.exclude(Q(crm_1571987728429='')|Q(crm_1571987728429=None)).count()  # Провайдеры ДК (длина больше 0)
        # (8) % лидов с ТхВ
        if cell_01_01_12:
            cell = round((cell_01_07_12 / cell_01_01_12) * 100, 2)
            cell_01_08_12 = f'{cell}%'
        else: cell_01_08_12 = ''
        # (9) Сделки >50
        cell_01_09_12 = round((lids_seo_conv.count() / cur_day) * cnt_days_in_cur_month)
        # (10) %Лид=>Сд. >50
        cell = round((cell_01_09_12 / cell_01_01_12) * 100, 2)
        cell_01_10_12 = f'{cell}%'
        # (12) Сделки >50 (все)
        cell = lids_all.filter(crm_1493416385__gt=50, status_id__contains='CONVERTED').count()
        cell_01_12_12 = round((cell / cur_day) * cnt_days_in_cur_month)
        # (13) Сделки 80
        # ('Билайн', 'МТС [кроме МСК и МО]', 'Ростелеком [кроме МСК]', 'МГТС [МСК и МО]')
        cell = lids_seo_conv.filter(crm_1493413514__in=['OTHER', '2', '3', '11']).count()  # Провайдер (INDUSTRY)
        cell_01_13_12 = round((cell / cur_day) * cnt_days_in_cur_month)
        # (14) Сд. приоритет (БИ и МТС ФЛ)
        # ('Билайн', 'МТС [кроме МСК и МО]')
        cell = lids_seo_conv.filter(crm_1493413514__in=['OTHER', '2']).count()  # Провайдер (INDUSTRY)
        cell_01_14_12 = round((cell / cur_day) * cnt_days_in_cur_month)
        # (15) Доля сделок ПРИОР от сд. >50
        cell = round((cell_01_14_12 / cell_01_09_12) * 100, 2)
        cell_01_15_12 = f'{cell}%'
        # (16) Ср. лид/день (будн.)
        cell = lids_seo.filter(create_date__week_day__range=(2,6)).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_01_16_12 = round(cell / working_days)
        # (17) Ср. лид/день (вых.)
        cell = lids_seo.filter(create_date__week_day__in=(1,7)).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_01_17_12 = round(cell / weekenddays)
        # (18) ТП SEO
        # ('ТП_пр', 'ТП_нраб', 'ТП_моб') https://docs.google.com/spreadsheets/d/1fPFxlhAje5V_kdlSHpLytBbgE6SiBaWtfsrFjw1XYv8/edit#gid=1803529933
        cell_tp_seo = lids_seo.filter(status_id__in=['1', '16', '21', '31', '32', '33']).count()  # Статус (STATUS)
        cell_01_18_12 = round((cell_tp_seo / cur_day) * cnt_days_in_cur_month)
        # (19) Расход ТП
        cell_01_19_12 = round(cell_tp_seo * 3.4)
        # (20) % ТП
        cell = round((cell_tp_seo / cell_01_01_12) * 100, 2)
        cell_01_20_12 = f'{cell}%'
        # (21) Подключки
        # ????????????????
        # (22) ТП IVR Лиза  (ТП_IVR)
        cell_tp_ivr_seo = lids_seo.filter(status_id='52').count()  # Статус (STATUS)
        cell_01_22_12 = round((cell_tp_ivr_seo / cur_day) * cnt_days_in_cur_month)
        # (23) % ТП IVR 
        cell = round((cell_tp_ivr_seo / cell_01_01_12) * 100, 2)
        cell_01_23_12 = f'{cell}%'
        # (2) Реальные лиды (без ТП)
        if cell_01_01_12:
            cell_01_02_12 = cell_01_01_12 - cell_01_18_12 - cell_01_22_12
        else: cell_01_02_12 = ''
        # (3) % реальных лидов
        if cell_01_02_12:
            cell = round((cell_01_02_12 / cell_01_01_12) * 100, 2)
            cell_01_03_12 = f'{cell}%'
            # (11) Конва реал. лид => сделка >50
            cell = round((cell_01_09_12 / cell_01_02_12) * 100, 2)
            cell_01_11_12 = f'{cell}%'
        else:
            cell_01_03_12 = ''
            cell_01_11_12 = ''
        # (24) % ТП Лизы от всего ТП
        cell = round((cell_01_22_12 / (cell_01_22_12 + cell_01_18_12)) * 100, 2)
        cell_01_24_12 = f'{cell}%'

        # (25) Понедельник
        cell = lids_all.filter(create_date__week_day=2).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_01_25_12 = round((cell / cur_day) * cnt_days_in_cur_month)
        # (26) Вторник
        cell = lids_all.filter(create_date__week_day=3).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_01_26_12 = round((cell / cur_day) * cnt_days_in_cur_month)
        # (27) Среда
        cell = lids_all.filter(create_date__week_day=4).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_01_27_12 = round((cell / cur_day) * cnt_days_in_cur_month)
        # (28) Четверг
        cell = lids_all.filter(create_date__week_day=5).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_01_28_12 = round((cell / cur_day) * cnt_days_in_cur_month)
        # (29) Пятница
        cell = lids_all.filter(create_date__week_day=6).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_01_29_12 = round((cell / cur_day) * cnt_days_in_cur_month)
        # (30) Суббота
        cell = lids_all.filter(create_date__week_day=7).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_01_30_12 = round((cell / cur_day) * cnt_days_in_cur_month)
        # (31) Воскресенье
        cell = lids_all.filter(create_date__week_day=1).count() # Дни недели пронумерованы от 1(воскресение) до 7(суббота)
        cell_01_31_12 = round((cell / cur_day) * cnt_days_in_cur_month)




        print('cell_01_01_12', cell_01_01_12)
        print('cell_01_02_12', cell_01_02_12)
        print('cell_01_03_12', cell_01_03_12)
        print('cell_01_04_12', cell_01_04_12)
        print('cell_01_05_12', cell_01_05_12)
        print('cell_01_06_12', cell_01_06_12)
        print('cell_01_07_12', cell_01_07_12)
        print('cell_01_08_12', cell_01_08_12)
        print('cell_01_09_12', cell_01_09_12)
        print('cell_01_10_12', cell_01_10_12)
        print('cell_01_11_12', cell_01_11_12)
        print('cell_01_12_12', cell_01_12_12)
        print('cell_01_13_12', cell_01_13_12)
        print('cell_01_14_12', cell_01_14_12)
        print('cell_01_15_12', cell_01_15_12)
        print('cell_01_16_12', cell_01_16_12)
        print('cell_01_17_12', cell_01_17_12)
        print('cell_01_18_12', cell_01_18_12)
        print('cell_01_19_12', cell_01_19_12)
        print('cell_01_20_12', cell_01_20_12)

        print('cell_01_22_12', cell_01_22_12)
        print('cell_01_23_12', cell_01_23_12)
        print('cell_01_24_12', cell_01_24_12)
        print('cell_01_25_12', cell_01_25_12)
        print('cell_01_26_12', cell_01_26_12)
        print('cell_01_27_12', cell_01_27_12)
        print('cell_01_28_12', cell_01_28_12)
        print('cell_01_29_12', cell_01_29_12)
        print('cell_01_30_12', cell_01_30_12)
        print('cell_01_31_12', cell_01_31_12)
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
        gvar_go.save(update_fields=['val_bool'])

    is_start = request.GET.get('start')
    if is_start and not is_run:
        # Разрешим загрузку в глобальной переменной
        gvar_go, _ = DcCrmGlobVar.objects.get_or_create(key='go_download_crm')
        gvar_go.val_bool = True
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

