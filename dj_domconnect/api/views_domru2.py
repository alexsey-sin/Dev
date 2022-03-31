from django.http.request import HttpRequest
from django.http import HttpResponse, FileResponse
from rest_framework import status
from api.models import BidDomRu2, BotAccess
from django.forms.models import model_to_dict
import json
from datetime import datetime


# @csrf_exempt
def set_bid_domru2(request):
    if request.method == 'GET':
        try:
            key = request.GET.get('key')
            if key != 'Q8kGM1HfWz':
                return HttpResponse('ERROR key.', status=status.HTTP_400_BAD_REQUEST)
            bid = BidDomRu2()
            city = request.GET.get('city')
            if city == None: raise ValueError
            bid.city = city
            street = request.GET.get('street')
            if street == None: raise ValueError
            bid.street = street
            house = request.GET.get('house')
            if house == None: raise ValueError
            bid.house = house
            bid.apartment = request.GET.get('apartment')
            bid.name = request.GET.get('name')
            phone = request.GET.get('phone')
            if not phone.isdigit() or len(phone) != 11:
                raise ValueError
            bid.phone = phone
            bid.service_tv = request.GET.get('service_tv')
            bid.service_net = request.GET.get('service_net')
            bid.service_phone = request.GET.get('service_phone')
            bid.comment = request.GET.get('comment')
            bid.status = 0
            bid.save()
        except:
            return HttpResponse('ERROR data.', status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('bid request OK.', status=status.HTTP_200_OK)
    return HttpResponse('Use GET request, please.', status=status.HTTP_400_BAD_REQUEST)


def get_bid_domru2(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        if key != 'Q8kGM1HfWz':
            HttpResponse('ERROR key.', status=status.HTTP_403_FORBIDDEN)
        
        yes_work = False
        # Отметимся что бот был
        obj_visit, _ = BotAccess.objects.get_or_create(name='Бот автозаявки ДомРу_ЮЛ')
        obj_visit.last_visit = datetime.now()
        yes_work = obj_visit.work
        obj_visit.save()

        if yes_work == True:
            tmp_bids = BidDomRu2.objects.filter(status=0).order_by('-pub_date')[:5]
            # queryset в список словарей с преобразованием объекта модели в словарь
            bids = [model_to_dict(row) for row in tmp_bids]
            data = json.dumps(bids)
            for bid in tmp_bids:
                bid.status = 1
                bid.save()
        else: data = json.dumps([])

        return HttpResponse(data, content_type='application/json; charset=utf-8')
    return HttpResponse('Use GET request, please.', content_type='text/plain; charset=utf-8')


def set_bid_domru2_status(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        if key != 'Q8kGM1HfWz':
            return HttpResponse('ERROR key.', status=status.HTTP_403_FORBIDDEN)
        
        id_bid = request.GET.get('id')
        new_status = request.GET.get('status')
        try:
            ins_bid = BidDomRu2.objects.get(id=id_bid)
            ins_bid.status = new_status
            ins_bid.save()
        except:
            return HttpResponse('ERROR data.', status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('New status OK.', status=status.HTTP_200_OK)
    return HttpResponse('Use GET request, please.', content_type='text/plain; charset=utf-8')

###############################################################################
###############################################################################
