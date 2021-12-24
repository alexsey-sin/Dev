from django.contrib import admin
from .models import CD


class CDAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "artist", "genre")
    list_filter = ("date", "genre")
    empty_value_display = "-пусто-"

    
admin.site.register(CD, CDAdmin)
