from django.http.request import HttpRequest
from django.http import HttpResponse
from rest_framework import status
from api.models import TxV
from django.forms.models import model_to_dict
import json
from datetime import datetime
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

            pv_code = request.GET.get('pv_code')
            if pv_code:
                try: txv.pv_code = int(pv_code)
                except: raise ValueError('pv_code is not integer')
            else: raise ValueError('pv_code is absent')

            login = request.GET.get('login')
            if login == None or len(login) == 0: raise ValueError('login is absent')
            txv.login = login

            password = request.GET.get('password')
            if password == None or len(password) == 0: raise ValueError('password is absent')
            txv.password = password
            
            login_2 = request.GET.get('login_2')
            if login_2: txv.login_2 = login_2
            
            password_2 = request.GET.get('password_2')
            if password_2: txv.password_2 = password_2
            
            id_lid = request.GET.get('id_lid')
            if id_lid: txv.id_lid = id_lid

            region = request.GET.get('region')
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

            apartment = request.GET.get('apartment')
            if apartment == None or len(apartment) == 0: raise ValueError('apartment is absent')
            txv.apartment = apartment

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
        
        pv = request.GET.get('pv_code')
        if pv:
            try: pv = int(pv)
            except: raise ValueError('pv_code is not integer')
        else: raise ValueError('pv_code is absent')
        tmp_txvs = TxV.objects.filter(pv_code=pv, status=0)
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
