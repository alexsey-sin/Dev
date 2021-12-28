# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from app.models import LizaGroupPhrase, LizaPhrase, GermanGroupPhrase, File, GermanPhrase, Name
from app.models import NdzGroupPhrase, NdzPhrase, PzGroupPhrase, PzPhrase


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
    # list_display = (
        # 'username', 'first_name', 'last_name', 'email', 'date_joined','is_active', 'is_staff')
    # search_fields = ('username',)
    # list_filter = ('username',)
    # empty_value_display = '-пусто-'


@admin.register(LizaGroupPhrase)
class LizaGroupPhraseAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'num_group', 'priority')
    search_fields = ('text',)
    list_filter = ('text',)
    empty_value_display = '-пусто-'


@admin.register(LizaPhrase)
class LizaPhraseAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'group', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('text',)
    empty_value_display = '-пусто-'


class FileInline(admin.TabularInline):
    model = File


@admin.register(GermanGroupPhrase)
class GermanGroupPhraseAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'num_group', 'priority')
    search_fields = ('text',)
    list_filter = ('text',)
    empty_value_display = '-пусто-'
    inlines = [
        FileInline,
    ]


@admin.register(GermanPhrase)
class GermanPhraseAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'group', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('text',)
    empty_value_display = '-пусто-'


@admin.register(Name)
class NameAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'sex', 'pub_date', 'author', 'short_names')
    search_fields = ('text',)
    list_filter = ('text',)
    empty_value_display = '-пусто-'


@admin.register(NdzGroupPhrase)
class NdzGroupPhraseAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'num_group', 'priority')
    search_fields = ('text',)
    list_filter = ('text',)
    empty_value_display = '-пусто-'


@admin.register(NdzPhrase)
class NdzPhraseAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'group', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('text',)
    empty_value_display = '-пусто-'


@admin.register(PzGroupPhrase)
class PzGroupPhraseAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'num_group', 'priority')
    search_fields = ('text',)
    list_filter = ('text',)
    empty_value_display = '-пусто-'


@admin.register(PzPhrase)
class PzPhraseAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'group', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('text',)
    empty_value_display = '-пусто-'
