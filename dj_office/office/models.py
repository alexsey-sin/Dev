from django.db import models


class TypeBOND(models.Model):
    typekey = models.CharField(
        max_length = 100,
        unique = True,
        verbose_name = 'Код',
    )
    name = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'Название',
    )
    descriptions = models.TextField(
        blank = True,
        null = True,
        verbose_name = 'Описание',
    )
    def __str__(self):
        return self.typekey


class MoexBOND(models.Model):
    secid = models.CharField(
        max_length = 100,
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        verbose_name = 'Тикер',
    )
    name = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        verbose_name = 'Название',
    )
    matdate = models.DateTimeField(
        blank = True,
        null = True,
        verbose_name = 'Погашение',
    )
    facevalue = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        null = True,
        verbose_name = 'Номинал',
    )
    couponfrequency = models.PositiveSmallIntegerField(
        blank = True,
        null = True,
        verbose_name = 'Куп./год',
    )
    couponvalue = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        null = True,
        verbose_name = 'Купон',
    )
    typekey = models.ForeignKey(
        TypeBOND,
        on_delete = models.CASCADE,
        verbose_name = 'Тип',
    )
    profit = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        null = True,
        verbose_name = 'Доходность',
    )
    def __str__(self):
        return self.secid


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
        verbose_name = 'Описание',
    )


class FilterBOND(models.Model):
    name = models.CharField(  # Название переменной
        max_length = 100,
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        verbose_name = 'Название',
    )
    check_facevalue_from = models.BooleanField(
        blank = True,
        default = 'False',
        verbose_name = 'активно Номинал от',
    )
    facevalue_from = models.IntegerField(
        blank = True,
        null = True,
        verbose_name = 'Номинал от',
    )
    check_facevalue_to = models.BooleanField(
        blank = True,
        default = 'False',
        verbose_name = 'активно Номинал до',
    )
    facevalue_to = models.IntegerField(
        blank = True,
        null = True,
        verbose_name = 'Номинал до',
    )
    check_matdate_from = models.BooleanField(
        blank = True,
        default = 'False',
        verbose_name = 'активно Погашение от',
    )
    matdate_from = models.DateTimeField(
        blank = True,
        null = True,
        verbose_name = 'Погашение от',
    )
    check_matdate_to = models.BooleanField(
        blank = True,
        default = 'False',
        verbose_name = 'активно Погашение до',
    )
    matdate_to = models.DateTimeField(
        blank = True,
        null = True,
        verbose_name = 'Погашение до',
    )
    check_profit_from = models.BooleanField(
        blank = True,
        default = 'False',
        verbose_name = 'активно Доходность от',
    )
    profit_from = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        null = True,
        verbose_name = 'Доходность от',
    )
    check_profit_to = models.BooleanField(
        blank = True,
        default = 'False',
        verbose_name = 'активно Доходность до',
    )
    profit_to = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        null = True,
        verbose_name = 'Доходность до',
    )
    by_type = models.CharField(
        max_length = 256,
        blank = True,
        null = True,
        verbose_name = 'Типы',
    )
