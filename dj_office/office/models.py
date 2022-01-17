from django.db import models


class MoexBOND(models.Model):
    secid = models.CharField(
        max_length = 100,
        blank = True,
        default = '',
        verbose_name='Тикер',
    )
    name = models.CharField(
        max_length = 100,
        blank = True,
        default = '',
        verbose_name='Название',
    )
    matdate = models.DateTimeField(
        blank = True,
        null = True,
        verbose_name='Погашение',
    )
    facevalue = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        default = 0.0,
        verbose_name='Номинал',
    )
    couponfrequency = models.PositiveSmallIntegerField(
        blank = True,
        default = 0,
        verbose_name='Куп./год',
    )
    couponvalue = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        default = 0.0,
        verbose_name='Купон',
    )
    typename = models.CharField(
        max_length = 100,
        blank = True,
        default = '',
        verbose_name='Тип',
    )
    def __str__(self):
        return self.name


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
