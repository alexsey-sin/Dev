from django.shortcuts import render
# Здесь импортируйте функцию render из файла django.shortcuts


def index(request):
    return render(request, 'homepage/index.html')
