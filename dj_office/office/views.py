from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# from django.contrib.auth import get_user_model
# from django.http import HttpResponse
from office.models import MoexBOND, GlobalVariable
from datetime import datetime
from datetime import timedelta
import requests
import time
from django.http import JsonResponse
import json
import threading
from threading import Thread
from django.http import JsonResponse
from datetime import datetime as dt
 
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
    thread_name = 'DownLoadBondFromMOEX'
    if not request.GET: return JsonResponse({})

    # str_from_modify = ''
    # last_modify_lid = DomconnectCrmLid.objects.order_by('modify_date').last()
    # if last_modify_lid:
        # from_modify = last_modify_lid.modify_date
        # from_modify = from_modify - timedelta(seconds=1)
        # str_from_modify = from_modify.strftime('%Y-%m-%dT%H:%M:%S')


    # return JsonResponse({'is_run': False})

    # Проверим идет ли загрузка
    is_run = False
    for thread in threading.enumerate():
        if thread.getName() == thread_name: is_run = True; break
    response = {'is_run': is_run}
    
    # Посмотрим нужны ли данные по загрузке
    get_state = request.GET.get('get_state')
    if get_state:
        gvar_cur, _ = GlobalVariable.objects.get_or_create(key='cur_num_download')
        gvar_tot, _ = GlobalVariable.objects.get_or_create(key='tot_num_download')
        response['val_current'] = gvar_cur.val_int
        response['val_total'] = gvar_tot.val_int
        
    is_stop = request.GET.get('stop')
    if is_stop:
        gvar_go, _ = GlobalVariable.objects.get_or_create(key='go_download')
        gvar_go.val_bool = False
        gvar_go.save()

    is_start = request.GET.get('start')
    if is_start and not is_run:
        # Разрешим загрузку в глобальной переменной
        gvar_go, _ = GlobalVariable.objects.get_or_create(key='go_download')
        gvar_go.val_bool = True
        gvar_go.save()

        # Обнулим глоб. переменную текущей позиции
        gvar_cur, _ = GlobalVariable.objects.get_or_create(key='cur_num_download')
        gvar_cur.val_int = 0
        gvar_cur.save()
        
        # Очистим лог
        gvar, _ = GlobalVariable.objects.get_or_create(key='log_download')
        gvar.val_datetime = None
        gvar.descriptions = None
        gvar.save()

        # Запустим поток загрузки
        th = Thread(target=thread_download_bond_moex, name=thread_name, args=())
        th.start()
        response['is_run'] = True
    return JsonResponse(response)
    # if not request.POST: return JsonResponse({})
    
    # thread_name = 'DownLoadBondFromMOEX'

    # # Проверим - закончен ли процесс предыдущей загрузки
    # for thread in threading.enumerate():
        # if thread.getName() == thread_name:
            # return HttpResponse('Процесс загрузки.', content_type='text/plain; charset=utf-8')

    # th = Thread(target=thread_download_bond_moex, name=thread_name, args=())
    # th.start()

    # # return HttpResponse('Загрузка началась.', content_type='text/plain; charset=utf-8')
    # response = {
        # 'is_taken': 25,
    # }
    # return JsonResponse(response)

def fix_result(mess):
    gvar, _ = GlobalVariable.objects.get_or_create(key='log_download')
    gvar.val_datetime = dt.today()
    if not gvar.descriptions: gvar.descriptions = mess
    else: gvar.descriptions = gvar.descriptions + mess
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

def GetMOEXsecidBonds():
    str_url = "http://iss.moex.com/iss/securities.json"
    outList = []
    # start = 7600
    start = 0
    limit = 100
    search_parameters = {
        'lang': 'ru',
        'group_by': 'group',
        'group_by_filter': 'stock_bonds',
    }
    
    cnt_err = 0
    while(True):
        gvar_go, _ = GlobalVariable.objects.get_or_create(key='go_download')
        if gvar_go.val_bool == False: break
        print('list')
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
            for i in range(cnt):
                sec_id = res['securities']['data'][i][ind_sec_id]
                outList.append(sec_id)
        except Exception as exc:
            cnt_err += 1

        start += limit
    if cnt_err: fix_result(f'Ошибок загрузки списка: {cnt_err}')
    return outList

def GetMOEXBonds(listSecId):
    # For example can be substituted RU000A101PV6.json
    str_url_tmp = "http://iss.moex.com/iss/securities/"
    
    cnt_err = 0
    total = len(listSecId)
    for i in range(total):
        gvar_go, _ = GlobalVariable.objects.get_or_create(key='go_download')
        if gvar_go.val_bool == False: break
        try:
            str_url = f'{str_url_tmp}{listSecId[i]}.json'
            response = requests.get(str_url)
            if response.status_code != 200:
                raise Exception(f'Ответ сервера: {response.status_code}')
            res = response.json()
            
            cnt_field = 0
            dict_bond = {}
            dict_bond['SECID'] = listSecId[i]
            # перелистаем поля бумаги
            for fldBond in res['description']['data']:
                if fldBond[0] == 'SECID' and listSecId[i] == fldBond[2]:
                    cnt_field += 1
                if fldBond[0] == 'NAME':
                    dict_bond['NAME'] = fldBond[2]
                    cnt_field += 1
                if fldBond[0] == 'MATDATE':
                    dict_bond['MATDATE'] = fldBond[2]
                    cnt_field += 1
                if fldBond[0] == 'FACEVALUE':
                    dict_bond['FACEVALUE'] = fldBond[2]
                    cnt_field += 1
                if fldBond[0] == 'COUPONFREQUENCY':
                    dict_bond['COUPONFREQUENCY'] = fldBond[2]
                    cnt_field += 1
                if fldBond[0] == 'COUPONVALUE':
                    dict_bond['COUPONVALUE'] = fldBond[2]
                    cnt_field += 1
                if fldBond[0] == 'TYPE':
                    dict_bond['TYPE'] = fldBond[2]
                    cnt_field += 1

            if cnt_field == 7:
                lid, _ = MoexBOND.objects.get_or_create(secid=dict_bond['SECID'])
                lid.name = dict_bond['NAME']
                lid.matdate = dt.strptime(dict_bond['MATDATE'], '%Y-%m-%d')
                lid.facevalue = dict_bond['FACEVALUE']
                lid.couponfrequency = dict_bond['COUPONFREQUENCY']
                lid.couponvalue = dict_bond['COUPONVALUE']
                lid.typename = dict_bond['TYPE']
                lid.save()


        except Exception as e:
            print(e)
            cnt_err += 1
        gvar_cur, _ = GlobalVariable.objects.get_or_create(key='cur_num_download')
        gvar_cur.val_int = i
        gvar_cur.save()
        gvar_tot, _ = GlobalVariable.objects.get_or_create(key='tot_num_download')
        gvar_tot.val_int = total
        gvar_tot.save()

    if cnt_err: fix_result(f'Ошибок загрузки бумаг: {cnt_err}')

def thread_download_bond_moex():
    MoexBOND.objects.all().delete()
    listSecIdBonds = GetMOEXsecidBonds()  # []
    GetMOEXBonds(listSecIdBonds)
    

# https://pythonru.com/primery/django-ajax
