from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from app.models import LizaGroupPhrase, LizaPhrase, Name
from app.models import NdzGroupPhrase, NdzPhrase, PzGroupPhrase, PzPhrase
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
    mess = 'please, please, please...'

    return HttpResponse(mess, content_type='text/plain; charset=utf-8')