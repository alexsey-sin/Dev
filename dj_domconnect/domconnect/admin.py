from django.contrib import admin
from domconnect.models import DcCrmGlobVar, DcCrmLid
from django.db import models
from django.forms import NumberInput


@admin.register(DcCrmGlobVar)
class DcCrmGlobVarAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DcCrmGlobVar._meta.get_fields()]
    # search_fields = ('change_date',)
    # list_filter = ('id', 'phone', 'change_date')
    empty_value_display = '-пусто-'
    # date_hierarchy = 'pub_date'


@admin.register(DcCrmLid)
class DcCrmLidAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DcCrmLid._meta.get_fields()]
    # search_fields = ('change_date',)
    # list_filter = ('id', 'phone', 'change_date')
    empty_value_display = '-пусто-'
    # date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }
    list_per_page = 20
