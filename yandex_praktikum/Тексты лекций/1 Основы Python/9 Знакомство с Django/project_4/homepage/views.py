from django.http import HttpResponse


def index(request):
    return HttpResponse('Anfisa for Friends -- Hello, world! -- ¯\(°:°)/¯')
