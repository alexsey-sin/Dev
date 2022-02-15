from django.http import HttpResponse
from mobile.models import MobileNumber, MobileData
from api.models import BotVisit
from mobile.forms import MobileNumberForm
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from rest_framework import status
import json


def index(request):
    # group = get_object_or_404(LizaGroupPhrase, num_group=num_group)
    # phrases = LizaPhrase.objects.filter(group=group).order_by('text')
    # lst = []
    # for phr in phrases:
    #     lst.append(phr.text)
    
    return HttpResponse('Страница пока не готова.', content_type='text/plain; charset=utf-8')


def api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cnt = 0
        cnt_n = 0
        operator = data.get('operator')
        numbers = data.get('numbers')
        s_balance = data.get('balance')
        if s_balance:
            str_bal = s_balance.strip().replace(',', '.')
            try:
                f_balance = float(str_bal)
            except:
                return HttpResponse('Ошибка преобразования float.', content_type='text/plain; charset=utf-8')
        for num in numbers:
            str_num = num.get('number')
            s_num_balance = num.get('balance')
            try:
                num_balance = float(s_num_balance)
            except:
                num_balance = 0.0
            if len(str_num) != 11:
                break
            mob_num, created = MobileNumber.objects.get_or_create(number=str_num, opsos=operator)
            if created: cnt_n += 1
            row = MobileData()
            row.number = mob_num
            mob_avlbl = num.get('mobile_available')
            if mob_avlbl:
                row.mobile_available = int(mob_avlbl)
            mob_pkt = num.get('mobile_total')
            if mob_pkt:
                row.mobile_packet = int(mob_pkt)
            elif mob_num.mobile_packet:
                row.mobile_packet = mob_num.mobile_packet
            sms_avlbl = num.get('sms_available')
            if sms_avlbl:
                row.sms_available = int(sms_avlbl)
            sms_pkt = num.get('sms_total')
            if sms_pkt:
                row.sms_packet = int(sms_pkt)
            elif mob_num.sms_packet:
                row.sms_packet = mob_num.sms_packet
            if s_balance:
                row.balance = f_balance
            elif s_num_balance:
                row.balance = num_balance
            row.save()
            cnt += 1
        message = f'сохранено {cnt} записей.'
        if cnt_n:
            message += f' Новых {cnt_n}.'
        return HttpResponse(message, content_type='text/plain; charset=utf-8')
    
    return HttpResponse('Ошибка записи.', content_type='text/plain; charset=utf-8')


