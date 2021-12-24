from .models import MobileNumber
from django import forms


class MobileNumberForm(forms.ModelForm):
    class Meta:
        model = MobileNumber
        fields = (
            'type_channel',
            'type_trunk',
            'type_tariff',
            'name_tariff',
            'tariff_description',
            'oatc_batc_description',
            'unlimited_on_net',
            'unlimited_on_net_not_consume_package',
            'package_cost',
            'oatc_batc_cost',
            'mobile_packet',
            'sms_packet',
            'active',
            'comment',
        )

