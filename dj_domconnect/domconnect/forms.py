from .models import DcSiteSEO
from django import forms


class DcSiteSEOForm(forms.ModelForm):
    class Meta:
        model = DcSiteSEO
        fields = (
            'num',
            'site',
            'name',
            'provider',
        )

