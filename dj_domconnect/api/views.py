from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.http import require_http_methods
from api.serializers import PVResultSerializer
from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from app.models import LizaGroupPhrase, LizaPhrase, Name
from app.models import NdzGroupPhrase, NdzPhrase, PzGroupPhrase, PzPhrase
from api.models import BidDomRu2, BidBeeline, BidMTS, BidBeeline2, PV_VARS
from api.models import BidRostelecom2, BidRostelecom, BidDomRu, BidTtk
from api.models import  BidOnlime, BidMGTS, TxV, BotAccess, PVResult
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
import json
from datetime import datetime
from rest_framework import status


User = get_user_model()


def get_liza_phrases(request, num_group):
    if request.method == 'GET':
        group = get_object_or_404(LizaGroupPhrase, num_group=num_group)
        phrases = LizaPhrase.objects.filter(group=group).order_by('text')
        lst = []
        for phr in phrases:
            lst.append(phr.text)
        
        return HttpResponse('/(' + '|'.join(lst) + ')/')
    else:
        return HttpResponse('Use GET request, please.', content_type='text/plain; charset=utf-8')


def get_liza_files(request, filename):
    if request.method == 'GET':
        gr = filename.split('.')
        try:
            num_group = int(gr[0])
            print()
        except:
            return HttpResponse('Use numbers in the file name, please.', content_type='text/plain; charset=utf-8')
        try:
            extension = gr[1]
            if extension != 'php' or len(gr) != 2:
                return HttpResponse('file extension error.', content_type='text/plain; charset=utf-8')
        except:
            return HttpResponse('Use numbers in the file name, please.', content_type='text/plain; charset=utf-8')
        
        group = get_object_or_404(LizaGroupPhrase, num_group=num_group)
        phrases = LizaPhrase.objects.filter(group=group).order_by('text')
        lst = []
        for phr in phrases:
            lst.append(phr.text)
        content = '/(' + '|'.join(lst) + ')/'

        response = FileResponse(content, 'rb')
        response["Content-Type"] = 'text/plain; charset=utf-8'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        response['X-Sendfile'] = filename
        return response
    else:
        return HttpResponse('Use GET request, please.', content_type='text/plain; charset=utf-8')


def get_name_files(request, filename):
    if filename == None or len(filename) == 0:
        return HttpResponse('File name required.', content_type='text/plain; charset=utf-8')
    if request.method == 'GET':
        objs_names = Name.objects.all()
        out_data = {'names': []}

        for obj_name in objs_names:
            name = obj_name.text
            phrases = obj_name.short_names
            lst_phrases = phrases.split(',')
            if len(lst_phrases) == 0: continue
            for phr in lst_phrases:
                if phr == '': phr = name
                dct = {'phrase': phr, 'name': name}
                out_data['names'].append(dct)

            # out_data['names'].append({'phrase': 'Анга', 'name': 'Ангела'})
        data = json.dumps(out_data)
        response = FileResponse(data, 'rb')
        response["Content-Type"] = 'application/json; charset=utf-8'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        response['X-Sendfile'] = filename
        return response
    else:
        return HttpResponse('Use GET request, please.', content_type='text/plain; charset=utf-8')


def get_names(request):
    if request.method == 'GET':
        objs_names = Name.objects.all()
        out_data = {'names': []}

        for obj_name in objs_names:
            name = obj_name.text
            phrases = obj_name.short_names
            lst_phrases = phrases.split(',')
            if len(lst_phrases) == 0: continue
            for phr in lst_phrases:
                if phr == '': phr = name
                dct = {'phrase': phr, 'name': name}
                out_data['names'].append(dct)

        data = json.dumps(out_data)
        return HttpResponse(data, content_type='application/json; charset=utf-8')
    else:
        return HttpResponse('Use GET request, please.', content_type='text/plain; charset=utf-8')


def get_ndz_phrases(request, num_group):
    if request.method == 'GET':
        group = get_object_or_404(NdzGroupPhrase, num_group=num_group)
        phrases = NdzPhrase.objects.filter(group=group).order_by('text')
        lst = []
        for phr in phrases:
            lst.append(phr.text)
        
        return HttpResponse('/(' + '|'.join(lst) + ')/')
    else:
        return HttpResponse('Use GET request, please.', content_type='text/plain; charset=utf-8')


def get_pz_phrases(request, num_group):
    if request.method == 'GET':
        group = get_object_or_404(PzGroupPhrase, num_group=num_group)
        phrases = PzPhrase.objects.filter(group=group).order_by('text')
        lst = []
        for phr in phrases:
            lst.append(phr.text)
        
        return HttpResponse('/(' + '|'.join(lst) + ')/')
    else:
        return HttpResponse('Use GET request, please.', content_type='text/plain; charset=utf-8')

