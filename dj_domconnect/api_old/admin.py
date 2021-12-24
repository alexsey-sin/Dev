from django.contrib import admin
from api.models import BidDomRu2, BidBeeline, BidMTS, BidBeeline2
from api.models import BidRostelecom2, BidRostelecom, BidDomRu, BidTtk, TxV
from api.models import TxvBeeline, TxvMts, TxvDomRu, TxvRostelecom
from django.db import models
from django.forms import NumberInput

@admin.register(BidDomRu2)
class BidDomRuAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'street', 'house', 'apartment', 'name',
        'phone', 'service_tv', 'service_net', 'service_phone', 'comment',
        'status', 'change_date', 'pub_date')
    search_fields = ('change_date',)
    list_filter = ('id', 'city','street', 'house', 'apartment', 'name',
        'phone', 'change_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
        # models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        # models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }


@admin.register(BidBeeline)
class BidBeelineAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BidBeeline._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('id', 'city','street', 'house', 'apartment', 'lastname',
        'phone', 'change_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(BidMTS)
class BidMTSlineAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BidMTS._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('id', 'city','street', 'house', 'apartment', 'firstname',
        'phone', 'change_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(BidBeeline2)
class BidBeeline2Admin(admin.ModelAdmin):
    list_display = [field.name for field in BidBeeline2._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('id', 'phone', 'change_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(BidRostelecom2)
class BidRostelecom2Admin(admin.ModelAdmin):
    list_display = [field.name for field in BidRostelecom2._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('id', 'phone', 'change_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(BidRostelecom)
class BidRostelecomAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BidRostelecom._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('id', 'phone', 'change_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(BidDomRu)
class BidDomRuAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BidDomRu._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('id', 'phone', 'change_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(BidTtk)
class BidTtkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BidTtk._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('id', 'phone', 'change_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(TxvBeeline)
class TxvBeelineAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TxvBeeline._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('id', 'change_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(TxvMts)
class TxvMtsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TxvMts._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('id', 'change_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(TxvDomRu)
class TxvDomRuAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TxvDomRu._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('id', 'change_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(TxvRostelecom)
class TxvRostelecomAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TxvRostelecom._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('id', 'change_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(TxV)
class TxVAdmin(admin.ModelAdmin):
    # Это как ограничить вывод длинного поля в списке
    def t_all30(self):
        verbose_name = 'Оператор',
        return u"%s..." % (self.tarifs_all[:30],)
    list_display = ['id', 'pv_code', 'id_lid', 'region', t_all30, 'pv_address', 'status', 'change_date', 'pub_date', 'bot_log']
    # list_display = [field.name for field in TxvRostelecom._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('id', 'id_lid', 'pv_code', 'change_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }
    # list_display = ['id', 'id_lid', 'region', t_all30, 'mts_address', 'status', 'change_date', 'pub_date', 'bot_log']
