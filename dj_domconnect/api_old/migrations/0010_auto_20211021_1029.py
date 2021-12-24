# Generated by Django 3.0.5 on 2021-10-21 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20211020_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidbeeline',
            name='region',
            field=models.CharField(blank=True, max_length=200, verbose_name='Область'),
        ),
        migrations.AlterField(
            model_name='bidbeeline',
            name='firstname',
            field=models.CharField(default='-', max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='bidbeeline',
            name='lastname',
            field=models.CharField(default='-', max_length=100, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='bidbeeline',
            name='patronymic',
            field=models.CharField(default='-', max_length=100, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='bidbeeline',
            name='type_abonent',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Пакетные предложения'), (1, 'Абонент Билайн'), (2, 'Доставка СИМ'), (3, 'Доставка СИМ(MNP)')], default=0, verbose_name='Тип абонента'),
        ),
    ]
