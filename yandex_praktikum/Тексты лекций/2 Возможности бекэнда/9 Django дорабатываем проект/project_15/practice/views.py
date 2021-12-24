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
            return redirect('/thank-you/')
        return render(request, 'index.html', {'form': form})

    form = ExchangeForm()
    return render(request, 'index.html', {'form': form})


def thankyou(request):
    if request.method == 'GET':
        return render(request, 'thankyou.html')