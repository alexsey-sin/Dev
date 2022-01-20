# Generated by Django 3.0.5 on 2022-01-20 09:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domconnect', '0004_auto_20220117_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalvariable',
            name='descriptions',
            field=models.TextField(blank=True, default='', verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='globalvariable',
            name='val_decimal',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 1, 20, 9, 31, 31, 612841), null=True, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='id_lid',
            field=models.IntegerField(unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='modify_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 1, 20, 9, 31, 31, 612841), null=True, verbose_name='Изменено'),
        ),
    ]
