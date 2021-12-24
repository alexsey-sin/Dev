from django import forms


# функция-валидатор:
def validate_not_empty(value):
    if value == '':
        raise forms.ValidationError(
            'А кто поле будет заполнять, Пушкин?',
            params={'value': value},
        )
