from django.shortcuts import render
from icecream.models import icecream_db
# Здесь импортируйте icecream_db из файла models приложения icecream


def index(request):
    icecreams = ''
    for i in range(len(icecream_db)):
        # Измените строку, добавляемую к icecreams
        icecreams += f"{icecream_db[i]['name']}  |  <a href='icecream/{i}/'>Узнать состав</a><br>"        
    context = {
        'icecreams': icecreams,
    }
    return render(request, 'homepage/index.html', context)
