from django import forms


def validate_not_empty(value):
    # проверка "а заполнено ли поле?"
    if value == '':
        raise forms.ValidationError(
            'Это поле не должно быть пустым!',
            params={'value': value},
        )
