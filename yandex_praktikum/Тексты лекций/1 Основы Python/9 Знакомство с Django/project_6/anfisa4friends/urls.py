from django.urls import include, path

urlpatterns = [
    path('', include('homepage.urls')),
    # Тут должен быть path(), который при обращении к главной странице
    # переадресует запрос в файл urls.py из директории homepage
]
