# Generated by Django 3.0.5 on 2021-12-27 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NdzGroupPhrase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(help_text='Дайте короткое название группе', max_length=200, unique=True, verbose_name='Название группы')),
                ('num_group', models.IntegerField(help_text='Укажите номер группы', unique=True, verbose_name='номер группы')),
                ('priority', models.IntegerField(help_text='Укажите приоритет от 0 до 100', verbose_name='Приоритет')),
            ],
        ),
        migrations.CreateModel(
            name='PzGroupPhrase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(help_text='Дайте короткое название группе', max_length=200, unique=True, verbose_name='Название группы')),
                ('num_group', models.IntegerField(help_text='Укажите номер группы', unique=True, verbose_name='номер группы')),
                ('priority', models.IntegerField(help_text='Укажите приоритет от 0 до 100', verbose_name='Приоритет')),
            ],
        ),
        migrations.CreateModel(
            name='PzPhrase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(help_text='Введите текст фразы', max_length=200, unique=True, verbose_name='Фраза')),
                ('pub_date', models.DateTimeField(auto_now=True, help_text='Текущее время (авто)', verbose_name='Дата создания/изменения')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.LizaGroupPhrase', verbose_name='Принадлежность фразы к группе')),
            ],
        ),
        migrations.CreateModel(
            name='NdzPhrase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(help_text='Введите текст фразы', max_length=200, unique=True, verbose_name='Фраза')),
                ('pub_date', models.DateTimeField(auto_now=True, help_text='Текущее время (авто)', verbose_name='Дата создания/изменения')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.LizaGroupPhrase', verbose_name='Принадлежность фразы к группе')),
            ],
        ),
    ]