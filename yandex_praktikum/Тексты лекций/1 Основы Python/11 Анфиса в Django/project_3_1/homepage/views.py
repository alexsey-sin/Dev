import sys
from django.shortcuts import render
from icecream.models import icecream_db
from anfisa.models import friends_db
from anfisa.services import what_weather


def index(request):
    # если не объявить здесь пустые переменные,
    # то при GET-запросе блок if request.method == 'POST' не сработает
    # и эти переменные не будут созданы
    
    # В результате, при попытке передать несуществующие переменные в словарь context
    # программа сломается и сообщит об ошибке
    icecreams = ''
    friends = ''
    city_weather = ''
    friend_output = ''

    for friend in friends_db:
        # Около каждого имени вставляется radio button,
        # и теперь в форме кликом по кнопочке можно будет выбрать одного из друзей.
        friends += (f'<input type="radio" name="friend"'
                    f'required value="{friend}">{friend}<br>')

    for i in range(len(icecream_db)):
        icecreams += (f'{icecream_db[i]["name"]} | '
                    f'<a href="icecream/{i}/">Узнать состав</a><br>')

    # Проверьте, что тип запроса — POST
    if request.method == 'POST':
        # Извлеките из запроса имя друга и сохраните его в пременную selected_friend
        selected_friend = request.POST['friend']
        # Получите название города и сохраните его в переменную city
        city = friends_db[selected_friend]
        # Запросите погоду в городе city и сохраните её в переменную weather
        weather = what_weather(city)
        # В переменную friend_output запишите строку
        # "{Имя_друга}, тебе прислали мороженое!"
        friend_output = f"{selected_friend},тебе прислали мороженое!"
        # В переменную city_weather запишите строку
        # "Погода в городе {название_города}: {погода_в_городе}"
        city_weather = f"Погода в городе {city}:{weather}"

        # Этот блок кода выведет результаты работы view-функции в терминал тренажёра. 
        # После нажатия на кнопку "Проверить" будет автоматически отправлен тестовый запрос к проекту,
        # а результаты будут выведены в терминал, где вы сможете их увидеть
  
        print(f'имя друга: { selected_friend } \n'
               f'город: { city } \n'
               f'погода в городе: { weather } \n'
               f'текст для вывода: { friend_output } \n'
               f'погода для вывода: { city_weather } \n', 
               file=sys.stderr)

    context = {
        'icecreams': icecreams,
        'friends': friends,
        'friend_output': friend_output,
        'city_weather': city_weather,
    }
    return render(request, 'homepage/index.html', context)
