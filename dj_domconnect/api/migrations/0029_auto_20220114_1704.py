# Generated by Django 3.0.5 on 2022-01-14 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20211229_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='BidMGTS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=200, verbose_name='Логин')),
                ('password', models.CharField(max_length=200, verbose_name='Пароль')),
                ('login2', models.CharField(max_length=200, verbose_name='Логин2')),
                ('password2', models.CharField(max_length=200, verbose_name='Пароль2')),
                ('id_lid', models.CharField(max_length=50, verbose_name='ID лида')),
                ('city', models.CharField(max_length=200, verbose_name='Город')),
                ('street', models.CharField(max_length=200, verbose_name='Адрес')),
                ('house', models.CharField(max_length=50, verbose_name='Дом')),
                ('apartment', models.CharField(max_length=50, verbose_name='Кв.')),
                ('wifi_router', models.CharField(default='', max_length=100, verbose_name='wifi Роутер')),
                ('count_tv', models.CharField(default='0', max_length=50, verbose_name='Кв.')),
                ('tv_adapter', models.CharField(default='', max_length=100, verbose_name='ТВ приставка')),
                ('tarif', models.CharField(max_length=100, verbose_name='Тариф')),
                ('tp_grafic', models.PositiveSmallIntegerField(choices=[(0, 'Без назначения'), (1, 'На ближайший таймслот'), (2, 'На заданное время'), (3, 'Запрос таймслотов')], default=0, verbose_name='Тип в график')),
                ('dt_grafic', models.CharField(blank=True, max_length=100, verbose_name='В график')),
                ('firstname', models.CharField(default='', max_length=100, verbose_name='Имя')),
                ('patronymic', models.CharField(default='', max_length=100, verbose_name='Отчество')),
                ('lastname', models.CharField(default='', max_length=100, verbose_name='Фамилия')),
                ('phone', models.CharField(max_length=11, verbose_name='Телефон')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('bid_number', models.CharField(blank=True, max_length=100, verbose_name='Номер заявки')),
                ('status', models.IntegerField(choices=[(0, 'Заявка поступила'), (1, 'Бот забрал заявку'), (2, 'Ошибка отправки заявки, передано оператору'), (3, 'Заявка принята МГТС')], verbose_name='Статус')),
                ('change_date', models.DateTimeField(auto_now=True, verbose_name='Изменено')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('bot_log', models.TextField(blank=True, verbose_name='Лог бота')),
            ],
        ),
        migrations.AlterField(
            model_name='txv',
            name='id_lid',
            field=models.CharField(blank=True, max_length=50, verbose_name='ID лида'),
        ),
    ]
