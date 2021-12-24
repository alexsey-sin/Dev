forms.py

from django import forms
from .models import GENRE_CHOICES, CD


class ExchangeForm(forms.Form):
    name = forms.CharField(label="Ваше имя", max_length=100)
    email = forms.EmailField(label="Электронная почта для обратной связи")
    title = forms.CharField(label="Название альбома", max_length=100)
    artist = forms.CharField(label="Исполнитель", max_length=40)
    genre = forms.ChoiceField(label="Жанр", choices=GENRE_CHOICES)
    price = forms.DecimalField(label="Стоимость", required=False)
    comment = forms.CharField(label="Комментарий", widget=forms.Textarea, required=False)

    def clean_artist(self):
        artist = self.cleaned_data["artist"]

        if not CD.objects.filter(artist__iexact=artist).exists():
            raise forms.ValidationError(
                "Диски этого артиста мы не собираем!", params={"artist": artist},
            )

        return artist


views.py

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import ExchangeForm


def send_msg(email, name, title, artist, genre, price, comment):
    subject = f"Обмен {artist}-{title}"
    body = f"""Предложение на обмен диска от {name} ({email})

    Название: {title}
    Исполнитель: {artist}
    Жанр: {genre}
    Стоимость: {price}
    Комментарий: {comment}

    """
    send_mail(
        subject, body, email, ["admin@rockenrolla.net", ],
    )


def index(request):
    if request.method == 'POST':
        form = ExchangeForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            title = form.cleaned_data['title']
            artist = form.cleaned_data['artist']
            genre = form.cleaned_data['genre']
            price = form.cleaned_data['price']
            comment = form.cleaned_data['comment']
            send_msg(email, name, title, artist, genre, price, comment)
            return redirect('thankyou.html')
        return render(request, 'index.html', {'form': form})

    form = ExchangeForm()
    return render(request, 'index.html', {'form': form})


def thankyou(request):
    if request.method == 'GET':
        return render(request, 'thankyou.html')



index.html

<!DOCTYPE html>
<!-- Based on https://getbootstrap.com/docs/4.4/examples/pricing/ -->
<html lang="ru">
  <head>
    <meta charset="utf-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1, shrink-to-fit=no"
    />
    <title>Уголок рокнрольщика</title>

    <!-- Bootstrap core CSS -->
    <link
      rel="stylesheet"
      href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
      integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"
      crossorigin="anonymous"
    />
  </head>

  <body>
  <h1>Предложение обмена</h1>
  <p class="lead">
    Предложите мне свой диск на обмен.
  </p>
    <form method="post">
      {% csrf_token %}
      {{ form.as_p }}
      <button type="submit">Отправить</button>
    </form>
  </body>
</html>


urls.py

from django.urls import path

from . import views

urlpatterns = [
    path("thank-you/", views.thankyou, name="thankyou"),
    path("", views.index, name="index"),
]






из request получить пользователя
https://ru.stackoverflow.com/questions/997226/%D0%9A%D0%B0%D0%BA-%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%82%D0%B5%D0%BA%D1%83%D1%89%D0%B5%D0%B3%D0%BE-user%D0%B0-%D0%B2-views-py-django

request.user даст вам User объект, представляющий текущего пользователя. Если пользователь не вошел в систему, request.user будет установлен в экземпляр AnonymousUser. Вы можете различить их с is_authenticated(), например:

if request.user.is_authenticated():
    # Do something for authenticated users.
else:
    # Do something for anonymous users.



tests.py в папках posts и users
from django.test import TestCase

# Create your tests here.












