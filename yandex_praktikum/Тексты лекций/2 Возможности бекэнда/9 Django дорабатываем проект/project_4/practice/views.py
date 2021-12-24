from django.shortcuts import render
from django.core.mail import send_mail

# Create your views here.


def send_msg(
    email, name, title, artist, date, genre, price, comment,
):
    subject = f"Обмен {artist}-{title} ({date})"
    body = f"""Предложение на обмен диска от {name} ({email})

    Название: {title}
    Исполнитель: {artist}
    Жанр: {genre}
    Дата выпуска альбома: {date}
    Стоимость: {price}
    Комментарий: {comment}

    """
    send_mail(
        subject, body, email, ["admin@rockenrolla.net",],
    )


def index(request):
    pass
