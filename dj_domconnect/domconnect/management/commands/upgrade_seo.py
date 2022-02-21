from django.core.management.base import BaseCommand
from domconnect.lib_seo import run_upgrade_seo


class Command(BaseCommand):
    help = 'Загрузка лидов и сделок из СРМ и расчет данных для кэш'

    def handle(self, *args, **options):
        run_upgrade_seo()
