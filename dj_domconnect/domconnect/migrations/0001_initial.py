# Generated by Django 3.0.5 on 2022-01-19 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DomconnectCrmLid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_lid', models.IntegerField(unique=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Титл')),
                ('status_id', models.IntegerField(verbose_name='Статус')),
                ('create_date', models.DateTimeField(verbose_name='Создано')),
                ('modify_date', models.DateTimeField(verbose_name='Изменено')),
                ('source_id', models.IntegerField(verbose_name='Источник')),
                ('assigned_by_id', models.IntegerField(verbose_name='ASSIGNED_BY_ID')),
                ('crm_1493416385', models.CharField(blank=True, max_length=100, verbose_name='Сумма тарифа')),
                ('crm_1499437861', models.CharField(blank=True, max_length=100, verbose_name='ИНН/Организация')),
                ('crm_1580454770', models.CharField(blank=True, max_length=100, verbose_name='Звонок?')),
                ('crm_1534919765', models.CharField(blank=True, max_length=100, verbose_name='Группы источников')),
                ('crm_1571987728429', models.CharField(blank=True, max_length=100, verbose_name='Провайдеры ДК')),
                ('crm_1592566018', models.CharField(blank=True, max_length=100, verbose_name='ТИп лида')),
                ('crm_1493413514', models.CharField(blank=True, max_length=100, verbose_name='Провайдер')),
                ('crm_1492017494', models.CharField(blank=True, max_length=100, verbose_name='Область')),
                ('crm_1492017736', models.CharField(blank=True, max_length=100, verbose_name='Город')),
                ('crm_1498756113', models.BooleanField(blank=True, default=False, verbose_name='Юр. лицо')),
                ('crm_1615982450', models.CharField(blank=True, max_length=100, verbose_name='utm_source')),
                ('crm_1615982567', models.CharField(blank=True, max_length=100, verbose_name='utm_medium')),
                ('crm_1615982644', models.CharField(blank=True, max_length=100, verbose_name='utm_campaign')),
                ('crm_1615982716', models.CharField(blank=True, max_length=100, verbose_name='utm_term')),
                ('crm_1615982795', models.CharField(blank=True, max_length=100, verbose_name='utm_content')),
                ('crm_1640267556', models.CharField(blank=True, max_length=100, verbose_name='utm_group')),
            ],
        ),
    ]