###############################################################################
###############################################################################
def get_bots_info(request, from_date):
    f_data = None
    try:
        f_data = datetime.strptime(from_date, '%d.%m.%Y')
    except Exception as e:
        return HttpResponse(str(e), content_type='text/plain; charset=utf-8')
    
    if f_data == None:
        return HttpResponse('Дата начала не задана.\nПример: get_bots_info/18.02.2022', content_type='text/plain; charset=utf-8')
    
    str_f_date = f_data.strftime('%d.%m.%Y %H:%M:%S')
    str_today = datetime.today().strftime('%d.%m.%Y %H:%M:%S')
    mess = f'Результаты работы ботов с {str_f_date} по {str_today}\n\n'
    pv_cort = (
        (BidDomRu2, 'BidDomRu2'),
        (BidBeeline, 'BidBeeline'),
        (BidMTS, 'BidMTS'),
        (BidBeeline2, 'BidBeeline2'),
        (BidRostelecom2, 'BidRostelecom2'),
        (BidRostelecom, 'BidRostelecom'),
        (BidDomRu, 'BidDomRu'),
        (BidTtk, 'BidTtk'),
        (BidOnlime, 'BidOnlime'),
        (BidMGTS, 'BidMGTS'),
    )
    for model, name in pv_cort:
        objs = model.objects.filter(pub_date__gte = f_data)
        all_cnt = objs.count()
        ok_cnt = objs.filter(status=3).count()  # Успешно отработано
        fil_cnt = objs.filter(status=2).count()  # Ошибка
        try:
            percent_ok = round((ok_cnt/all_cnt)*100, 2)
            percent_fil = round((fil_cnt/all_cnt)*100, 2)
        except: percent_ok = percent_fil = 0
        mess += f'BID {name} => Всего: {all_cnt} => Успешно: {percent_ok}%; Ошибок: {percent_fil}%\n'

    # objs = BidTtk.objects.all()
    # all_cnt = objs.count()
    # ok_cnt = objs.filter(status=3).count()
    # mess += f'BidTtk {ok_cnt}/{all_cnt}\n'

    pv_code = (
        (1, 'Билайн'),
        (2, 'ДомРу'),
        (3, 'МТС'),
        (4, 'Ростелеком'),
        (5, 'ТТК'),
        (6, 'ОнЛайм'),
        (7, 'МГТС'),
    )
    for code, name in pv_code:
        objs = TxV.objects.filter(pv_code=code, pub_date__gte = f_data)
        all_cnt = objs.count()
        ok_cnt = objs.filter(status=3).count()
        fil_cnt = objs.filter(status=2).count()  # Ошибка
        try:
            percent_ok = round((ok_cnt/all_cnt)*100, 2)
            percent_fil = round((fil_cnt/all_cnt)*100, 2)
        except: percent_ok = percent_fil = 0
        mess += f'TXV {name} => Всего: {all_cnt} => Успешно: {percent_ok}%; Ошибок: {percent_fil}%\n'


    return HttpResponse(mess, content_type='text/plain; charset=utf-8')

def get_bots_vizit(request):
    if request.method == 'GET':
        try:
            key = request.GET.get('key')
            if key != 'Q8kGM1HfWz': raise ValueError('ERROR key.')
            
            obj_bots_vizit = BotAccess.objects.all()
            lst_bots_vizit = [model_to_dict(row) for row in obj_bots_vizit]
            data = json.dumps(lst_bots_vizit, default=str, indent=1)
        except ValueError as e:
            return HttpResponse(f'ERROR: {e}', status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse(data, content_type='application/json; charset=utf-8', status=status.HTTP_200_OK)

def get_lk_access(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        if key != 'Q8kGM1HfWz':
            HttpResponse('ERROR key.', status=status.HTTP_403_FORBIDDEN)

        lk_name = request.GET.get('lk_name')
        yes_work = False
        # Отметимся что бот был
        obj_visit, _ = BotAccess.objects.get_or_create(name=f'Парсер ЛК {lk_name}')
        obj_visit.last_visit = datetime.now()
        yes_work = obj_visit.work
        obj_visit.save()

        if yes_work == True:
            access = {'login': obj_visit.login, 'password': obj_visit.password}
            data = json.dumps(access)
        else: data = json.dumps({})

        return HttpResponse(data, content_type='application/json; charset=utf-8')
    return HttpResponse('Use GET request, please.', content_type='text/plain; charset=utf-8')
###############################################################################
###############################################################################
class SetPvResultViewSet(viewsets.ModelViewSet):
    queryset = PVResult.objects.all()
    permission_classes = [IsAuthenticated,]  # IsAuthenticated
    serializer_class = PVResultSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)


@require_http_methods(['GET',])
def get_pv_result(request, pv_code, from_date):
    dct_pv = {k : v for k, v in PV_VARS}  # Преобразуем кортеж кортежей в словарь

    try:
        f_data = datetime.strptime(from_date, '%d.%m.%Y')
    except Exception as e:
        return HttpResponse(f'Ошибка преобразования даты \"{from_date}\"', content_type='text/plain; charset=utf-8')
    
    if pv_code not in dct_pv:
        return HttpResponse(f'Код провайдера \"{pv_code}\" не корректен', content_type='text/plain; charset=utf-8')
    
    objs = PVResult.objects.filter(pv_code=pv_code, pub_date=f_data)
    
    str_f_date = f_data.strftime('%d.%m.%Y %H:%M:%S')
    str_today = datetime.today().strftime('%d.%m.%Y %H:%M:%S')
    mess = f'Результат работы бота ПВ {str_f_date} {from_date}\n\n'


    print(pv_code, from_date)
    # key = request.GET.get('key')
    # if key != 'Q8kGM1HfWz':
    #     HttpResponse('ERROR key.', status=status.HTTP_403_FORBIDDEN)

    # lk_name = request.GET.get('lk_name')
    # yes_work = False
    # # Отметимся что бот был
    # obj_visit, _ = BotAccess.objects.get_or_create(name=f'Парсер ЛК {lk_name}')
    # obj_visit.last_visit = datetime.now()
    # yes_work = obj_visit.work
    # obj_visit.save()

    # if yes_work == True:
    #     access = {'login': obj_visit.login, 'password': obj_visit.password}
    #     data = json.dumps(access)
    # else: data = json.dumps({})

    return HttpResponse('Уже в избранном',
        status=status.HTTP_208_ALREADY_REPORTED,
        content_type='text/plain; charset=utf-8'
    )

