from django.contrib import admin
from domconnect.models import DcCrmGlobVar, DcCrmLid, DcCashSEO
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
    def fl_title(self):
        return f'{self.title[:15]}...'
    fl_title.short_description = 'Титл'
    def fl_1571987728429(self):
        return f'{self.crm_1571987728429[:15]}...'
    fl_1571987728429.short_description = 'Провайдеры ДК'
    def fl_source_id(self):
        return f'{self.source_id[:15]}...'
    fl_source_id.short_description = 'Источник'
    def c_date(self):
        return self.create_date.strftime('%d.%m.%Y %H:%M')
    c_date.short_description = 'Создано'
    def m_date(self):
        return self.modify_date.strftime('%d.%m.%Y %H:%M')
    m_date.short_description = 'Изменено'

    list_display = ('id_lid', fl_title, 'status_id', c_date, m_date, fl_source_id, 'assigned_by_id',
        'crm_1493416385', 'crm_1499437861', 'crm_1580454770', 'crm_1534919765', fl_1571987728429,
        'crm_1592566018', 'crm_1493413514', 'crm_1492017494', 'crm_1492017736', 'crm_1498756113',
        'crm_1615982450', 'crm_1615982567', 'crm_1615982644', 'crm_1615982716', 'crm_1615982795',
        'crm_1640267556'
        )
    search_fields = ('id_lid', 'status_id',)
    list_filter = ('status_id', )
    empty_value_display = '-пусто-'
    date_hierarchy = 'create_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }
    list_per_page = 20


@admin.register(DcCashSEO)
class DcCashSEOAdmin(admin.ModelAdmin):
    def v_date(self):
        return self.val_date.strftime('%m.%Y')
    v_date.short_description = 'Период'

    list_display = (v_date, 'table', 'row', 'val')
    # list_display = [field.name for field in DcCashSEO._meta.get_fields()]
    # search_fields = ('change_date',)
    list_filter = ('val_date', 'table')
    empty_value_display = '-пусто-'
    date_hierarchy = 'val_date'
