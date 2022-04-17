from django.http.request import HttpRequest
from django.http import HttpResponse
from rest_framework import status
from api.models import TxV, BotAccess, PV_VARS
from django.forms.models import model_to_dict
import json
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
# import logging

# logger = logging.getLogger('django_log')

def set_txv(request):
    if request.method == 'GET':
        # cur_time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        # logger.info(cur_time)
        # logger.info(str(request.GET))
        try:
            key = request.GET.get('key')
            if key != 'Q8kGM1HfWz':
                return HttpResponse('ERROR key.', status=status.HTTP_400_BAD_REQUEST)

            txv = TxV()
            pv_name = ''
            pv = request.GET.get('pv_code')
            dct_pv = {k : v for k, v in PV_VARS}  # Преобразуем кортеж кортежей в словарь
            if pv:
                try:
                    txv.pv_code = int(pv)
                    pv_name = dct_pv.get(txv.pv_code)
                    if pv_name == None: raise ValueError('pv_code is undefined')
                except: raise ValueError('pv_code is not integer')
            else: raise ValueError('pv_code is absent')

            # Возьмем доступы
            obj_visit, _ = BotAccess.objects.get_or_create(name=f'Бот ТХВ {pv_name}')
            txv.login = obj_visit.login
            txv.password = obj_visit.password
            txv.login_2 = obj_visit.login_2
            txv.password_2 = obj_visit.password_2

            id_lid = request.GET.get('id_lid')
            if id_lid: txv.id_lid = id_lid

            provider_dc = request.GET.get('provider_dc')
            if provider_dc: txv.provider_dc = provider_dc

            region = request.GET.get('region', '')
            if region: txv.region = region

            city = request.GET.get('city')
            if city == None or len(city) == 0: raise ValueError('city is absent')
            txv.city = city

            street = request.GET.get('street')
            if street == None or len(street) == 0: raise ValueError('street is absent')
            txv.street = street
            
            house = request.GET.get('house')
            if house == None or len(house) == 0: raise ValueError('house is absent')
            txv.house = house

            apartment = request.GET.get('apartment', '')
            if apartment: txv.apartment = apartment

            # Проверим нет ли уже такого адреса этого провайдера в базе
            old_date = datetime.today() - timedelta(days=3)  # __lte <= ;  __gte >=
            old_txv = TxV.objects.filter(pv_code=txv.pv_code, region=region, city=city, street=street, house=house, apartment=apartment, pub_date__gte=old_date)
            if len(old_txv) > 0:
                ans_mes = old_txv[0].available_connect
                if len(ans_mes) == 0: ans_mes = old_txv[0].bot_log
                return HttpResponse(f'txv already exists: \n{ans_mes}.', status=status.HTTP_200_OK)

            txv.status = 0
            txv.save()
        except ValueError as e:
            return HttpResponse(f'ERROR data. {e}', status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('txv request OK.', status=status.HTTP_200_OK)
    return HttpResponse('Use GET request, please.', status=status.HTTP_400_BAD_REQUEST)


def get_txv(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        if key != 'Q8kGM1HfWz':
            HttpResponse('ERROR key.', status=status.HTTP_403_FORBIDDEN)
        
        pv_name = ''
        pv = request.GET.get('pv_code')
        dct_pv = {k : v for k, v in PV_VARS}  # Преобразуем кортеж кортежей в словарь
        if pv:
            try:
                pv = int(pv)
                pv_name = dct_pv.get(pv)
                if pv_name == None: raise ValueError('pv_code is undefined')
            except: raise ValueError('pv_code is not integer')
        else: raise ValueError('pv_code is absent')

        # Отметимся что бот был и определим разрешено ли работать
        obj_visit, _ = BotAccess.objects.get_or_create(name=f'Бот ТХВ {pv_name}')
        obj_visit.last_visit = datetime.now()
        yes_work = obj_visit.work
        obj_visit.save()

        if yes_work == True:
            tmp_txvs = TxV.objects.filter(pv_code=pv, status=0).order_by('-pub_date')[:5]
            # queryset в список словарей с преобразованием объекта модели в словарь
            txvs = [model_to_dict(row) for row in tmp_txvs]
            data = json.dumps(txvs)
            for txv in tmp_txvs:
                txv.status = 1
                txv.save()
        else: data = json.dumps([])
        
        return HttpResponse(data, content_type='application/json; charset=utf-8')
    return HttpResponse('Use GET request, please.', content_type='text/plain; charset=utf-8')


# Если вы добавите @csrf_exempt в начало вашего представления, вы в основном говорите,
# что ему не нужен токен. Это освобождение от безопасности, которое вы должны воспринимать всерьез.
@csrf_exempt
def set_txv_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        key = data.get('key')
        if key != 'Q8kGM1HfWz':
            return HttpResponse('ERROR key.', status=status.HTTP_403_FORBIDDEN)
        
        id_txv = data.get('id')
        new_available_connect = data.get('available_connect')
        new_tarifs_all = data.get('tarifs_all')
        new_pv_address = data.get('pv_address')
        new_status = data.get('status')
        new_bot_log = data.get('bot_log')
        try:
            ins_txv = TxV.objects.get(id=id_txv)
            if new_available_connect: ins_txv.available_connect = new_available_connect
            if new_tarifs_all: ins_txv.tarifs_all = new_tarifs_all
            if new_pv_address: ins_txv.pv_address = new_pv_address
            ins_txv.status = new_status
            if new_bot_log:
                bot_log = ins_txv.bot_log
                cur_time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
                bot_log += f'{cur_time}: {new_bot_log}\n'
                ins_txv.bot_log = bot_log
            ins_txv.save()
        except:
            return HttpResponse('ERROR data.', status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('New status OK.', status=status.HTTP_200_OK)
    return HttpResponse('Use POST request, please.', content_type='text/plain; charset=utf-8')
