# Generated by Django 3.0.5 on 2021-10-19 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20211018_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidbeeline',
            name='patronymic',
            field=models.CharField(blank=True, max_length=100, verbose_name='Отчество'),
        ),
        migrations.AddField(
            model_name='bidbeeline',
            name='type_abonent',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Пакетные предложения'), (1, 'Абонент Билайн'), (2, 'Доставка СИМ'), (3, 'Доставка СИМ(MNP)')], default=0, verbose_name='Статус'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bidbeeline',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Заявка поступила'), (1, 'Бот забрал заявку'), (2, 'Ошибка отправки заявки, передано оператору'), (3, 'Заявка принята Билайн')], verbose_name='Статус'),
        ),
    ]
