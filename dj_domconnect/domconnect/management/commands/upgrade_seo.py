from django.core.management.base import BaseCommand
from domconnect.download_crm import run_download_crm
from datetime import datetime
from domconnect.models import DcCrmGlobVar


class Command(BaseCommand):
    help = 'Загрузка лидов и сделок из СРМ и расчет данных для кэш'

    def handle(self, *args, **options):

        gvar_go, _ = DcCrmGlobVar.objects.get_or_create(key='go_upgrade_seo')
        if gvar_go.val_bool == True:
            self.stdout.write(self.style.SUCCESS('Идет процесс обновления данных SEO и расчета.'))
            return
        gvar_go.val_bool = True
        gvar_go.val_datetime = datetime.today()
        gvar_go.descriptions = 'Обновение SEO запущено'
        gvar_go.save()

        self.stdout.write(self.style.SUCCESS('Обновение данных SEO запущено.'))
        run_download_crm()

        gvar_go.val_bool = False
        gvar_go.val_datetime = datetime.today()
        gvar_go.descriptions = 'Обновение SEO закончено'
        gvar_go.save()

        self.stdout.write(self.style.SUCCESS('Расчет и сохранение данных SEO в кэш закончено.'))
