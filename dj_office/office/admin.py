from django.contrib import admin
from office.models import GlobalVariable, MoexBOND
# from django.db import models
# from django.forms import NumberInput


@admin.register(GlobalVariable)
class GlobalVariableAdmin(admin.ModelAdmin):
    def v_str(self):
        if self.val_str: return f'{self.val_str[:20]}...'
    v_str.short_description = 'Строка'
    def v_descr(self):
        if self.descriptions: return f'{self.descriptions[:20]}...'
    v_descr.short_description = 'Текст'
    def v_date(self):
        if self.val_datetime: return self.val_datetime.strftime('%d.%m.%Y %H:%M')
    v_date.short_description = 'Дата'

    list_display = ('key', v_str, 'val_bool', 'val_int', 'val_decimal', v_date, v_descr)
    empty_value_display = '---'


@admin.register(MoexBOND)
class MoexBONDAdmin(admin.ModelAdmin):
    def mdate(self):
        return self.matdate.strftime('%d.%m.%Y')
    mdate.admin_order_field = 'matdate'
    mdate.short_description = 'Погашение'    

    list_display = ('secid', 'name', mdate, 'facevalue', 'couponfrequency', 'couponvalue', 'typename')
    search_fields = ('secid', )
    empty_value_display = '---'
    date_hierarchy = 'matdate'

    # list_filter = ('secid', 'name', 'matdate', 'facevalue', 'couponvalue', 'typename')
    # list_display = [field.name for field in MoexBOND._meta.get_fields()]
    # formfield_overrides = {
        # models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
        # # models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        # # models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    # }
