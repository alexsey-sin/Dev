from django.shortcuts import render
from .models import icecream_db


def icecream_list(request):
    icecreams = ''
    for i in range(len(icecream_db)):
        # Исправьте строчку ниже
        icecreams += f"{icecream_db[i]['name']}<br>"
    # Используйте render в return
    context = {'icecreams':icecreams}
    return render(request, 'icecream/icecream-list.html', context)
