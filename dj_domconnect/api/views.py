from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from app.models import LizaGroupPhrase, LizaPhrase, Name
from app.models import NdzGroupPhrase, NdzPhrase, PzGroupPhrase, PzPhrase
from api.models import BidDomRu2, BidBeeline, BidMTS, BidBeeline2
from api.models import BidRostelecom2, BidRostelecom, BidDomRu, BidTtk
from api.models import  BidOnlime, BidMGTS, TxV
from django.contrib.auth import get_user_model
import json


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
def get_bots_info(request):
    mess = ''

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
        objs = model.objects.all()
        all_cnt = objs.count()
        ok_cnt = objs.filter(status=3).count()
        mess += f'BID {name} => {ok_cnt}/{all_cnt}\n'

    # objs = BidTtk.objects.all()
    # all_cnt = objs.count()
    # ok_cnt = objs.filter(status=3).count()
    # mess += f'BidTtk {ok_cnt}/{all_cnt}\n'

    # objs = BidOnlime.objects.all()
    # all_cnt = objs.count()
    # ok_cnt = objs.filter(status=3).count()
    # mess += f'BidOnlime {ok_cnt}/{all_cnt}\n'

    # objs = BidMGTS.objects.all()
    # all_cnt = objs.count()
    # ok_cnt = objs.filter(status=3).count()
    # mess += f'BidMGTS {ok_cnt}/{all_cnt}\n'

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
        objs = TxV.objects.filter(pv_code=code)
        all_cnt = objs.count()
        ok_cnt = objs.filter(status=3).count()
        mess += f'TXV {name} => {ok_cnt}/{all_cnt}\n'


    return HttpResponse(mess, content_type='text/plain; charset=utf-8')