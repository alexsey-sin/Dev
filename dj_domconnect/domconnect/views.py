# -*- encoding: utf-8 -*-
from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q, Max
# from django.core.paginator import Paginator
# from app.forms import NameForm, LizaPhraseForm, GermanPhraseForm, NdzPhraseForm, PzPhraseForm
from domconnect.models import DcCrmGlobVar, DcCrmLid, DcCashSEO, DcSiteSEO, DcSourceSEO, DcCrmDeal
from domconnect.models import DcCatalogProviderSEO, DcCatalogSourceSEO
from datetime import datetime, timedelta
from django.http import JsonResponse
from domconnect.lib_seo import get_key_crm, run_upgrade_seo, make_csv_text, dounload_catalog
from domconnect.forms import DcSiteSEOForm
from threading import Thread
import os, logging, json, threading, requests
from pathlib import Path
from django import forms


logging.basicConfig(
    level=logging.INFO,     # DEBUG, INFO, WARNING, ERROR и CRITICAL По возрастанию
    filename='main.log',
    format='%(asctime)s:%(name)s:%(message)s'
    # log.info('So should this')
    # # # # log.debug('This message should go to the log file')
    # # # # log.warning('And this, too')
)
logger = logging.getLogger(__name__)  # запустили логгирование


@login_required(login_url='/login/')
def index(request):  # Статистика SEO
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}

    seo_archive_folder_path = 'seo_archive'
    label_seo = ''
    # Посмотрим состояние загрузки в глобальной переменной
    gvar_go, _ = DcCrmGlobVar.objects.get_or_create(key='go_upgrade_seo')
    if gvar_go.val_bool == True: label_seo = 'Идет Обновление данных ...'
    else: 
        if gvar_go.val_datetime: last_datetime = gvar_go.val_datetime.strftime("%d.%m.%Y %H:%M:%S")
        else: last_datetime = 'Нет данных'
        label_seo = f'Последнее обновление: {last_datetime}'
    context['label_seo'] = label_seo

    # Берем последний сохраненный архив
    page_context = {}
    # try:
    #     # Возьмем список всех файлов в папке
    list_archives = os.listdir(seo_archive_folder_path)
    if list_archives:
        # Отсортируем по дате создания
        list_archives_sort = sorted(list_archives, key=lambda x: os.path.getctime(os.path.join(seo_archive_folder_path, x)), reverse=True)
        # Соберем без расширения
        list_namefiles = [s.split('.js')[0] for s in list_archives_sort]
        context['list_archives'] = list_namefiles

        with open(f'{seo_archive_folder_path}/{list_archives_sort[0]}', 'r', encoding='utf-8') as file:
            page_context = json.load(file)
    # except Exception as e:
    #     context['label_seo'] = 'Ошибка загрузки данных из кэш.'
    #     logger.error(str(e))
    
    # Переносим полученные данные
    if page_context:
        context['data_month'] = page_context['data_month']
        context['cnt_month'] = len(page_context['data_month']) - 3  # количество месяцев вывода
        context['col_grafic'] = context['cnt_month'] + 1  # Номер колонки "График"
        context['col_compare'] = context['cnt_month'] + 2  # Номер колонки "Сравн. мес"
        context['data_0_table'] = page_context['data_0_table']
        context['data_sites'] = page_context['data_sites'] 

    context['segment'] = 'statseo'
    context['color_forecast'] = 'style="background: #FFFFE0;"'

    if request.method == 'POST':
        get_seo = request.POST.get('get_seo')
        if get_seo:
            arch_filename = f'{seo_archive_folder_path}/{get_seo}.json'
            try:
                with open(arch_filename, 'r', encoding='utf-8') as file:
                    page_context = json.load(file)
                response = make_csv_text(page_context, get_seo)
                return response 
            except Exception as e:
                context['label_seo'] = 'Ошибка загрузки файла.'
                logger.error(str(e))
    
    return render(request, 'domconnect/statseo.html', context)


