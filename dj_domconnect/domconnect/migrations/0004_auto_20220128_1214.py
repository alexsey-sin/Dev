# Generated by Django 3.0.5 on 2022-01-28 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domconnect', '0003_auto_20220126_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='DcCashSEO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('val_date', models.DateField(verbose_name='Период')),
                ('table', models.PositiveSmallIntegerField(verbose_name='Таблица')),
                ('row', models.PositiveSmallIntegerField(verbose_name='Строка')),
                ('val', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=8, verbose_name='Значение')),
            ],
        ),
        migrations.AlterField(
            model_name='dccrmlid',
            name='assigned_by_id',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Ответственный'),
        ),
    ]