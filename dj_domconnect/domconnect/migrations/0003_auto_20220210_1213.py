# Generated by Django 3.0.5 on 2022-02-10 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domconnect', '0002_dccrmdeal_dccrmservice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dccrmdeal',
            name='crm_5903C16BCEE3A',
            field=models.ManyToManyField(blank=True, null=True, related_name='services', to='domconnect.DcCrmService', verbose_name='Услуги'),
        ),
    ]
