# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
# from django.core.paginator import Paginator
# from app.forms import NameForm, LizaPhraseForm, GermanPhraseForm, NdzPhraseForm, PzPhraseForm
from domconnect.models import DomconnectCrmLid, GlobalVariable
from datetime import datetime as dt
import requests
import time
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




    context['segment'] = 'statseo'
    return render(request, 'domconnect/statseo.html', context)
    

@login_required(login_url='/login/')
def downloadLidsFromCRM(request, from_date):
    thread_name = 'DownLoadLidsFromCRM'
    if not request.POST:
        return redirect(reverse('app:home'))

    # Проверим - закончен ли процесс предыдущей загрузки
    for thread in threading.enumerate():
        if thread.getName() == thread_name:
            return HttpResponse('Процесс загрузки.', content_type='text/plain; charset=utf-8')

    th = Thread(target=thread_download_crm, name=thread_name, args=(from_date, ))
    th.start()

    return HttpResponse('Загрузка началась.', content_type='text/plain; charset=utf-8')


def fix_result_download_crm(mess):
    gvar, _ = GlobalVariable.objects.get_or_create(key='last_download_crm')
    gvar.val_datetime = dt.today()
    gvar.val_str = mess
    gvar.save()

def append_lids(lids):
    for new_lid in lids:
        # try:
        # print(new_lid)
        lid = DomconnectCrmLid.objects.get_or_create(id_lid=new_lid.get('ID'))
        lid.title = new_lid.get('TITLE')
        lid.status_id = new_lid.get('STATUS_ID')
        lid.create_date = dt.strptime(new_lid.get('DATE_CREATE'), '%Y-%m-%dT%H:%M:%S%z')  # "2022-01-01T04:43:22+03:00"
        lid.modify_date = dt.strptime(new_lid.get('DATE_MODIFY'), '%Y-%m-%dT%H:%M:%S%z')
        lid.source_id = int(new_lid.get('SOURCE_ID'))
        lid.assigned_by_id = int(new_lid.get('ASSIGNED_BY_ID'))
        lid.crm_1493416385 = new_lid.get('UF_CRM_1493416385')
        lid.crm_1499437861 = new_lid.get('UF_CRM_1499437861')
        lid.crm_1580454770 = new_lid.get('UF_CRM_1580454770')
        lid.crm_1534919765 = ';'.join(new_lid.get('UF_CRM_1534919765'))
        lid.crm_1571987728429 = new_lid.get('UF_CRM_1571987728429')
        lid.crm_1592566018 = ';'.join(new_lid.get('UF_CRM_1592566018'))
        lid.crm_1493413514 = new_lid.get('UF_CRM_1493413514')
        lid.crm_1492017494 = new_lid.get('UF_CRM_1492017494')
        lid.crm_1492017736 = new_lid.get('UF_CRM_1492017736')
        lid.crm_1498756113 = bool(new_lid.get('UF_CRM_1498756113'))
        lid.crm_1615982450 = new_lid.get('UF_CRM_1615982450')
        lid.crm_1615982567 = new_lid.get('UF_CRM_1615982567')
        lid.crm_1615982644 = new_lid.get('UF_CRM_1615982644')
        lid.crm_1615982716 = new_lid.get('UF_CRM_1615982716')
        lid.crm_1615982795 = new_lid.get('UF_CRM_1615982795')
        lid.crm_1640267556 = new_lid.get('UF_CRM_1640267556')
        lid.save()
        print(lid.id_lid, 'Ok')
        # except Exception as e: 
        #     lid.delete()
        #     return str(e)

def thread_download_crm(from_date):
    gvar, created = GlobalVariable.objects.get_or_create(key='url_download_crm')
    url = gvar.val_str
    if not url:
        print('Not url address')
        return   # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.list'
    
    print(f'start thread {from_date}')

    dt_start = dt.strptime(from_date, '%d.%m.%Y')
    str_dt_start = dt_start.strftime('%Y-%m-%dT%H:%M:%S')
    go_next = 0
    # go_total = 0
    # out_lst = []

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
            'order': {'DATE_MODIFY': 'ASC'},  # Если нужно с сортировкой
            'filter': {
                '>DATE_CREATE': str_dt_start,  # '2021-10-01T00:00:00'
                # '<DATE_CREATE': '2021-10-31T23:59:59',
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
        try:
            responce = requests.post(url, headers=headers, json=data)
            if responce.status_code == 200:
                answer = json.loads(responce.text)
                result = answer.get('result')
                go_next = answer.get('next')
                go_total = answer.get('total')
                print(go_next, go_total)
                append_lids(result)
                if not go_next: break
            else: return fix_result_download_crm(f'Ошибка get_lids: responce.status_code: {responce.status_code}\n{responce.text}')
        except Exception as e: fix_result_download_crm(f'Ошибка get_lids: try: requests.post {e}')

        time.sleep(1)
    
    fix_result_download_crm('')  # Зафиксируем время загрузки с пустым сообщением

    print('stop thread')














# gvar, created = GlobalVariable.objects.get_or_create(key='downloadcrm')
# gvar.val = 'False'
# gvar.save()

# gvar, created = GlobalVariable.objects.get_or_create(key='downloadcrm')
# if gvar.val == 'True': 
# else:
#     gvar.val = 'True'
#     gvar.save()
