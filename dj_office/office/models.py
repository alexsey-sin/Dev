from django.db import models


class MoexBOND(models.Model):
    secid = models.CharField(
        max_length = 100,
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        verbose_name='Тикер',
    )
    name = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
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
        null = True,
        verbose_name='Номинал',
    )
    couponfrequency = models.PositiveSmallIntegerField(
        blank = True,
        null = True,
        verbose_name='Куп./год',
    )
    couponvalue = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        null = True,
        verbose_name='Купон',
    )
    typename = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name='Тип',
    )
    def __str__(self):
        return self.name


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
