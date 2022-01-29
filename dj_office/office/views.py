from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# from django.contrib.auth import get_user_model
# from django.http import HttpResponse
from office.models import TypeBOND, MoexBOND, GlobalVariable, FilterBOND
from office.forms import FilterBONDForm
from datetime import datetime, timedelta
import requests
import time
from django.http import JsonResponse
import json
import threading
from threading import Thread
from django.http import JsonResponse
from decimal import Decimal

 
# User = get_user_model()


@login_required(login_url="/login/")
def index(request):
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}


    # group = get_object_or_404(LizaGroupPhrase, id=id_group)
    # context['group_name'] = group.text
    
    # if request.method == 'POST':
        # id_filter = request.POST.get('id_filter', None)
        # if id_filter:
            # form = LizaPhraseForm(request.POST or None)
            # if form.is_valid():
                # new_form = form.save(commit=False)
                # new_form.by_type = '["djdhss", ";lktirr45","mmbnhcy"]'
                # new_form.save()
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

    return render(request, 'office/index.html', context)


@login_required(login_url="/login/")
def moexbond(request):
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name, 'page_title': 'Облигации ММВБ'}
    context['segment'] = 'moexbond'
    error_mess = ''
    success_mess = ''
    
    if request.method == 'POST':
        # print('POST')
        # id_filter = request.POST.get('id_filter', None)
        # if id_filter:
            # print('id_filter', id_filter)
        form = FilterBONDForm(request.POST or None)
        if form.is_valid():
            # print('form.is_valid')
            new_form = form.save(commit=False)
            new_form.by_type = '["djdhss", ";lktirr45","mmbnhcy"]'
            new_form.save()
            # print('save.ok')
            success_mess = 'Фильтр сохранен.'
        else:
            for field in form.errors:
               error_mess += f'{field} {form.errors[field].as_text()}\n'
    
    all_filters = FilterBOND.objects.all()
    filters = []
    for f in all_filters: filters.append({'id': f.id, 'name': f.name})
    context['filters'] = filters
    print(filters)
    
    # error_mess = 'Фильтр должен иметь название'
    gvar_end, _ = GlobalVariable.objects.get_or_create(key='end_download')
    val = gvar_end.val_int
    if val: context['num_all_bond'] = val
    else: context['num_all_bond'] = 0
    val = gvar_end.val_datetime
    if val: context['last_upgrade'] = f'Обновлено: {val.strftime("%d.%m.%Y")}'
    else: context['last_upgrade'] = '---'
    if error_mess: context['error_mess'] = error_mess
    if success_mess: context['success_mess'] = success_mess
    return render(request, 'office/moexbond.html', context)


@login_required(login_url="/login/")
def testbond(request):
    response = {'value': 0}
    # obj_type, _ = TypeBOND.objects.get_or_create(typekey='hfjddytyst19818')
    # lid, _ = MoexBOND.objects.get_or_create(secid='dkd123456', typekey=obj_type)
    # print(obj_type)
    # print(obj_type.id)
    
    # print(lid)
    # # lid.save()
    # print(lid.id)
    return JsonResponse(response)


def download_moex(request):
    thread_name = 'DownLoadBondFromMOEX'
    if not request.GET: return JsonResponse({})

    is_run = False
    for thread in threading.enumerate():
        if thread.getName() == thread_name: is_run = True; break
    response = {'is_run': is_run}
    
    # Посмотрим нужны ли данные по загрузке
    get_state = request.GET.get('get_state')
    if get_state:
        gvar_cur, _ = GlobalVariable.objects.get_or_create(key='cur_num_download')
        gvar_tot, _ = GlobalVariable.objects.get_or_create(key='tot_num_download')
        gvar_end, _ = GlobalVariable.objects.get_or_create(key='end_download')
        response['val_current'] = gvar_cur.val_int
        response['val_total'] = gvar_tot.val_int
        response['num_all_bond'] = gvar_end.val_int
        response['last_upgrade'] = gvar_end.val_datetime.strftime('%d.%m.%Y')

        
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

def fix_result(mess):
    gvar, _ = GlobalVariable.objects.get_or_create(key='log_download')
    gvar.val_datetime = datetime.today()
    if not gvar.descriptions: gvar.descriptions = mess
    else: gvar.descriptions = gvar.descriptions + mess
    gvar.save()

def GetMOEXsecidBonds():  # Загрузка списка бумаг
    str_url = "http://iss.moex.com/iss/securities.json"
    outList = []
    start = 7600
    # start = 0
    limit = 100
    search_parameters = {
        'lang': 'ru',
        'group_by': 'group',
        'group_by_filter': 'stock_bonds',
    }
    
    print('Загрузка списка.')
    cnt_err = 0
    while(True):
        gvar_go, _ = GlobalVariable.objects.get_or_create(key='go_download')
        if gvar_go.val_bool == False: break
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

def GetMOEXBonds(listSecId):  # Загрузка бумаг и сохранение в базу
    # For example can be substituted RU000A101PV6.json
    str_url_tmp = "http://iss.moex.com/iss/securities/"
    
    print('Загрузка бумаг.')
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
                obj_type, _ = TypeBOND.objects.get_or_create(typekey=dict_bond['TYPE'])
                lid, _ = MoexBOND.objects.get_or_create(secid=dict_bond['SECID'], typekey=obj_type)
                lid.name = dict_bond['NAME']
                lid.matdate = datetime.strptime(dict_bond['MATDATE'], '%Y-%m-%d')
                lid.facevalue = dict_bond['FACEVALUE']
                lid.couponfrequency = dict_bond['COUPONFREQUENCY']
                lid.couponvalue = dict_bond['COUPONVALUE']
                obj_type, _ = TypeBOND.objects.get_or_create(typekey=dict_bond['TYPE'])
                # Вычисляем номинальную доходность
                try:
                    kup = Decimal(dict_bond['COUPONVALUE'])
                    kup_year = int(dict_bond['COUPONFREQUENCY'])
                    nominal = Decimal(dict_bond['FACEVALUE'])
                    if kup > 0 and kup_year > 0 and nominal > 0:
                        lid.profit = ((kup * kup_year) / nominal) * 100
                    else: continue
                except Exception as e: print(e)
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

def thread_download_bond_moex():  # Поток загрузки бумаг
    MoexBOND.objects.all().delete()
    listSecIdBonds = GetMOEXsecidBonds()  # []
    GetMOEXBonds(listSecIdBonds)
    all_cnt = MoexBOND.objects.all().count()
    gvar_end, _ = GlobalVariable.objects.get_or_create(key='end_download')
    gvar_end.val_int = all_cnt
    gvar_end.val_datetime = datetime.today()
    gvar_end.save()
    print('Загрузка завершена.')
    

# https://pythonru.com/primery/django-ajax
