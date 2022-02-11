# Generated by Django 3.0.5 on 2022-02-10 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domconnect', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DcCrmService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_service', models.PositiveSmallIntegerField(unique=True, verbose_name='ID услуги')),
                ('service', models.CharField(blank=True, default='', max_length=255, verbose_name='Услуга')),
            ],
        ),
        migrations.CreateModel(
            name='DcCrmDeal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_deal', models.IntegerField(unique=True, verbose_name='ID сделки')),
                ('source_id', models.CharField(blank=True, default='', max_length=255, verbose_name='Источник')),
                ('create_date', models.DateTimeField(blank=True, null=True, verbose_name='Создано')),
                ('modify_date', models.DateTimeField(blank=True, null=True, verbose_name='Изменено')),
                ('crm_5904FB99DBF0C', models.DateTimeField(blank=True, null=True, verbose_name='Подключение')),
                ('crm_5EECA3B76309E', models.DateTimeField(blank=True, null=True, verbose_name='Дата лида')),
                ('crm_5903C16BDAA69', models.IntegerField(blank=True, default=0, verbose_name='Сумма тарифа')),
                ('crm_5903C16BCEE3A', models.ManyToManyField(related_name='services', to='domconnect.DcCrmService', verbose_name='Услуги')),
            ],
        ),
    ]
