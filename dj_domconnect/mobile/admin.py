from django.contrib import admin
from mobile.models import MobileNumber, MobileData


@admin.register(MobileNumber)
class MobileNumberAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in MobileNumber._meta.get_fields()]
    list_display = (
        'number',
        'opsos',
        'ats_except',
        'ats_except_min',
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
    search_fields = ('number',)
    list_filter = ('number',)
    # date_hierarchy = 'pub_date'
    empty_value_display = '---'


@admin.register(MobileData)
class MobileDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MobileData._meta.get_fields()]
    # list_display = (
    #     'number', 'mobile_available', 'mobile_packet', 'sms_available', 'sms_packet', 'balance', 'add_date')
    search_fields = ('number__number',)
    list_filter = ('number',)
    date_hierarchy = 'add_date'
    empty_value_display = '---'
# 'number__opsos', 

# admin.site.register(MobileNumber, MobileNumberAdmin)
# admin.site.register(MobileData, MobileDataAdmin)
