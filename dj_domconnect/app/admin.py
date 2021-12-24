# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from app.models import LizaGroupPhrase, LizaPhrase, GermanGroupPhrase, File, GermanPhrase, Name


# class UserAdmin(admin.ModelAdmin):
    # list_display = (
        # 'username', 'first_name', 'last_name', 'email', 'date_joined','is_active', 'is_staff')
    # search_fields = ('username',)
    # list_filter = ('username',)
    # empty_value_display = '-пусто-'


class LizaGroupPhraseAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'num_group', 'priority')
    search_fields = ('text',)
    list_filter = ('text',)
    empty_value_display = '-пусто-'


class LizaPhraseAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'group', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('text',)
    empty_value_display = '-пусто-'


class FileInline(admin.TabularInline):
    model = File


class GermanGroupPhraseAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'num_group', 'priority')
    search_fields = ('text',)
    list_filter = ('text',)
    empty_value_display = '-пусто-'
    inlines = [
        FileInline,
    ]


class GermanPhraseAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'group', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('text',)
    empty_value_display = '-пусто-'


class NameAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'sex', 'pub_date', 'author', 'short_names')
    search_fields = ('text',)
    list_filter = ('text',)
    empty_value_display = '-пусто-'


# admin.site.register(User, UserAdmin)
admin.site.register(LizaGroupPhrase, LizaGroupPhraseAdmin)
admin.site.register(LizaPhrase, LizaPhraseAdmin)
admin.site.register(GermanGroupPhrase, GermanGroupPhraseAdmin)
admin.site.register(GermanPhrase, GermanPhraseAdmin)
admin.site.register(Name, NameAdmin)
