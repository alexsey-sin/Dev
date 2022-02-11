from django.core.management.base import BaseCommand
from domconnect.download_crm import run_download_crm
from datetime import datetime
from domconnect.models import DcCrmGlobVar


class Command(BaseCommand):
    help = 'Загрузка лидов и сделок из СРМ и расчет данных для кэш'

    def handle(self, *args, **options):
        run_download_crm()
