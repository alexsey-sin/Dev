from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Contact


User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "email")


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'body')

    # метод-валидатор для поля subject
    def clean_subject(self):
        data = self.cleaned_data['subject']

        # если пользователь не поблагодарил администратора
        # - считаем это ошибкой
        if "спасибо" not in data.lower():
            raise forms.ValidationError("Вы обязательно",
                                        "должны нас поблагодарить!")

        # метод-валидатор обязательно должен вернуть очищенные данные,
        # даже если не изменил их
        return data
