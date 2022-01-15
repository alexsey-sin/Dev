from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model
# from django.http import HttpResponse
 
User = get_user_model()


@login_required(login_url="/login/")
def index(request):
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}

    # return render(request, 'app/index.html', context)
    return render(request, 'office/index.html', context)
    
