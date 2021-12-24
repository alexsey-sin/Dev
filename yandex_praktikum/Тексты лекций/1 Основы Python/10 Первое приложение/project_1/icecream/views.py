from django.http import HttpResponse
from .models import icecream_db


#def icecream_list(request):
#    return HttpResponse(f'Cписок сортов мороженого: {icecreams}')
def icecream_list(request):
    icecreams = ''
    for m in icecream_db:
        #listin.append(m['name'])
        icecreams += ':' + m['name'] + ':'
    #strin = '::'.join(listin)
    return HttpResponse(f'Cписок сортов мороженого{icecreams}')