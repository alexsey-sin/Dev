from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# from django.contrib.auth import get_user_model
# from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime as dt
import requests
import time
import json
import threading
from threading import Thread
 
# User = get_user_model()


@login_required(login_url="/login/")
def index(request):
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}

    # return render(request, 'app/index.html', context)
    return render(request, 'office/index.html', context)
    

@login_required(login_url="/login/")
def moexbond(request):
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name, 'page_title': 'Лиза'}

    # group = get_object_or_404(LizaGroupPhrase, id=id_group)
    # context['group_name'] = group.text
    
    # if request.method == 'POST':
        # form = LizaPhraseForm(request.POST or None)
        # id_edit = request.POST.get('edit', None)
        # id_delete = request.POST.get('delete', None)

        # if id_edit:  # редактирование
            # try:
                # rec = get_object_or_404(LizaPhrase, id=id_edit)
                # rec.text = request.POST.get("text")
                # rec.author = user
                # rec.save()
            # except:
                # context['error_mess'] = 'Ошибка редактирования, возможно такая фраза уже существует.'
        # elif id_delete:
            # rec = get_object_or_404(LizaPhrase, id=id_delete)
            # rec.delete()
        # elif form.is_valid():
            # new_form = form.save(commit=False)
            # new_form.group = group
            # new_form.author = user
            # new_form.save()
        # else:
            # context['error_mess'] = 'Ошибка заполнения формы, возможно такая фраза уже существует.'

    # form = LizaPhraseForm()
    # context['form'] = form

    # data = LizaPhrase.objects.filter(group=group.id).order_by('pub_date')
    # context['cnt_phrases'] = data.count()
    # paginator = Paginator(data, 20)
    # page_number = request.GET.get('page')
    # page = paginator.get_page(page_number)

    # context['page_number'] = page_number
    # context['page'] = page
    # context['paginator'] = paginator

    return render(request, 'office/moexbond.html', context)


def download_moex(request):
    if not request.POST: return JsonResponse({})
    
    thread_name = 'DownLoadBondFromMOEX'

    # Проверим - закончен ли процесс предыдущей загрузки
    for thread in threading.enumerate():
        if thread.getName() == thread_name:
            return HttpResponse('Процесс загрузки.', content_type='text/plain; charset=utf-8')

    th = Thread(target=thread_download_bond_moex, name=thread_name, args=())
    th.start()

    # return HttpResponse('Загрузка началась.', content_type='text/plain; charset=utf-8')
    response = {
        'is_taken': 25,
    }
    return JsonResponse(response)

def fix_result(mess):
    gvar, _ = GlobalVariable.objects.get_or_create(key='last_download_crm')
    gvar.val_datetime = dt.today()
    gvar.val_str = mess
    gvar.save()

def append_bond_moex(lids):
    for new_lid in lids:
        # try:
        print('before lid:')
        lid = DomconnectCrmLid.objects.get_or_create(id_lid=int(new_lid.get('ID')))
        print('after lid:', lid)
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

def GetMOEXsecidBonds()
    str_url = "http://iss.moex.com/iss/securities.json"
    outList = []
    start = 7600
    limit = 100
    search_parameters = {
        'lang': 'ru',
        'group_by': 'group',
        'group_by_filter': 'stock_bonds',
    }

    while(True):
        try:
            search_parameters['limit'] = limit
            search_parameters['start'] = start
            response = requests.get(str_url, params=search_parameters)
            if response.status_code != 200:
                raise Exception(f'Ответ сервера: {response.status_code}')
            res = response.json()
            ind_sec_id = res['securities']['columns'].index('secid')
            cnt = len(res['securities']['data'])
            if cnt == 0:
                break
            self.message_value.emit(f'Загружаем предварительный список: {len(outList)+cnt}')
            for i in range(cnt):
                sec_id = res['securities']['data'][i][ind_sec_id]
                outList.append(sec_id)
                self.message_value.emit(sec_id)
        except Exception as exc:
            self.message_value.emit(f'Ошибка загрузки списка: {exc}')
            print(exc)
            break

        start += limit
    return outList


def thread_download_bond_moex(from_date):
    listSecIdBonds = GetMOEXsecidBonds()  # []
    
    
    # gvar, created = GlobalVariable.objects.get_or_create(key='url_download_moex')
    # url = gvar.val_str
    # if not url:
        # fix_result('Not url address')
        # return   # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.list'
    
    # print('start thread')

    # # dt_start = dt.strptime(from_date, '%d.%m.%Y')
    # # str_dt_start = dt_start.strftime('%Y-%m-%dT%H:%M:%S')
    # go_next = 0
    # # go_total = 0
    # # out_lst = []

    # headers = {
        # 'Content-Type': 'application/json',
        # 'Connection': 'Keep-Alive',
        # 'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    # }
    # # print(str_dt_start)
    # # return '', []
    # while True:
        # data = {
            # 'start': go_next,
            # 'order': {'DATE_MODIFY': 'ASC'},  # Если нужно с сортировкой
            # 'filter': {
                # '>DATE_CREATE': str_dt_start,  # '2021-10-01T00:00:00'
                # # '<DATE_CREATE': '2021-10-31T23:59:59',
            # },
            # 'select': [
                # 'ID', 
                # 'TITLE', 
                # 'STATUS_ID', 
                # 'DATE_CREATE',
                # 'DATE_MODIFY',
                # 'SOURCE_ID',
                # 'ASSIGNED_BY_ID',
                # 'UF_CRM_1493416385',  # Сумма тарифа
                # 'UF_CRM_1499437861',  # ИНН/Организация
                # 'UF_CRM_1580454770',  # Звонок?
                # 'UF_CRM_1534919765',  # Группы источников
                # 'UF_CRM_1571987728429',  # Провайдеры ДК
                # 'UF_CRM_1592566018',  # ТИп лида
                # 'UF_CRM_1493413514',  # Провайдер
                # 'UF_CRM_1492017494',  # Область
                # 'UF_CRM_1492017736',  # Город
                # 'UF_CRM_1498756113',  # Юр. лицо

                # 'UF_CRM_1615982450',  # utm_source
                # 'UF_CRM_1615982567',  # utm_medium
                # 'UF_CRM_1615982644',  # utm_campaign
                # 'UF_CRM_1615982716',  # utm_term                
                # 'UF_CRM_1615982795',  # utm_content                
                # 'UF_CRM_1640267556',  # utm_group 
            # ]
        # }
        # try:
            # responce = requests.post(url, headers=headers, json=data)
            # if responce.status_code == 200:
                # answer = json.loads(responce.text)
                # result = answer.get('result')
                # go_next = answer.get('next')
                # go_total = answer.get('total')
                # print(go_next, go_total)
                # append_bond_moex(result)
                # if not go_next: break
            # else: return fix_result(f'Ошибка get_lids: responce.status_code: {responce.status_code}\n{responce.text}')
        # except Exception as e: fix_result(f'Ошибка get_lids: try: requests.post {e}')

        # time.sleep(1)
    
    # fix_result('')  # Зафиксируем время загрузки с пустым сообщением

    # print('stop thread')

# https://pythonru.com/primery/django-ajax
