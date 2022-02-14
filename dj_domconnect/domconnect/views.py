# -*- encoding: utf-8 -*-
from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q
# from django.core.paginator import Paginator
# from app.forms import NameForm, LizaPhraseForm, GermanPhraseForm, NdzPhraseForm, PzPhraseForm
from domconnect.models import DcCrmGlobVar, DcCrmLid, DcCashSEO, DcSiteSEO, DcSourceSEO, DcCrmDeal
from datetime import datetime, timedelta
from django.http import JsonResponse
from domconnect.lib_seo import run_upgrade_seo, make_seo_page, make_csv_text
from threading import Thread
import os, logging, json, threading, calendar


logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    format='%(asctime)s:%(name)s:%(message)s'
    # log.info('So should this')
    # # # # log.debug('This message should go to the log file')
    # # # # log.warning('And this, too')
)
loger = logging.getLogger(__name__)  # запустили логгирование


@login_required(login_url='/login/')
def index(request):  # Статистика SEO
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}
    now_date = datetime.today()

    label_seo = ''
    # Посмотрим состояние загрузки в глобальной переменной
    gvar_go, _ = DcCrmGlobVar.objects.get_or_create(key='go_upgrade_seo')
    if gvar_go.val_bool == True: label_seo = 'Идет Обновление данных ...'
    else: 
        if gvar_go.val_datetime: last_datetime = gvar_go.val_datetime.strftime("%d.%m.%Y %H:%M:%S")
        else: last_datetime = 'Нет данных'
        label_seo = f'Последнее обновление: {last_datetime}'
    context['label_seo'] = label_seo

    # page_context = make_seo_page()
    page_context = {}
    try:
        with open('seo_page.json', 'r', encoding='utf-8') as file:
            page_context = json.load(file)
    except Exception as e:
        context['label_seo'] = 'Ошибка загрузки данных из кэш.'
        loger.error(str(e))
    # Переносим полученные данные
    if page_context:
        context['data_month'] = page_context['data_month']
        context['data_0_table'] = page_context['data_0_table']
        context['data_sites'] = page_context['data_sites'] 

    context['segment'] = 'statseo'
    context['color_forecast'] = 'style="background: #FFFFE0;"'

    if request.method == 'POST':
        get_seo = request.POST.get('get_seo')
        if get_seo and bool(get_seo) == True:
            filename = now_date.strftime('%d-%m-%Y.csv')
            content = make_csv_text(page_context)
            response = HttpResponse(content, content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response        
    
    
    return render(request, 'domconnect/statseo.html', context)
    
@login_required(login_url='/login/')
def dataCrm(request):  # Данные SEO

    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}


    context['segment'] = 'datacrm'
    return render(request, 'domconnect/datacrm.html', context)
    
@login_required(login_url='/login/')
def dataAjax(request):
    # thread_name = 'DownLoadLidsFromCRM'
    # if not request.GET: return JsonResponse({})

    # # Проверим идет ли загрузка
    # is_run = False
    # for thread in threading.enumerate():
    #     if thread.getName() == thread_name: is_run = True; break
    # response = {'is_run': is_run}
    
    # # Посмотрим нужны ли данные по загрузке
    # get_state = request.GET.get('get_state')
    # if get_state:
    #     gvar_cur, _ = DcCrmGlobVar.objects.get_or_create(key='cur_num_download_crm')
    #     gvar_tot, _ = DcCrmGlobVar.objects.get_or_create(key='tot_num_download_crm')
    #     response['val_current'] = gvar_cur.val_int
    #     response['val_total'] = gvar_tot.val_int
        
    # is_stop = request.GET.get('stop')
    # if is_stop:
    #     gvar_go, _ = DcCrmGlobVar.objects.get_or_create(key='go_upgrade_seo')
    #     gvar_go.val_bool = False
    #     gvar_go.val_datetime = datetime.today()
    #     gvar_go.save(update_fields=['val_bool'])

    # is_start = request.GET.get('start')
    # if is_start and not is_run:
    #     # Разрешим загрузку в глобальной переменной
    #     gvar_go, _ = DcCrmGlobVar.objects.get_or_create(key='go_upgrade_seo')
    #     gvar_go.val_bool = True
    #     gvar_go.val_datetime = datetime.today()
    #     gvar_go.descriptions = 'Загрузка запущена'
    #     gvar_go.save(update_fields=['val_bool'])

    #     # Обнулим глоб. переменную текущей позиции
    #     gvar_cur, _ = DcCrmGlobVar.objects.get_or_create(key='cur_num_download_crm')
    #     gvar_cur.val_int = 0
    #     gvar_cur.save(update_fields=['val_int'])

    #     # Запустим поток загрузки
    #     th = Thread(target=run_download_crm, name=thread_name)
    #     th.start()
    #     response['is_run'] = True
    # return JsonResponse(response)
    pass

# @login_required(login_url='/login/')
# def getSeoCSV(request):
#     if not request.GET: return JsonResponse({})
#     # Посмотрим нужны ли данные в csv
#     get_seo = request.GET.get('get_seo')
#     if get_seo:
#         print('getSeoCSV')
#         out_data = {'names': []}
#         filename = 'fff.csv'
#         data = json.dumps(out_data)
#         response = FileResponse(data, 'rb')
#         response["Content-Type"] = 'application/json; charset=utf-8'
#         response['Content-Disposition'] = f'attachment; filename={filename}'
#         response['X-Sendfile'] = filename
#         return response
#     else:
#         return JsonResponse({})


################################################################################################
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

    if err:
        loger.error(err)
        context = {
            'result': 'Error',
            'message': f'{err}',
            'result_style': 'danger',
        }
    else:
        loger.info('Site Source Service обновлены.')
        context = {
            'result': 'Ok',
            'message': 'Записи Site Source обновлены.',
            'result_style': 'success',
        }
    return render(request, 'domconnect/show_mess_and_redirect.html', context)

@login_required(login_url='/login/')
def deleteAllDeals(request):  # Удаление всех сделок
    count = DcCrmDeal.objects.all().count()
    DcCrmDeal.objects.all().delete()

    context = {
        'result': 'Ok',
        'message': f'Записи сделок удалены. ({count})',
        'result_style': 'success',
    }
    return render(request, 'domconnect/show_mess_and_redirect.html', context)

@login_required(login_url='/login/')
def upgradeSeo(request):
    thread_name = 'ThreadUpgradeSeo'
    is_run = False
    for thread in threading.enumerate():
        if thread.getName() == thread_name: is_run = True; break

    if is_run:
        context = {
            'result': 'Ok',
            'message': f'Поток обновления и расчета уже идет.',
            'result_style': 'info',
        }
    else:
        # Запустим поток загрузки
        th = Thread(target=run_upgrade_seo, name=thread_name, args=())
        th.start()
        context = {
            'result': 'Ok',
            'message': f'Поток обновления и расчета запущен.',
            'result_style': 'success',
        }

    return render(request, 'domconnect/show_mess_and_redirect.html', context)
