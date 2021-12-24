from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm, ContactForm
from django.shortcuts import render


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def user_contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
    return render(request, 'contact.html', {'form': form})
