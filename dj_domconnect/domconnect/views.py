# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
# from django.core.paginator import Paginator
# from app.forms import NameForm, LizaPhraseForm, GermanPhraseForm, NdzPhraseForm, PzPhraseForm
from domconnect.models import DomconnectCrmLid, GlobalVariable
from datetime import datetime
from datetime import timedelta
import requests
import time
from django.http import JsonResponse
import json
import threading
from threading import Thread


@login_required(login_url='/login/')
def index(request):
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}

    # lid = DomconnectCrmLid.objects.get_or_create(id_lid='123')
    # print(datetime.now())


    context['segment'] = 'statseo'
    return render(request, 'domconnect/statseo.html', context)
    

@login_required(login_url='/login/')
def downloadLidsFromCRM(request):
    thread_name = 'DownLoadLidsFromCRM'
    if not request.GET: return JsonResponse({})

    str_from_modify = ''
    last_modify_lid = DomconnectCrmLid.objects.order_by('modify_date').last()
    if last_modify_lid:
        from_modify = last_modify_lid.modify_date
        from_modify = from_modify - timedelta(seconds=1)
        str_from_modify = from_modify.strftime('%Y-%m-%dT%H:%M:%S')


    # return JsonResponse({'is_run': False})

    # Проверим идет ли загрузка
    is_run = False
    for thread in threading.enumerate():
        if thread.getName() == thread_name: is_run = True; break
    response = {'is_run': is_run}
    
    # Посмотрим нужны ли данные по загрузке
    get_state = request.GET.get('get_state')
    if get_state:
        gvar_cur, _ = GlobalVariable.objects.get_or_create(key='cur_num_download_crm')
        gvar_tot, _ = GlobalVariable.objects.get_or_create(key='tot_num_download_crm')
        response['val_current'] = gvar_cur.val_int
        response['val_total'] = gvar_tot.val_int
        
    is_stop = request.GET.get('stop')
    if is_stop:
        gvar_go, _ = GlobalVariable.objects.get_or_create(key='go_download_crm')
        gvar_go.val_bool = False
        gvar_go.save()

    is_start = request.GET.get('start')
    if is_start and not is_run:
        # Разрешим загрузку в глобальной переменной
        gvar_go, _ = GlobalVariable.objects.get_or_create(key='go_download_crm')
        gvar_go.val_bool = True
        gvar_go.save()

        # Обнулим глоб. переменную текущей позиции
        gvar_cur, _ = GlobalVariable.objects.get_or_create(key='cur_num_download_crm')
        gvar_cur.val_int = 0
        gvar_cur.save()

        # Очистим лог
        gvar, _ = GlobalVariable.objects.get_or_create(key='log_download')
        gvar.val_datetime = None
        gvar.descriptions = None
        gvar.save()

        # Запустим поток загрузки
        th = Thread(target=thread_download_crm, name=thread_name, args=(str_from_modify, ))
        th.start()
        response['is_run'] = True
    return JsonResponse(response)


def fix_result_download_crm(mess):
    gvar, _ = GlobalVariable.objects.get_or_create(key='log_download_crm')
    gvar.val_datetime = datetime.now()
    gvar.descriptions += mess
    gvar.save()

