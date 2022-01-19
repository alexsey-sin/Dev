from django.contrib import admin
from domconnect.models import  DomconnectCrmLid, GlobalVariable
from django.db import models
from django.forms import NumberInput


@admin.register(DomconnectCrmLid)
class BidOnlimeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DomconnectCrmLid._meta.get_fields()]
    # search_fields = ('change_date',)
    # list_filter = ('id', 'phone', 'change_date')
    empty_value_display = '-пусто-'
    # date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(GlobalVariable)
class BidOnlimeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GlobalVariable._meta.get_fields()]
    # search_fields = ('change_date',)
    # list_filter = ('id', 'phone', 'change_date')
    empty_value_display = '-пусто-'
    # date_hierarchy = 'pub_date'
