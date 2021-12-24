from django.http.request import HttpRequest
from django.http import HttpResponse
from rest_framework import status
from api.models import TxvBeeline
from django.forms.models import model_to_dict
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
# import logging

# logger = logging.getLogger('django_log')

def set_txv_beeline(request):
    if request.method == 'GET':
        # cur_time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        # logger.info(cur_time)
        # logger.info(str(request.GET))
        try:
            key = request.GET.get('key')
            if key != 'Q8kGM1HfWz':
                return HttpResponse('ERROR key.', status=status.HTTP_400_BAD_REQUEST)
            txv = TxvBeeline()

            partner_login = request.GET.get('partner_login')
            if partner_login == None or len(partner_login) == 0: raise ValueError('partner_login is absent')
            txv.partner_login = partner_login

            partner_workercode = request.GET.get('partner_workercode')
            if partner_workercode == None or len(partner_workercode) == 0: raise ValueError('partner_workercode is absent')
            txv.partner_workercode = partner_workercode

            partner_password = request.GET.get('partner_password')
            if partner_password == None or len(partner_password) == 0: raise ValueError('partner_password is absent')
            txv.partner_password = partner_password
            
            id_lid = request.GET.get('id_lid')
            if id_lid == None or len(id_lid) == 0: raise ValueError('id_lid is absent')
            txv.id_lid = id_lid

            city = request.GET.get('city')
            if city == None or len(city) == 0: raise ValueError('city is absent')
            txv.city = city

            street = request.GET.get('street')
            if street == None or len(street) == 0: raise ValueError('street is absent')
            txv.street = street
            
            house = request.GET.get('house')
            if house == None or len(house) == 0: raise ValueError('house is absent')
            txv.house = house

            apartment = request.GET.get('apartment')
            if apartment: txv.apartment = apartment

            date_connect = request.GET.get('date_connect')
            if date_connect: txv.date_connect = date_connect

            txv.status = 0
            txv.save()
        except ValueError as e:
            return HttpResponse(f'ERROR data. {e}', status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('txv request OK.', status=status.HTTP_200_OK)
    return HttpResponse('Use GET request, please.', status=status.HTTP_400_BAD_REQUEST)


def get_txv_beeline(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        if key != 'Q8kGM1HfWz':
            HttpResponse('ERROR key.', status=status.HTTP_403_FORBIDDEN)
        
        tmp_txvs = TxvBeeline.objects.filter(status=0)
        # queryset в список словарей с преобразованием объекта модели в словарь
        txvs = [model_to_dict(row) for row in tmp_txvs]
        data = json.dumps(txvs)
        for txv in tmp_txvs:
            txv.status = 1
            txv.save()
        return HttpResponse(data, content_type='application/json; charset=utf-8')
    return HttpResponse('Use GET request, please.', content_type='text/plain; charset=utf-8')


# Если вы добавите @csrf_exempt в начало вашего представления, вы в основном говорите,
# что ему не нужен токен. Это освобождение от безопасности, которое вы должны воспринимать всерьез.
@csrf_exempt
def set_txv_beeline_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        key = data.get('key')
        if key != 'Q8kGM1HfWz':
            return HttpResponse('ERROR key.', status=status.HTTP_403_FORBIDDEN)
        
        id_txv = data.get('id')
        new_info_restrictions = data.get('info_restrictions')
        new_tarifs_all = data.get('tarifs_all')
        new_contract = data.get('contract')
        new_find_date = data.get('find_date')
        new_available_first_date_connect = data.get('available_first_date_connect')
        new_available_timeslot = data.get('available_timeslot')
        new_status = data.get('status')
        new_bot_log = data.get('bot_log')
        try:
            ins_txv = TxvBeeline.objects.get(id=id_txv)
            if new_info_restrictions: ins_txv.info_restrictions = new_info_restrictions
            if new_tarifs_all: ins_txv.tarifs_all = new_tarifs_all
            if new_contract: ins_txv.contract = new_contract
            if new_find_date: ins_txv.find_date = new_find_date
            if new_available_first_date_connect: ins_txv.available_first_date_connect = new_available_first_date_connect
            if new_available_timeslot: ins_txv.available_timeslot = new_available_timeslot
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
