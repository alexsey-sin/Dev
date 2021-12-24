from .models import Name, LizaPhrase, GermanPhrase
from django import forms


class NameForm(forms.ModelForm):
    class Meta:
        model = Name
        fields = ('text', 'sex', 'short_names',)


class LizaPhraseForm(forms.ModelForm):
    class Meta:
        model = LizaPhrase
        fields = ('text',)


class GermanPhraseForm(forms.ModelForm):
    class Meta:
        model = GermanPhrase
        fields = ('text',)
