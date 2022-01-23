# Generated by Django 4.0.1 on 2022-01-23 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FilterBOND',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('check_facevalue_from', models.BooleanField(blank=True, default='False', null=True, verbose_name='активно Номинал от')),
                ('facevalue_from', models.IntegerField(blank=True, null=True, verbose_name='Номинал от')),
                ('check_facevalue_to', models.BooleanField(blank=True, default='False', null=True, verbose_name='активно Номинал до')),
                ('facevalue_to', models.IntegerField(blank=True, null=True, verbose_name='Номинал до')),
                ('check_matdate_from', models.BooleanField(blank=True, default='False', null=True, verbose_name='активно Погашение от')),
                ('matdate_from', models.DateTimeField(blank=True, null=True, verbose_name='Погашение от')),
                ('check_matdate_to', models.BooleanField(blank=True, default='False', null=True, verbose_name='активно Погашение до')),
                ('matdate_to', models.DateTimeField(blank=True, null=True, verbose_name='Погашение до')),
                ('check_profit_from', models.BooleanField(blank=True, default='False', null=True, verbose_name='активно Доходность от')),
                ('profit_from', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Доходность от')),
                ('check_profit_to', models.BooleanField(blank=True, default='False', null=True, verbose_name='активно Доходность до')),
                ('profit_to', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Доходность до')),
                ('by_type', models.CharField(blank=True, max_length=256, null=True, verbose_name='Типы')),
            ],
        ),
        migrations.CreateModel(
            name='GlobalVariable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, unique=True)),
                ('val_str', models.CharField(blank=True, max_length=100, null=True)),
                ('val_bool', models.BooleanField(blank=True, null=True)),
                ('val_int', models.IntegerField(blank=True, null=True)),
                ('val_datetime', models.DateTimeField(blank=True, null=True)),
                ('val_decimal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('descriptions', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='TypeBOND',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typekey', models.CharField(max_length=100, unique=True, verbose_name='Код')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('descriptions', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='MoexBOND',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secid', models.CharField(max_length=100, unique=True, verbose_name='Тикер')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
                ('matdate', models.DateTimeField(blank=True, null=True, verbose_name='Погашение')),
                ('facevalue', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Номинал')),
                ('couponfrequency', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Куп./год')),
                ('couponvalue', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Купон')),
                ('profit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Доходность')),
                ('typekey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='office.typebond', verbose_name='Тип')),
            ],
        ),
    ]
