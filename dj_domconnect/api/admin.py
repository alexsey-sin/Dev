from django.contrib import admin
from api.models import BidDomRu2, BidBeeline, BidMTS, BidBeeline2
from api.models import BidRostelecom2, BidRostelecom, BidDomRu, BidTtk
from api.models import  BidOnlime, BidMGTS, TxV, BotVisit
from django.db import models
from django.forms import NumberInput


@admin.register(BotVisit)
class BotVisitAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_visit')
    search_fields = ('name',)
    list_filter = ('last_visit', 'name')
    empty_value_display = '-пусто-'
    date_hierarchy = 'last_visit'


@admin.register(BidDomRu2)
class BidDomRuAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'street', 'house', 'apartment', 'name',
        'phone', 'service_tv', 'service_net', 'service_phone', 'comment',
        'status', 'change_date', 'pub_date')
    list_filter = ('status', 'pub_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
        # models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        # models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }


@admin.register(BidBeeline)
class BidBeelineAdmin(admin.ModelAdmin):
    def address(self):
        return f'{self.city}, {self.street}, {self.house}'
    address.short_description = 'Адрес'
    def field_FIO(self):
        return f'{self.firstname} {self.patronymic} {self.lastname}'
    field_FIO.short_description = 'ФИО'
    def gr_error(self):
        return f'{self.grafic_error[:20]}...'
    gr_error.short_description = 'Ошибки графика'
    def gr_dop_info(self):
        return f'{self.grafic_dop_info[:20]}...'
    gr_dop_info.short_description = 'График Доп инфо'
    def b_log(self):
        return f'{self.bot_log[:20]}...'
    b_log.short_description = 'Лог'

    list_display = ['id_lid', address, field_FIO, 'status', 'pub_date', gr_dop_info, gr_error, b_log]
    search_fields = ('id_lid',)  # Верхнее поле "Найти"
    list_filter = ('status', 'pub_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }
    list_per_page = 20  # количество объектов на одной странице при отображении списка объектов. По умолчанию равно 100.


@admin.register(BidMTS)
class BidMTSlineAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BidMTS._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('status', 'pub_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(BidBeeline2)
class BidBeeline2Admin(admin.ModelAdmin):
    def b_log(self):
        return f'{self.bot_log[:20]}...'
    b_log.short_description = 'Лог'
    list_display = ['id_lid', 'status', 'client_name', 'contact_name', 'pub_date', b_log, 'phone']
    search_fields = ('id_lid',)  # Верхнее поле "Найти"
    list_filter = ('status', 'pub_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(BidRostelecom2)
class BidRostelecom2Admin(admin.ModelAdmin):
    def address(self):
        return f'{self.address[:20]}'
    address.short_description = 'Адрес'
    def field_FIO(self):
        return f'{self.firstname} {self.patronymic} {self.lastname}'
    def b_log(self):
        return f'{self.bot_log[:20]}...'
    b_log.short_description = 'Лог'
    list_display = ['id_lid', 'status', address, field_FIO, 'pub_date', b_log, 'phone']
    search_fields = ('id_lid',)  # Верхнее поле "Найти"
    list_filter = ('status', 'pub_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(BidRostelecom)
class BidRostelecomAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BidRostelecom._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('status', 'pub_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(BidDomRu)
class BidDomRuAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BidDomRu._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('status', 'pub_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(BidTtk)
class BidTtkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BidTtk._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('status', 'pub_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(BidOnlime)
class BidOnlimeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BidOnlime._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('status', 'pub_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(BidMGTS)
class BidMGTSAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BidMGTS._meta.get_fields()]
    search_fields = ('change_date',)
    list_filter = ('status', 'pub_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }


@admin.register(TxV)
class TxVAdmin(admin.ModelAdmin):
    # Это как ограничить вывод длинного поля в списке
    def tarifs(self):
        return u"%s..." % (self.tarifs_all[:30],)
    def connect(self):
        return u"%s..." % (self.available_connect[:30],)
    def logs(self):
        return u"%s..." % (self.bot_log[:30],)
    list_display = ['id', 'pv_code', 'id_lid', 'region', 'city', connect, tarifs, 'pv_address', 'status', 'change_date', 'pub_date', logs]
    # list_display = [field.name for field in TxvRostelecom._meta.get_fields()]
    search_fields = ('id_lid',)
    list_filter = ('pv_code', 'status', 'pub_date')
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size':'150'})},
    }