@login_required(login_url='/login/')
def sites(request):  #
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name, 'segment': 'sites'}

    if request.method == 'POST':
        id_delete = request.POST.get('delete', None)
        id_change = request.POST.get('id_change', None)
        direct = request.POST.get('direct', None)

        if id_delete:
            try:
                _ = DcSiteSEO.objects.get(id=id_delete).delete()
                objs_site = DcSiteSEO.objects.order_by('num')
                for i in range(len(objs_site)):
                    objs_site[i].num = i
                    objs_site[i].save()
            except Exception as e: context['error_mess'] = f'Ошибка удаления сайта: {e}.'
        if id_change and direct:
            try:
                old_pos = DcSiteSEO.objects.get(id=id_change).num
                max_pos = DcSiteSEO.objects.aggregate(Max('num'))['num__max']
                rec = True
                if (direct == 'change_down' and old_pos == max_pos) or (direct == 'change_up' and old_pos == 0): rec = False
                if rec:
                    objs_site = DcSiteSEO.objects.order_by('num')
                    for i in range(len(objs_site)):
                        if direct == 'change_up':
                            if i == old_pos-1: objs_site[i].num = i+1
                            if i == old_pos: objs_site[i].num = i-1
                        if direct == 'change_down':
                            if i == old_pos+1: objs_site[i].num = i-1
                            if i == old_pos: objs_site[i].num = i+1
                        objs_site[i].save()
            except Exception as e: context['error_mess'] = f'Ошибка перемещения сайта: {e}.'

    tmp_data = DcSiteSEO.objects.order_by('num').values()
    data = [row for row in tmp_data]
    for row in data:
        row['provider'] = DcCatalogProviderSEO.objects.get(id=row['provider_id'])

    context['data'] = data

    return render(request, 'domconnect/sites.html', context)


@login_required(login_url='/login/')
def site_edit(request, id_site):
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name, 'segment': 'site_edit'}

    if request.method == 'POST':
        id_edit_site = request.POST.get('edit_site', None)
        new_source = request.POST.get('new_source', None)
        delete_source = request.POST.get('delete_source', None)
        id_change = request.POST.get('id_change', None)
        direct = request.POST.get('direct', None)

        if id_edit_site:
            try:
                if int(id_edit_site) > 0:
                    objs_site = DcSiteSEO.objects.filter(id=id_edit_site)
                    if len(objs_site) != 1: raise Exception('Нет сайта')
                    obj_site = objs_site[0]
                else:
                    obj_site = DcSiteSEO()
                
                obj_site.num = request.POST.get('num')
                obj_site.site = request.POST.get('site')
                obj_site.name = request.POST.get('name')
                obj_site.provider = DcCatalogProviderSEO.objects.get(name=request.POST.get('provider'))
                obj_site.save()
                return redirect('domconnect:sites')
            except Exception as e: context['error_mess'] = f'Ошибка сохранения сайта {e}.'
        if new_source:
            try:
                if int(id_site) == 0: raise Exception('Сначала надо сохранить сайт.')
                objs_site = DcSiteSEO.objects.filter(id=id_site)
                if len(objs_site) != 1: raise Exception(f'Сайт {id_site} не найден.')
                obj_site = objs_site[0]
                objs_source = DcCatalogSourceSEO.objects.filter(name=new_source)
                if len(objs_source) != 1: raise Exception(f'Источник {new_source} не найден.')
                obj_source = objs_source[0]
                try: next_num = DcSourceSEO.objects.filter(site=id_site).aggregate(Max('num'))['num__max'] + 1
                except: next_num = 1
                _, create = DcSourceSEO.objects.get_or_create(site=obj_site, source=obj_source, num=next_num)
                if create != True: raise Exception(f'Источник {new_source} не сохранен.')
            except Exception as e: context['error_mess'] = f'Ошибка сохранения источника: {e}.'
        if delete_source:
            try:
                _ = DcSourceSEO.objects.get(id=delete_source).delete()
                objs_source = DcSourceSEO.objects.filter(site=id_site).order_by('num')
                for i in range(len(objs_source)):
                    objs_source[i].num = i
                    objs_source[i].save()
            except Exception as e: context['error_mess'] = f'Ошибка удаления источника: {e}.'
        if id_change and direct:
            try:
                old_pos = DcSourceSEO.objects.get(id=id_change).num
                max_pos = DcSourceSEO.objects.filter(site=id_site).aggregate(Max('num'))['num__max']
                rec = True
                if (direct == 'change_down' and old_pos == max_pos) or (direct == 'change_up' and old_pos == 0): rec = False
                if rec:
                    objs_source = DcSourceSEO.objects.filter(site=id_site).order_by('num')
                    for i in range(len(objs_source)):
                        if direct == 'change_up':
                            if i == old_pos-1: objs_source[i].num = i+1
                            if i == old_pos: objs_source[i].num = i-1
                        if direct == 'change_down':
                            if i == old_pos+1: objs_source[i].num = i-1
                            if i == old_pos: objs_source[i].num = i+1
                        objs_source[i].save()
            except Exception as e: context['error_mess'] = f'Ошибка перемещения сайта: {e}.'
            

    objs_provider = DcCatalogProviderSEO.objects.all().values()
    provider_list = [row for row in objs_provider]
    context['provider_list'] = provider_list

    objs_source = DcCatalogSourceSEO.objects.all().values()
    source_list = [row for row in objs_source]
    context['source_list'] = source_list

    context['id_site'] = 0
    try: context['num'] = DcSiteSEO.objects.aggregate(Max('num'))['num__max'] + 1
    except: context['num'] = 1
    context['site'] = ''
    context['name'] = ''
    context['provider'] = ''
    if id_site > 0:
        objs_provider = DcSiteSEO.objects.filter(id=id_site)
        if len(objs_provider) == 1:
            context['id_site'] = id_site
            context['num'] = objs_provider[0].num
            context['site'] = objs_provider[0].site
            context['name'] = objs_provider[0].name
            context['provider'] = objs_provider[0].provider

        objs_source = DcSourceSEO.objects.filter(site=id_site).order_by('num')
        if len(objs_source) > 0:
            sources = [row for row in objs_source]
            context['sources'] = sources

    return render(request, 'domconnect/site_edit.html', context)


