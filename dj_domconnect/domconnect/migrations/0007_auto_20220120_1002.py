# Generated by Django 3.0.5 on 2022-01-20 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domconnect', '0006_auto_20220120_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domconnectcrmlid',
            name='id_lid',
            field=models.IntegerField(unique=True, verbose_name='ID лида'),
        ),
    ]