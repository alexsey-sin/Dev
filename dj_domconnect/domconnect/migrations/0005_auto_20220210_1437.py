# Generated by Django 3.0.5 on 2022-02-10 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domconnect', '0004_auto_20220210_1214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dccrmdeal',
            name='crm_5903C16BCEE3A',
        ),
        migrations.AddField(
            model_name='dccrmdeal',
            name='crm_5903C16BCEE3A',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Услуги'),
        ),
        migrations.DeleteModel(
            name='DcCrmService',
        ),
    ]
