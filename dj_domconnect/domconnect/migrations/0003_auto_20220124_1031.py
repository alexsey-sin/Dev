# Generated by Django 3.0.5 on 2022-01-24 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domconnect', '0002_auto_20220124_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='assigned_by_id',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='ASSIGNED_BY_ID'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='crm_1492017494',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Область'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='crm_1492017736',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='crm_1493413514',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Провайдер'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='crm_1493416385',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Сумма тарифа'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='crm_1498756113',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Юр. лицо'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='crm_1499437861',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='ИНН/Организация'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='crm_1534919765',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Группы источников'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='crm_1571987728429',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Провайдеры ДК'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='crm_1580454770',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Звонок?'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='crm_1592566018',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='ТИп лида'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='crm_1615982450',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='utm_source'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='crm_1615982567',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='utm_medium'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='crm_1615982644',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='utm_campaign'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='crm_1615982716',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='utm_term'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='crm_1615982795',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='utm_content'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='crm_1640267556',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='utm_group'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='source_id',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Источник'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='status_id',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='title',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Титл'),
        ),
        migrations.AlterField(
            model_name='globalvariable',
            name='descriptions',
            field=models.TextField(blank=True, default='', verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='globalvariable',
            name='val_str',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
