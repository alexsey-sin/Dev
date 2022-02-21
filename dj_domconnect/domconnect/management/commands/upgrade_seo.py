import threading
from threading import Thread
from django.core.management.base import BaseCommand
from domconnect.lib_seo import run_upgrade_seo


class Command(BaseCommand):
    help = 'Загрузка лидов и сделок из СРМ и расчет данных для кэш'

    def handle(self, *args, **options):
        thread_name = 'ThreadUpgradeSeo'
        is_run = False
        for thread in threading.enumerate():
            if thread.getName() == thread_name: is_run = True; break

        if is_run == False:
            # Запустим поток загрузки
            th = Thread(target=run_upgrade_seo, name=thread_name, args=())
            th.start()
