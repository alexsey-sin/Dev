# Generated by Django 3.0.5 on 2022-01-26 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domconnect', '0002_auto_20220126_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dccrmlid',
            name='crm_1493416385',
            field=models.IntegerField(blank=True, default=0, verbose_name='Сумма тарифа'),
        ),
        migrations.AlterField(
            model_name='dccrmlid',
            name='crm_1498756113',
            field=models.BooleanField(blank=True, default=False, verbose_name='Юр. лицо'),
        ),
        migrations.AlterField(
            model_name='dccrmlid',
            name='crm_1580454770',
            field=models.BooleanField(blank=True, default=False, verbose_name='Звонок?'),
        ),
        migrations.AlterField(
            model_name='dccrmlid',
            name='crm_1592566018',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Тип лида'),
        ),
    ]