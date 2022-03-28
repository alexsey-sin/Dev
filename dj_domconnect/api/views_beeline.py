from django.http.request import HttpRequest
from django.http import HttpResponse
from rest_framework import status
from api.models import BidBeeline, BotVisit
from django.forms.models import model_to_dict
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
# import logging

# logger = logging.getLogger('django_log')

def set_bid_beeline(request):
    if request.method == 'GET':
        # cur_time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        # logger.info(cur_time)
        # logger.info(str(request.GET))
        try:
            key = request.GET.get('key')
            if key != 'Q8kGM1HfWz':
                return HttpResponse('ERROR key.', status=status.HTTP_400_BAD_REQUEST)
            bid = BidBeeline()

            partner_login = request.GET.get('partner_login')
            if partner_login == None or len(partner_login) == 0: raise ValueError('partner_login is absent')
            bid.partner_login = partner_login

            partner_workercode = request.GET.get('partner_workercode')
            if partner_workercode == None or len(partner_workercode) == 0: raise ValueError('partner_workercode is absent')
            bid.partner_workercode = partner_workercode

            partner_password = request.GET.get('partner_password')
            if partner_password == None or len(partner_password) == 0: raise ValueError('partner_password is absent')
            bid.partner_password = partner_password
            
            id_lid = request.GET.get('id_lid')
            if id_lid == None or len(id_lid) == 0: raise ValueError('id_lid is absent')
            bid.id_lid = id_lid

            city = request.GET.get('city')
            if city == None or len(city) == 0: raise ValueError('city is absent')
            bid.city = city

            street = request.GET.get('street')
            if street == None or len(street) == 0: raise ValueError('street is absent')
            bid.street = street
            
            house = request.GET.get('house')
            if house == None or len(house) == 0: raise ValueError('house is absent')
            bid.house = house

            apartment = request.GET.get('apartment')
            if apartment == None or not apartment.isdigit(): raise ValueError('apartment is absent or error')
            bid.apartment = apartment

            firstname = request.GET.get('firstname')
            if firstname and firstname.isalpha(): bid.firstname = firstname
            
            patronymic = request.GET.get('patronymic')
            if patronymic and patronymic.isalpha(): bid.patronymic = patronymic

            lastname = request.GET.get('lastname')
            if lastname and lastname.isalpha(): bid.lastname = lastname
            
            phone = request.GET.get('phone', None)
            if phone == None: raise ValueError('phone is absent')
            if not phone.isdigit(): raise ValueError('phone is not digit')
            if len(phone) != 11: raise ValueError('phone bad length')
            bid.phone = phone
            
            type_abonent = request.GET.get('type_abonent')  # приходит в любом случае строка
            if type_abonent:
                try: 
                    if type(type_abonent) == str: type_abonent = int(type_abonent)
                except:  raise ValueError('error parse int type_abonent')
                bid.type_abonent = type_abonent
            else: raise ValueError('not type_abonent')

            tarif = request.GET.get('tarif')
            if tarif == None or len(tarif) == 0: raise ValueError('tarif')
            bid.tarif = tarif
            
            dt_grafic = request.GET.get('dt_grafic')
            if dt_grafic: bid.dt_grafic = dt_grafic
            
            bid.status = 0
            bid.save()
        except ValueError as e:
            return HttpResponse(f'ERROR data. {e}', status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('bid request OK.', status=status.HTTP_200_OK)
    return HttpResponse('Use GET request, please.', status=status.HTTP_400_BAD_REQUEST)


def get_bid_beeline(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        if key != 'Q8kGM1HfWz':
            HttpResponse('ERROR key.', status=status.HTTP_403_FORBIDDEN)
        
        yes_work = False
        # Отметимся что бот был
        obj_visit, _ = BotVisit.objects.get_or_create(name=f'Бот автозаявки Билайн')
        obj_visit.last_visit = datetime.now()
        yes_work = obj_visit.work
        obj_visit.save()

        if yes_work == True:
            tmp_bids = BidBeeline.objects.filter(status=0)[:5]
            # queryset в список словарей с преобразованием объекта модели в словарь
            bids = [model_to_dict(row) for row in tmp_bids]
            data = json.dumps(bids)
            for bid in tmp_bids:
                bid.status = 1
                bid.save()
        else: data = json.dumps([])
        
        return HttpResponse(data, content_type='application/json; charset=utf-8')
    return HttpResponse('Use GET request, please.', content_type='text/plain; charset=utf-8')


# Если вы добавите @csrf_exempt в начало вашего представления, вы в основном говорите,
# что ему не нужен токен. Это освобождение от безопасности, которое вы должны воспринимать всерьез.
@csrf_exempt
def set_bid_beeline_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        key = data.get('key')
        if key != 'Q8kGM1HfWz':
            return HttpResponse('ERROR key.', status=status.HTTP_403_FORBIDDEN)
        
        id_bid = data.get('id')
        new_ctn_abonent = data.get('ctn_abonent')
        new_bid_number = data.get('bid_number')
        new_status = data.get('status')
        new_bot_log = data.get('bot_log')
        new_grafic_error = data.get('grafic_error')
        new_grafic_dop_info = data.get('grafic_dop_info')
        try:
            ins_bid = BidBeeline.objects.get(id=id_bid)
            ins_bid.status = new_status
            if new_ctn_abonent: ins_bid.ctn_abonent = new_ctn_abonent
            if new_bid_number: ins_bid.bid_number = new_bid_number
            if new_bot_log:
                bot_log = ins_bid.bot_log
                cur_time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
                bot_log += f'{cur_time}: {new_bot_log}\n'
                ins_bid.bot_log = bot_log
            if new_grafic_error: ins_bid.grafic_error = new_grafic_error
            if new_grafic_dop_info: ins_bid.grafic_dop_info = new_grafic_dop_info
            ins_bid.save()
        except:
            return HttpResponse('ERROR data.', status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('New status OK.', status=status.HTTP_200_OK)
    return HttpResponse('Use POST request, please.', content_type='text/plain; charset=utf-8')
