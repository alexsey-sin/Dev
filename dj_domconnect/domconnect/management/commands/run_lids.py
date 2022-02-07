from django.core.management.base import BaseCommand, CommandError
from domconnect.download_lids import run_download_crm
from datetime import datetime, timedelta
from domconnect.models import DcCrmGlobVar, DcCrmLid


class Command(BaseCommand):
    help = 'Загрузка лидов из СРМ и расчет данных для кэш'

    def handle(self, *args, **options):

        str_from_modify = ''
        last_modify_lid = DcCrmLid.objects.order_by('modify_date').last()
        if last_modify_lid:
            from_modify = last_modify_lid.modify_date
            if type(from_modify) == datetime:
                from_modify = from_modify - timedelta(seconds=1)
                str_from_modify = from_modify.strftime('%Y-%m-%dT%H:%M:%S')

        gvar_go, _ = DcCrmGlobVar.objects.get_or_create(key='go_download_crm')
        if gvar_go.val_bool:
            self.stdout.write(self.style.SUCCESS('Идет процесс загрузки и расчета.'))
            return
        gvar_go.val_bool = True
        gvar_go.val_datetime = datetime.today()
        gvar_go.descriptions = 'Загрузка запущена'
        gvar_go.save()

        # Обнулим глоб. переменную текущей позиции
        gvar_cur, _ = DcCrmGlobVar.objects.get_or_create(key='cur_num_download_crm')
        gvar_cur.val_int = 0
        gvar_cur.save(update_fields=['val_int'])

        self.stdout.write(self.style.SUCCESS('Загрузка лидов запущена.'))
        run_download_crm(str_from_modify)
        self.stdout.write(self.style.SUCCESS('Расчет и сохранение в кэш закончено.'))