@login_required(login_url='/login/')
def sources(request):  #
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name, 'segment': 'sources'}

    tmp_data = DcSourceSEO.objects.order_by('num').values()
    data = [row for row in tmp_data]
    for dt in data:
        dt['source'] = DcCatalogSourceSEO.objects.get(id=dt['source_id']).name
        dt['site'] = DcSiteSEO.objects.get(id=dt['site_id']).site
        print(dt)

    context['data'] = data
    return render(request, 'domconnect/sources.html', context)


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
        # Обновим каталог 
        dounload_catalog()
        with open('SiteSource.json', 'r', encoding='utf-8') as file:
            js_data = json.load(file)
        if not js_data or len(js_data) == 0: raise Exception('Нет данных для обновления.')
        DcSiteSEO.objects.all().delete()
        DcSourceSEO.objects.all().delete()
        # Перебираем сайты с вложенными источниками и заносим в базу
        for dct_site in js_data:
            num =  dct_site.get('num')
            name_site = dct_site.get('name')
            site = dct_site.get('site')
            cod_provider = dct_site.get('provider')
            sources = dct_site.get('sources')
            if not num or not site or not cod_provider or not sources:
                raise Exception('Ошибка данных сайта для обновления.')
            obj_provider = DcCatalogProviderSEO.objects.get(prov_id=cod_provider)
            obj_site, _ = DcSiteSEO.objects.get_or_create(num=num, site=site, name=name_site, provider=obj_provider)
            if not obj_site: raise Exception('Ошибка сохранения сайта.')

            # Сохраняем источники
            for rec in sources:
                num_source = rec.get('num')
                name_source = rec.get('source')
                if not num_source or not name_source: raise Exception('Ошибка данных источника для обновления.')
                try:
                    obj_cat_source = DcCatalogSourceSEO.objects.get(name=name_source)
                except:
                    logger.error(f'Ошибка Икточник: {name_source} отсутствует в каталоге.')
                    continue

                obj_source, _ = DcSourceSEO.objects.get_or_create(num=num_source, source=obj_cat_source, site=obj_site)
                if not obj_source: raise Exception('Ошибка сохранения источника.')
            
    except Exception as e:
        err = f'Ошибка upgradeSiteSource: try: {e}'

    if err:
        logger.error(err)
        context = {
            'result': 'Error',
            'message': f'{err}',
            'result_style': 'danger',
        }
    else:
        logger.info('Site Source Service обновлены.')
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
            'message': 'Поток обновления и расчета уже идет.',
            'result_style': 'info',
        }
    else:
        # Запустим поток загрузки
        th = Thread(target=run_upgrade_seo, name=thread_name, args=())
        th.start()
        context = {
            'result': 'Ok',
            'message': 'Поток обновления и расчета запущен.',
            'result_style': 'success',
        }

    return render(request, 'domconnect/show_mess_and_redirect.html', context)
