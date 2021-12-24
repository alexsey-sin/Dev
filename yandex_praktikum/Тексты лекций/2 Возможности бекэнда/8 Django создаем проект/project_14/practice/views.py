# from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):

    # Доступные тарифные планы
    plans = [
        {
            "name": "Бесплатно",
            "price": "0",
            "options": {"users": 10, "space": 10, "support": "Почтовая рассылка"},
        },
        {
            "name": "Профессиональный",
            "price": "49",
            "options": {"users": 50, "space": 100, "support": "Телефон и email"},
        },
        {
            "name": "Корпоративный",
            "price": "99",
            "options": {"users": 100, "space": 500, "support": "Персональный менеджер"},
        },
    ]
    
    context = {'plans': plans}
    # return HttpResponse("Hello, world!")
    return render(request, 'index.html', context)
