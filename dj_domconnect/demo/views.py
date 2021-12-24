# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="/login/")
def index(request):
    
    context = {}
    return render(request, 'demo/index.html', context)


@login_required(login_url="/login/")
def pages(request):
    context = {}
    template = 'demo/' + request.path.split('/')[-1]
    return render(request, template, context)
