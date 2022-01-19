from django.db import models


class DomconnectCrmLid(models.Model):
    id_lid = models.IntegerField(
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        blank = True,
        default = 0,
        verbose_name='ID',
    )
    title = models.CharField(
        max_length = 255,
        verbose_name = 'Титл',  # Удобочитаемое имя поля
        blank = True,
        default = '',
    )
    status_id = models.IntegerField(
        verbose_name='Статус',
        blank = True,
        default = 0,
    )
    create_date = models.DateTimeField(
        verbose_name='Создано',
        blank = True,
        null = True,
    )
    modify_date = models.DateTimeField(
        verbose_name='Изменено',
        blank = True,
        null = True,
    )
    source_id = models.IntegerField(
        verbose_name='Источник',
        blank = True,
        default = 0,
    )
    assigned_by_id = models.IntegerField(
        verbose_name='ASSIGNED_BY_ID',
        blank = True,
        default = 0,
    )
    crm_1493416385 = models.CharField(
        max_length = 100,
        verbose_name = 'Сумма тарифа',
        blank = True,
        default = '',
    )
    crm_1499437861 = models.CharField(
        max_length = 100,
        verbose_name = 'ИНН/Организация',
        blank = True,
        default = '',
    )
    crm_1580454770 = models.CharField(
        max_length = 100,
        verbose_name = 'Звонок?',
        blank = True,
        default = '',
    )
    crm_1534919765 = models.CharField(
        max_length = 100,
        verbose_name = 'Группы источников',
        blank = True,
        default = '',
    )
    crm_1571987728429 = models.CharField(
        max_length = 100,
        verbose_name = 'Провайдеры ДК',
        blank = True,
        default = '',
    )
    crm_1592566018 = models.CharField(
        max_length = 100,
        verbose_name = 'ТИп лида',
        blank = True,
        default = '',
    )
    crm_1493413514 = models.CharField(
        max_length = 100,
        verbose_name = 'Провайдер',
        blank = True,
        default = '',
    )
    crm_1492017494 = models.CharField(
        max_length = 100,
        verbose_name = 'Область',
        blank = True,
        default = '',
    )
    crm_1492017736 = models.CharField(
        max_length = 100,
        verbose_name = 'Город',
        blank = True,
        default = '',
    )
    crm_1498756113 = models.BooleanField(
        verbose_name = 'Юр. лицо',
        blank = True,
        default = False,
    )

    crm_1615982450 = models.CharField(
        max_length = 100,
        verbose_name = 'utm_source',
        blank = True,
        default = '',
    )
    crm_1615982567 = models.CharField(
        max_length = 100,
        verbose_name = 'utm_medium',
        blank = True,
        default = '',
    )
    crm_1615982644 = models.CharField(
        max_length = 100,
        verbose_name = 'utm_campaign',
        blank = True,
        default = '',
    )
    crm_1615982716 = models.CharField(
        max_length = 100,
        verbose_name = 'utm_term',
        blank = True,
        default = '',
    )
    crm_1615982795 = models.CharField(
        max_length = 100,
        verbose_name = 'utm_content',
        blank = True,
        default = '',
    )
    crm_1640267556 = models.CharField(
        max_length = 100,
        verbose_name = 'utm_group',
        blank = True,
        default = '',
    )

    def __str__(self):
        return self.title


class GlobalVariable(models.Model):
    key = models.CharField(  # Название переменной
        max_length = 100,
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
    )
    val_str = models.CharField(
        max_length = 100,
        blank = True,
        default = '',
    )
    val_bool = models.BooleanField(
        blank = True,
        default = False,
    )
    val_int = models.IntegerField(
        blank = True,
        default = 0,
    )
    val_datetime = models.DateTimeField(
        blank = True,
        null = True,
    )


