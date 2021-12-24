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
