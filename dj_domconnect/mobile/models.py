from django.db import models


class MobileNumber(models.Model):
    beeline = 'beeline'
    megafon = 'megafon'
    mts = 'mts'
    OPSOS_VAR = (
        (beeline, 'Билайн'),
        (megafon, 'Мегафон'),
        (mts, 'МТС'),
    )
    opsos = models.CharField(
        max_length=16,
        choices=OPSOS_VAR,
        verbose_name = 'Оператор',
        blank = False,
    )
    type_channel = models.CharField(
        max_length = 32,
        default = '',
        blank = True,
        verbose_name = 'Тип канала (ОП/Лиза, Герман)',
    )
    type_trunk = models.CharField(
        max_length = 32,
        default = '',
        blank = True,
        verbose_name = 'Тип транка (SIP, Gateway)',
    )
    type_tariff = models.CharField(
        max_length = 32,
        default = '',
        blank = True,
        verbose_name = 'Тип тарифа (для Би, для Мег, для МТС, для ост)',
    )
    name_tariff = models.CharField(
        max_length = 32,
        default = '',
        blank = True,
        verbose_name = 'Название тарифа',
    )
    tariff_description = models.CharField(
        max_length = 256,
        default = '',
        blank = True,
        verbose_name = 'Описание тарифа',
    )
    oatc_batc_description = models.CharField(
        max_length = 256,
        default = '',
        blank = True,
        verbose_name = 'Описание ОАТС/ВАТС',
    )
    unlimited_on_net = models.CharField(
        max_length = 32,
        default = '',
        blank = True,
        verbose_name = 'Безлимит внутри сети',
    )
    unlimited_on_net_not_consume_package = models.CharField(
        max_length = 32,
        default = '',
        blank = True,
        verbose_name = 'Безлимит внутри сети не расходует пакет',
    )
    package_cost = models.FloatField(
        blank=True, null=True,
        default=None,
        verbose_name = 'Стоимость пакета',
    )
    oatc_batc_cost = models.FloatField(
        blank=True, null=True,
        default=None,
        verbose_name = 'Стоимость ВАТС/ОАТС в пересчете на 1 номер',
    )
    number = models.CharField(
        unique = True,
        max_length = 16,
        blank = False,
        verbose_name = 'Номер',
        # default = '',
    )
    mobile_packet = models.IntegerField(
        blank=True, null=True,
        verbose_name = 'Пакет минут',
    )
    sms_packet = models.IntegerField(
        blank=True, null=True,
        verbose_name = 'Пакет смс',
    )
    active = models.BooleanField(
        default = True,
        verbose_name = 'Активность номера',
    )
    ats_except = models.BooleanField(
        default = False,
        verbose_name = 'Исключение для АТС',
    )
    ats_except_min = models.IntegerField(
        default = 0,
        verbose_name = 'Искл АТС мин',
    )
    comment = models.CharField(
        max_length = 256,
        default = '',
        blank = True,
        verbose_name = 'Комментарий',
    )

    def save(self, *args, **kwargs):
        if self.package_cost: self.package_cost = round(self.package_cost, 2)
        if self.oatc_batc_cost: self.oatc_batc_cost = round(self.oatc_batc_cost, 2)
        super(MobileNumber, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.number)


class MobileData(models.Model):
    number = models.ForeignKey(
        MobileNumber,
        related_name='mobile_number',
        blank = False,
        on_delete=models.CASCADE,
        verbose_name='Номер телефона',
    )
    mobile_available = models.IntegerField(
        blank=True, null=True,
        verbose_name='Доступно минут',
    )
    mobile_packet = models.IntegerField(
        blank=True, null=True,
        verbose_name='Пакет минут',
    )
    sms_available = models.IntegerField(
        blank=True, null=True,
        verbose_name='Доступно смс',
    )
    sms_packet = models.IntegerField(
        blank=True, null=True,
        verbose_name='Пакет смс',
    )
    balance = models.FloatField(
        blank=True, null=True,
        verbose_name='Баланс',
    )
    add_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Время обновления',
    )
    
    def __str__(self):
        return str(self.number)