def append_lids(lids):
    cnt_err = 0
    for new_lid in lids:
        err = True
        try:
            lid, _ = DomconnectCrmLid.objects.get_or_create(id_lid=new_lid.get('ID'))
            lid.title = new_lid.get('TITLE')
            lid.status_id = new_lid.get('STATUS_ID')
            lid.create_date = datetime.strptime(new_lid.get('DATE_CREATE')[:-6], '%Y-%m-%dT%H:%M:%S')  # "2022-01-01T04:43:22+03:00"
            lid.modify_date = datetime.strptime(new_lid.get('DATE_MODIFY')[:-6], '%Y-%m-%dT%H:%M:%S')
            lid.assigned_by_id = new_lid.get('ASSIGNED_BY_ID')
            lid.crm_1493416385 = new_lid.get('UF_CRM_1493416385')
            lid.crm_1499437861 = new_lid.get('UF_CRM_1499437861')
            lid.crm_1580454770 = new_lid.get('UF_CRM_1580454770')
            val_field = new_lid.get('UF_CRM_1534919765')
            if val_field and len(val_field) > 0: lid.crm_1534919765 = val_field[0]
            lid.crm_1571987728429 = new_lid.get('UF_CRM_1571987728429')
            val_field = new_lid.get('UF_CRM_1592566018')
            if val_field and len(val_field) > 0: lid.crm_1592566018 = val_field[0]
            lid.crm_1493413514 = new_lid.get('UF_CRM_1493413514')
            lid.crm_1492017494 = new_lid.get('UF_CRM_1492017494')
            lid.crm_1492017736 = new_lid.get('UF_CRM_1492017736')
            lid.crm_1498756113 = new_lid.get('UF_CRM_1498756113')
            lid.crm_1615982450 = new_lid.get('UF_CRM_1615982450')
            lid.crm_1615982567 = new_lid.get('UF_CRM_1615982567')
            lid.crm_1615982644 = new_lid.get('UF_CRM_1615982644')
            lid.crm_1615982716 = new_lid.get('UF_CRM_1615982716')
            lid.crm_1615982795 = new_lid.get('UF_CRM_1615982795')
            lid.crm_1640267556 = new_lid.get('UF_CRM_1640267556')
            lid.save()
            err = False
        except Exception as e: 
            print(str(e))
        if err: cnt_err += 1
    return cnt_err


def thread_download_crm(str_from_modify):
    gvar, create = GlobalVariable.objects.get_or_create(key='url_download_crm')
    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.list'
    if create:
        gvar.val_str = url
        gvar.save()
    else:
        url = gvar.val_str
    
    print(f'start thread {str_from_modify}')

    # dt_start = dt.strptime(from_date, '%d.%m.%Y')
    # str_dt_start = dt_start.strftime('%Y-%m-%dT%H:%M:%S')
    go_next = 0
    go_total = 0

    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }

    cnt_err = 0
    while True:
        gvar_go, _ = GlobalVariable.objects.get_or_create(key='go_download_crm')
        if gvar_go.val_bool == False: break
        data = {
            'start': go_next,
            'order': {'DATE_MODIFY': 'ASC'},  # С сортировкой
            'filter': {
                # '>DATE_CREATE': '2020-01-01T00:00:00',  # '2021-10-01T00:00:00'
                '>DATE_CREATE': '2022-01-01T00:00:00',  # '2021-10-01T00:00:00'
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
                cnt_err += append_lids(result)
                if not go_next: break
            else: return fix_result_download_crm(f'Ошибка get_lids: responce.status_code: {responce.status_code}\n{responce.text}')
        except Exception as e: fix_result_download_crm(f'Ошибка get_lids: try: requests.post {e}')
        gvar_cur, _ = GlobalVariable.objects.get_or_create(key='cur_num_download_crm')
        gvar_cur.val_int = go_next
        gvar_cur.save()
        gvar_tot, _ = GlobalVariable.objects.get_or_create(key='tot_num_download_crm')
        gvar_tot.val_int = go_total
        gvar_tot.save()
        time.sleep(1)
    
    gvar_go, _ = GlobalVariable.objects.get_or_create(key='go_download_crm')
    gvar_go.val_bool = False
    gvar_go.save()
    mess = f'Обработано лидов: {go_total}. Ошибок: {cnt_err}'
    fix_result_download_crm(mess)
    print('stop thread')


@login_required(login_url='/login/')
def deleteAllLids(request):
    DomconnectCrmLid.objects.all().delete()
    return HttpResponse('Delete all.', content_type='text/plain; charset=utf-8')
    






