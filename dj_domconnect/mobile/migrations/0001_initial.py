# Generated by Django 3.0.5 on 2021-10-08 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MobileNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opsos', models.CharField(choices=[('beeline', 'Билайн'), ('megafon', 'Мегафон'), ('mts', 'МТС')], max_length=16, verbose_name='Оператор')),
                ('type_channel', models.CharField(blank=True, default='', max_length=32, verbose_name='Тип канала (ОП/Лиза, Герман)')),
                ('type_trunk', models.CharField(blank=True, default='', max_length=32, verbose_name='Тип транка (SIP, Gateway)')),
                ('type_tariff', models.CharField(blank=True, default='', max_length=32, verbose_name='Тип тарифа (для Би, для Мег, для МТС, для ост)')),
                ('name_tariff', models.CharField(blank=True, default='', max_length=32, verbose_name='Название тарифа')),
                ('tariff_description', models.CharField(blank=True, default='', max_length=256, verbose_name='Описание тарифа')),
                ('oatc_batc_description', models.CharField(blank=True, default='', max_length=256, verbose_name='Описание ОАТС/ВАТС')),
                ('unlimited_on_net', models.CharField(blank=True, default='', max_length=32, verbose_name='Безлимит внутри сети')),
                ('unlimited_on_net_not_consume_package', models.CharField(blank=True, default='', max_length=32, verbose_name='Безлимит внутри сети не расходует пакет')),
                ('package_cost', models.FloatField(blank=True, default=None, null=True, verbose_name='Стоимость пакета')),
                ('oatc_batc_cost', models.FloatField(blank=True, default=None, null=True, verbose_name='Стоимость ВАТС/ОАТС в пересчете на 1 номер')),
                ('number', models.CharField(max_length=16, unique=True, verbose_name='Номер')),
                ('mobile_packet', models.IntegerField(blank=True, null=True, verbose_name='Пакет минут')),
                ('sms_packet', models.IntegerField(blank=True, null=True, verbose_name='Пакет смс')),
                ('active', models.BooleanField(default=True, verbose_name='Активность номера')),
                ('comment', models.CharField(blank=True, default='', max_length=256, verbose_name='Комментарий')),
            ],
        ),
        migrations.CreateModel(
            name='MobileData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_available', models.IntegerField(blank=True, null=True, verbose_name='Доступно минут')),
                ('mobile_packet', models.IntegerField(blank=True, null=True, verbose_name='Пакет минут')),
                ('sms_available', models.IntegerField(blank=True, null=True, verbose_name='Доступно смс')),
                ('sms_packet', models.IntegerField(blank=True, null=True, verbose_name='Пакет смс')),
                ('balance', models.FloatField(blank=True, null=True, verbose_name='Баланс')),
                ('add_date', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mobile_number', to='mobile.MobileNumber', verbose_name='Номер телефона')),
            ],
        ),
    ]
