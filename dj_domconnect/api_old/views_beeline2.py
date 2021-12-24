from django.http.request import HttpRequest
from django.http import HttpResponse
from rest_framework import status
from api.models import BidBeeline2
from django.forms.models import model_to_dict
import json
from datetime import datetime


def set_bid_beeline2(request):
    if request.method == 'GET':
        try:
            key = request.GET.get('key')
            if key != 'Q8kGM1HfWz':
                return HttpResponse('ERROR key.', status=status.HTTP_400_BAD_REQUEST)
            bid = BidBeeline2()

            parther_key = request.GET.get('parther_key')
            if parther_key == None or len(parther_key) == 0: raise ValueError('parther_key is absent')
            bid.parther_key = parther_key

            client = request.GET.get('client_inn_name')
            if client == None or len(client) == 0: raise ValueError('client_inn_name is absent')
            client = client.split('/')
            if len(client) > 2: raise ValueError('client_inn_name contains many separators /')
            elif len(client) == 2:
                bid.client_inn = client[0].strip()
                bid.client_name = client[1].strip()
            else:  # нет разделителя /
                bid.client_inn = '000000000'
                bid.client_name = client[0].strip()

            id_lid = request.GET.get('id_lid')
            if id_lid == None or len(id_lid) == 0: raise ValueError('id_lid is absent')
            bid.id_lid = id_lid

            contact_name = request.GET.get('contact_name')
            if contact_name == None or len(contact_name) == 0: raise ValueError('contact_name is absent')
            bid.contact_name = contact_name

            phone = request.GET.get('phone', None)
            if phone == None: raise ValueError('phone is absent')
            if not phone.isdigit(): raise ValueError('phone is not digit')
            if len(phone) != 11: raise ValueError('phone bad length')
            bid.phone = phone

            email = request.GET.get('email')
            if email and len(email) > 0: bid.email = email
            
            comment = request.GET.get('comment')
            if comment and len(comment) > 0: bid.comment = comment

            products = request.GET.get('products')
            if products == None or len(products) == 0: raise ValueError('products is absent')
            bid.products = products
            
            bid.status = 0
            bid.save()
        except ValueError as e:
            return HttpResponse(f'ERROR data. {e}', status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('bid request OK.', status=status.HTTP_200_OK)
    return HttpResponse('Use GET request, please.', status=status.HTTP_400_BAD_REQUEST)


def get_bid_beeline2(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        if key != 'Q8kGM1HfWz':
            HttpResponse('ERROR key.', status=status.HTTP_403_FORBIDDEN)
        
        tmp_bids = BidBeeline2.objects.filter(status=0)
        # queryset в список словарей с преобразованием объекта модели в словарь
        bids = [model_to_dict(row) for row in tmp_bids]
        data = json.dumps(bids)
        for bid in tmp_bids:
            bid.status = 1
            bid.save()
        return HttpResponse(data, content_type='application/json; charset=utf-8')
    return HttpResponse('Use GET request, please.', content_type='text/plain; charset=utf-8')


def set_bid_beeline2_status(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        if key != 'Q8kGM1HfWz':
            return HttpResponse('ERROR key.', status=status.HTTP_403_FORBIDDEN)
        
        id_bid = request.GET.get('id')
        new_ctn_abonent = request.GET.get('ctn_abonent')
        new_bid_number = request.GET.get('bid_number')
        new_status = request.GET.get('status')
        new_bot_log = request.GET.get('bot_log')
        try:
            ins_bid = BidBeeline2.objects.get(id=id_bid)
            ins_bid.status = new_status
            if new_ctn_abonent: ins_bid.ctn_abonent = new_ctn_abonent
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
