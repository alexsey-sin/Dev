from django.http import HttpResponse
from rest_framework import status
from api.models import BidRostelecom, BotAccess
from django.forms.models import model_to_dict
import json
from datetime import datetime
# import logging

# logger = logging.getLogger('django_log')

def set_bid_rostelecom(request):
    if request.method == 'GET':
        # cur_time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        # logger.info(cur_time)
        # logger.info(str(request.GET))
        try:
            key = request.GET.get('key')
            if key != 'Q8kGM1HfWz':
                return HttpResponse('ERROR key.', status=status.HTTP_400_BAD_REQUEST)
            bid = BidRostelecom()

            # Возьмем доступы
            obj_visit, _ = BotAccess.objects.get_or_create(name='Бот автозаявки Ростелеком')
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

            region = request.GET.get('region')
            if region == None or len(region) == 0: raise ValueError('region is absent')
            bid.region = region

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
            
            service_home_internet = request.GET.get('service_home_internet')
            if service_home_internet: bid.service_home_internet = service_home_internet
            
            service_smart_house = request.GET.get('service_smart_house')
            if service_smart_house: bid.service_smart_house = service_smart_house
            
            service_smart_intercom = request.GET.get('service_smart_intercom')
            if service_smart_intercom: bid.service_smart_intercom = service_smart_intercom
            
            service_interactive_tv = request.GET.get('service_interactive_tv')
            if service_interactive_tv: bid.service_interactive_tv = service_interactive_tv
            
            service_wink_tv_online = request.GET.get('service_wink_tv_online')
            if service_wink_tv_online: bid.service_wink_tv_online = service_wink_tv_online
            
            service_home_phone = request.GET.get('service_home_phone')
            if service_home_phone: bid.service_home_phone = service_home_phone
            
            service_mobile_connection = request.GET.get('service_mobile_connection')
            if service_mobile_connection: bid.service_mobile_connection = service_mobile_connection
            
            service_iptv_packets = request.GET.get('service_iptv_packets')
            if service_iptv_packets: bid.service_iptv_packets = service_iptv_packets
            
            comment = request.GET.get('comment')
            if comment: bid.comment = comment

            bid.status = 0
            bid.save()
        except ValueError as e:
            return HttpResponse(f'ERROR data. {e}', status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('bid request OK.', status=status.HTTP_200_OK)
    return HttpResponse('Use GET request, please.', status=status.HTTP_400_BAD_REQUEST)


def get_bid_rostelecom(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        if key != 'Q8kGM1HfWz':
            HttpResponse('ERROR key.', status=status.HTTP_403_FORBIDDEN)
        
        yes_work = False
        # Отметимся что бот был
        obj_visit, _ = BotAccess.objects.get_or_create(name='Бот автозаявки Ростелеком')
        obj_visit.last_visit = datetime.now()
        yes_work = obj_visit.work
        obj_visit.save()

        if yes_work == True:
            tmp_bids = BidRostelecom.objects.filter(status=0).order_by('-pub_date')[:5]
            # queryset в список словарей с преобразованием объекта модели в словарь
            bids = [model_to_dict(row) for row in tmp_bids]
            data = json.dumps(bids)
            for bid in tmp_bids:
                bid.status = 1
                bid.save()
        else: data = json.dumps([])

        return HttpResponse(data, content_type='application/json; charset=utf-8')
    return HttpResponse('Use GET request, please.', content_type='text/plain; charset=utf-8')


def set_bid_rostelecom_status(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        if key != 'Q8kGM1HfWz':
            return HttpResponse('ERROR key.', status=status.HTTP_403_FORBIDDEN)
        
        id_bid = request.GET.get('id')
        new_bid_number = request.GET.get('bid_number')
        new_status = request.GET.get('status')
        new_bot_log = request.GET.get('bot_log')
        try:
            ins_bid = BidRostelecom.objects.get(id=id_bid)
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
