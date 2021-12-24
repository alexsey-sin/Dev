from django.http import HttpResponse
from .models import icecream_db


def icecream_list(request):
    icecreams = ''
    for i in range(len(icecream_db)):
        icecreams += f"{icecream_db[i]['name']} :: "
    return HttpResponse(f'Cписок сортов мороженого: {icecreams}')
