from django.contrib import admin
from office.models import GlobalVariable, MoexBOND
# from django.db import models
# from django.forms import NumberInput


@admin.register(GlobalVariable)
class GlobalVariableAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GlobalVariable._meta.get_fields()]
    empty_value_display = '-пусто-'


@admin.register(MoexBOND)
class MoexBONDAdmin(admin.ModelAdmin):
    list_display = ('id', 'secid', 'mdate', 'facevalue',
        'couponfrequency', 'couponvalue', 'typename')
    # list_display = [field.name for field in MoexBOND._meta.get_fields()]
    search_fields = ('secid', 'name', 'matdate', 'facevalue', 'couponvalue', 'typename')
    # list_filter = ('secid', 'name', 'matdate', 'facevalue', 'couponvalue', 'typename')
    empty_value_display = '-пусто-'
    date_hierarchy = 'matdate'
    def mdate(self, obj):
        return obj.matdate.strftime('%d.%m.%Y')
        mdate.admin_order_field = 'matdate'
        mdate.short_description = 'Погашение'    

    # formfield_overrides = {
        # models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
        # # models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        # # models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    # }
