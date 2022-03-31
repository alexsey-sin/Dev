from django.http import HttpResponse
from rest_framework import status
from api.models import BidTtk, BotVisit
from django.forms.models import model_to_dict
import json
from datetime import datetime
# import logging

# logger = logging.getLogger('django_log')

def set_bid_ttk(request):
    if request.method == 'GET':
        # cur_time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        # logger.info(cur_time)
        # logger.info(str(request.GET))
        try:
            key = request.GET.get('key')
            if key != 'Q8kGM1HfWz':
                return HttpResponse('ERROR key.', status=status.HTTP_400_BAD_REQUEST)
            bid = BidTtk()

            # Возьмем доступы
            obj_visit, _ = BotVisit.objects.get_or_create(name='Бот автозаявки ТТК')
            bid.login = obj_visit.login
            bid.password = obj_visit.password

            id_lid = request.GET.get('id_lid')
            if id_lid == None or len(id_lid) == 0: raise ValueError('id_lid is absent')
            bid.id_lid = id_lid

            firstname = request.GET.get('firstname')
            if firstname and firstname.isalpha() and len(firstname) > 2:
                bid.firstname = firstname.capitalize()
            
            patronymic = request.GET.get('patronymic')
            if patronymic and patronymic.isalpha() and len(patronymic) > 2:
                bid.patronymic = patronymic.capitalize()

            lastname = request.GET.get('lastname')
            if lastname and lastname.isalpha() and len(lastname) > 2:
                bid.lastname = lastname.capitalize()
            
            phone = request.GET.get('phone', None)
            if phone == None: raise ValueError('phone is absent')
            if not phone.isdigit(): raise ValueError('phone is not digit')
            if len(phone) != 11: raise ValueError('phone bad length')
            bid.phone = phone

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
            if apartment == None or len(apartment) == 0: raise ValueError('apartment is absent')
            bid.apartment = apartment

            general_package = request.GET.get('general_package')
            if general_package: bid.general_package = general_package
            
            service_internet = request.GET.get('service_internet')
            if service_internet: bid.service_internet = service_internet
            
            service_tv = request.GET.get('service_tv')
            if service_tv: bid.service_tv = service_tv
            
            equipment = request.GET.get('equipment')
            if equipment: bid.equipment = equipment
            
            comment = request.GET.get('comment')
            if comment: bid.comment = comment

            bid.status = 0
            bid.save()
        except ValueError as e:
            return HttpResponse(f'ERROR data. {e}', status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('bid request OK.', status=status.HTTP_200_OK)
    return HttpResponse('Use GET request, please.', status=status.HTTP_400_BAD_REQUEST)


def get_bid_ttk(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        if key != 'Q8kGM1HfWz':
            HttpResponse('ERROR key.', status=status.HTTP_403_FORBIDDEN)
        
        yes_work = False
        # Отметимся что бот был
        obj_visit, _ = BotVisit.objects.get_or_create(name='Бот автозаявки ТТК')
        obj_visit.last_visit = datetime.now()
        yes_work = obj_visit.work
        obj_visit.save()

        if yes_work == True:
            tmp_bids = BidTtk.objects.filter(status=0).order_by('-pub_date')[:5]
            # queryset в список словарей с преобразованием объекта модели в словарь
            bids = [model_to_dict(row) for row in tmp_bids]
            data = json.dumps(bids)
            for bid in tmp_bids:
                bid.status = 1
                bid.save()
        else: data = json.dumps([])

        return HttpResponse(data, content_type='application/json; charset=utf-8')
    return HttpResponse('Use GET request, please.', content_type='text/plain; charset=utf-8')


def set_bid_ttk_status(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        if key != 'Q8kGM1HfWz':
            return HttpResponse('ERROR key.', status=status.HTTP_403_FORBIDDEN)
        
        id_bid = request.GET.get('id')
        new_bid_number = request.GET.get('bid_number')
        new_status = request.GET.get('status')
        new_bot_log = request.GET.get('bot_log')
        try:
            ins_bid = BidTtk.objects.get(id=id_bid)
            ins_bid.status = new_status
            if new_bid_number: ins_bid.bid_number = new_bid_number
            if new_bot_log:
                bot_log = ins_bid.bot_log
                cur_time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
                bot_log += f'{cur_time}: {new_bot_log}\n'
                ins_bid.bot_log = bot_log
            ins_bid.save()
        except:
            return HttpResponse('ERROR data.', status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('New status OK.', status=status.HTTP_200_OK)
    return HttpResponse('Use GET request, please.', content_type='text/plain; charset=utf-8')
