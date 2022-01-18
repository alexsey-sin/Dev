from django.db import models
from datetime import datetime


class DomconnectCrmLid(models.Model):
    id_lid = models.IntegerField(  # Обязательное поле
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        verbose_name='ID лида',
    )
    title = models.CharField(
        max_length = 255,
        blank = True,
        null = True,
        verbose_name = 'Титл',
    )
    status_id = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name='Статус',
    )
    create_date = models.DateTimeField(
        blank = True,
        null = True,
        verbose_name='Создано',
    )
    modify_date = models.DateTimeField(
        blank = True,
        null = True,
        verbose_name='Изменено',
    )
    source_id = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name='Источник',
    )
    assigned_by_id = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name='ASSIGNED_BY_ID',
    )
    crm_1493416385 = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'Сумма тарифа',
    )
    crm_1499437861 = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'ИНН/Организация',
    )
    crm_1580454770 = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'Звонок?',
    )
    crm_1534919765 = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'Группы источников',
    )
    crm_1571987728429 = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'Провайдеры ДК',
    )
    crm_1592566018 = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'ТИп лида',
    )
    crm_1493413514 = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'Провайдер',
    )
    crm_1492017494 = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'Область',
    )
    crm_1492017736 = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'Город',
    )
    crm_1498756113 = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'Юр. лицо',
    )

    crm_1615982450 = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'utm_source',
    )
    crm_1615982567 = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'utm_medium',
    )
    crm_1615982644 = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'utm_campaign',
    )
    crm_1615982716 = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'utm_term',
    )
    crm_1615982795 = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'utm_content',
    )
    crm_1640267556 = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'utm_group',
    )

    def __str__(self):
        return str(self.id_lid)


class GlobalVariable(models.Model):
    key = models.CharField(  # Название переменной
        max_length = 100,
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
    )
    val_str = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
    )
    val_bool = models.BooleanField(
        blank = True,
        null = True,
    )
    val_int = models.IntegerField(
        blank = True,
        null = True,
    )
    val_datetime = models.DateTimeField(
        blank = True,
        null = True,
    )
    val_decimal = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        null = True,
    )
    descriptions = models.TextField(
        blank = True,
        null = True,
        verbose_name='Описание',
    )