def numsetting(request):
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}

    if request.method == 'POST':
        form = MobileNumberForm(request.POST or None)
        id_edit = request.POST.get('edit', None)
        id_delete = request.POST.get('delete', None)

        if id_edit:  # редактирование
            try:
                if form.is_valid():
                    new_form = form.save(commit=False)
                    old_num = MobileNumber.objects.get(id=id_edit)
                    new_form.id = id_edit
                    new_form.opsos = old_num.opsos
                    new_form.number = old_num.number
                    new_form.save()
            except:
                context['error_mess'] = 'Ошибка редактирования.'
        elif id_delete:
            rec = get_object_or_404(MobileNumber, id=id_delete)
            rec.delete()
        else:
            context['error_mess'] = 'Ошибка запроса.'
    
    # queryset в список словарей
    tmp_data = MobileNumber.objects.order_by('opsos', 'number').values()
    data = [row for row in tmp_data]
    for row_data in data:
        try:
            pc = row_data.get('package_cost')
            obc = row_data.get('oatc_batc_cost')
            obj_mob_sett = MobileNumber.objects.get(id=row_data['id'])
            pack_m = obj_mob_sett.mobile_number.all().last().mobile_packet
            pack_s = obj_mob_sett.mobile_number.all().last().sms_packet
            pcbc = pc + obc
            if pcbc > 0 and pack_m > 0:
                row_data['price_min'] = f'{(pcbc/pack_m):.2f}'
            else:
                continue
            row_data['price_min_sms'] = f'{(pcbc/(pack_m+pack_s)):.2f}'
        except:
            continue

    if len(data) == 0:
        context['error_mess'] = 'Нет номеров.'

    form = MobileNumberForm()
    context['form'] = form

    paginator = Paginator(data, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context['segment'] = 'numsetting'
    context['page_number'] = page_number
    context['page'] = page
    context['paginator'] = paginator

    return render(request,'mobile/Numbers.html', context)


def numcondition(request):
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}

    # queryset в список словарей
    tmp_data = MobileNumber.objects.filter(active=True).order_by('opsos', 'number').values()
    data = [row for row in tmp_data]
    total_packet_min = 0
    total_spent_min = 0
    total_avlbl_min = 0
    total_packet_sms = 0
    total_spent_sms = 0
    total_avlbl_sms = 0
    days_for_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31,]
    num_date = datetime.now().day
    num_month = datetime.now().month
    num_days_for_current_month = days_for_month[num_month]
    for row_data in data:
        try:
            obj_mob_sett = MobileNumber.objects.get(id=row_data['id'])
            mob_data = obj_mob_sett.mobile_number.all().last()
            row_data['id_data_mob'] = mob_data.id
            m_aval = mob_data.mobile_available
            m_pack = mob_data.mobile_packet
            row_data['mobile_available'] = m_aval
            row_data['mobile_packet'] = m_pack
            if m_aval: total_avlbl_min += m_aval
            if m_pack:
                total_packet_min += m_pack
                if m_aval == None: m_aval = 0
                m_spt = m_pack - m_aval
                row_data['mobile_spent'] = m_spt
                total_spent_min += m_spt

            row_data['num_date'] = num_date
            s_aval = mob_data.sms_available
            s_pack = mob_data.sms_packet
            row_data['sms_available'] = s_aval
            row_data['sms_packet'] = s_pack
            if s_aval: total_avlbl_sms += s_aval
            if s_pack:
                total_packet_sms += s_pack
                if s_aval == None: s_aval = 0
                s_spt = s_pack - s_aval
                row_data['sms_spent'] = s_spt
                total_spent_sms += s_spt
        except:
            continue
    avrg_min = round(total_spent_min / num_date, 2)
    avrg_sms = round(total_spent_sms / num_date, 2)
    total = {
        'total_packet_min': total_packet_min, 'total_packet_sms': total_packet_sms,
        'total_spent_min': total_spent_min, 'total_spent_sms': total_spent_sms,
        'total_avlbl_min': total_avlbl_min, 'total_avlbl_sms': total_avlbl_sms,
    }
    average = {'avrg_min': avrg_min, 'avrg_sms': avrg_sms}
    forecast = {
        'min_month': round(avrg_min * num_days_for_current_month, 2),
        'sms_month': round(avrg_sms * num_days_for_current_month, 2),
    }

    context['segment'] = 'numcondition'
    context['data'] = data
    context['total'] = total
    context['average'] = average
    context['forecast'] = forecast

    return render(request,'mobile/Condition.html', context)


def get_mobile_residue(request):
    if request.method == 'GET':
        try:
            key = request.GET.get('key')
            if key != 'Q8kGM1HfWz': raise ValueError('ERROR key.')

            if not request.body: raise ValueError('empty request - empty response')
            num_query = json.loads(request.body)
            nums = num_query.get('nums')
            # Здесь nums = [] - список номеров в 11 значном формате
            out_dict = {}
            if nums:
                for num in nums:
                    # проверка номера на цифры и длину
                    if num == None: out_dict[num] = 'no number assigned'; continue
                    if not num.isdigit(): out_dict[num] = 'number is not digit'; continue
                    if len(num) != 11: out_dict[num] = 'number bad length'; continue

                    # проверка номера на присутствие в базе
                    obj_num = MobileNumber.objects.filter(number=num)
                    if not obj_num: out_dict[num] = 'number is absent'; continue

                    # проверка номера на наличие данных по остаткам минут
                    query_num_data = MobileData.objects.filter(number=obj_num[0]).last()
                    if not query_num_data: out_dict[num] = 'no data for this number'; continue

                    # Проверяем на исключительную ситуацию (безлимит или отключен)
                    is_excrpt = obj_num[0].ats_except
                    if is_excrpt:
                        residue = obj_num[0].ats_except_min
                    else:
                        residue = MobileData.objects.filter(number=obj_num[0]).last().mobile_available
                    out_dict[num] = residue
        except ValueError as e:
            return HttpResponse(f'ERROR: {e}', status=status.HTTP_400_BAD_REQUEST)
        
        obj_visit, _ = BotVisit.objects.get_or_create(name='ATS-TRUNK')
        obj_visit.last_visit = datetime.now()
        obj_visit.save()
        
        data = json.dumps(out_dict)
        return HttpResponse(data, content_type='application/json; charset=utf-8', status=status.HTTP_200_OK)
    
    return HttpResponse('Use GET request, please.', status=status.HTTP_400_BAD_REQUEST)
###############################################################################
###############################################################################
