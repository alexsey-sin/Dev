from django.shortcuts import render
from icecream.models import icecream_db
from anfisa.models import friends_db
# Здесь импортируйте словарь friends_db из файла anfisa/models.py


def index(request):
    icecreams = ''
    # Создайте пустую переменную friends 
    friends = ''
    # Циклом обойдите словарь friends_db и сохраните все имена друзей в переменную friends
    for friend in friends_db:
        friends += (f'{friend}<br>')
    for i in range(len(icecream_db)):
        icecreams += (f'{icecream_db[i]["name"]} |' 
                    f'<a href="icecream/{i}/">  Узнать состав</a><br>')
    context = {
        'icecreams': icecreams,
        # Добавьте переменную friends в словарь context
        'friends': friends,
    }
    return render(request, 'homepage/index.html', context)
