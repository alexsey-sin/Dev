from django.db import models


PV_VARS = (
    (1, 'Билайн'),
    (2, 'ДомРу'),
    (3, 'МТС'),
    (4, 'Ростелеком'),
    (5, 'ТТК'),
    (6, 'ОнЛайм'),
    (7, 'МГТС'),
)


class BotAccess(models.Model):
    name = models.CharField(
        unique = True,
        max_length = 200,
        verbose_name = 'Название бота',
    )
    last_visit = models.DateTimeField(
        null = True,
        blank = True,
        verbose_name='Время посещения',
    )
    omission_min = models.PositiveSmallIntegerField(
        default = 120,
        verbose_name = 'Бездействие мин',
    )
    work = models.BooleanField(
        default = True,
        verbose_name = 'В работе',
    )
    login = models.CharField(
        verbose_name = 'Логин',
        max_length = 200,
        default = 'login',
    )
    password = models.CharField(
        verbose_name = 'Пароль',
        max_length = 200,
        default = 'password',
    )
    login_2 = models.CharField(
        verbose_name = 'Логин_2',
        max_length = 200,
        blank = True,
    )
    password_2 = models.CharField(
        verbose_name = 'Пароль_2',
        max_length = 200,
        blank = True,
    )
    
    def __str__(self):
        return self.name


class BidDomRu2(models.Model):
    STATUS_VAR = (
        (0, 'Заявка поступила'),
        (1, 'Бот забрал заявку'),
        (2, 'Ошибка в заявке, передано оператору'),
        (3, 'Заявка отклонена, передано оператору'),
        (4, 'Заявка принята ДомРу'),
    )
    SERVICE_CHOICES = (
        (0, 'Нет'),
        (1, 'Да'),
    )
    city = models.CharField(
        verbose_name = 'Город',
        max_length = 200,
    )
    street = models.CharField(
        max_length=200,
        verbose_name = 'Адрес',
    )
    house = models.CharField(
        max_length=50,
        verbose_name = 'Дом',
    )
    apartment = models.CharField(
        max_length=50,
        verbose_name = 'Кв.',
    )
    name = models.CharField(
        max_length=50,
        verbose_name = 'Имя',
    )
    phone = models.CharField(
        max_length=11,
        verbose_name = 'Телефон',
    )
    service_tv = models.PositiveSmallIntegerField(
        default = 0,
        choices = SERVICE_CHOICES,
        verbose_name = 'TV',
    )
    service_net = models.PositiveSmallIntegerField(
        default = 0,
        choices = SERVICE_CHOICES,
        verbose_name = 'NET',
    )
    service_phone = models.PositiveSmallIntegerField(
        default = 0,
        choices = SERVICE_CHOICES,
        verbose_name = 'PHONE',
    )
    comment = models.TextField(
        blank = True,
        verbose_name='Коментарий',
    )
    status = models.IntegerField(
        choices = STATUS_VAR,
        verbose_name = 'Статус',
    )
    change_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано',
    )


class BidBeeline(models.Model):
    STATUS_VAR = (
        (0, 'Заявка поступила'),
        (1, 'Бот забрал заявку'),
        (2, 'Ошибка отправки заявки, передано оператору'),
        (3, 'Заявка принята Билайн'),
    )
    TYPE_ABONENT_VAR = (
        (0, 'Пакетные предложения'),
        (1, 'Абонент Билайн'),
        (2, 'Доставка СИМ'),
        (3, 'Доставка СИМ(MNP)'),
    )
    partner_login = models.CharField(
        verbose_name = 'Логин',
        max_length = 200,
    )
    partner_workercode = models.CharField(
        verbose_name = 'Партнер',
        max_length = 200,
    )
    partner_password = models.CharField(
        verbose_name = 'Пароль',
        max_length = 200,
    )
    id_lid = models.CharField(
        max_length=50,
        verbose_name = 'ID лида',
    )
    city = models.CharField(
        verbose_name = 'Город',
        max_length = 200,
    )
    street = models.CharField(
        max_length=200,
        verbose_name = 'Улица',
    )
    house = models.CharField(
        max_length=50,
        verbose_name = 'Дом',
    )
    apartment = models.CharField(
        max_length=50,
        verbose_name = 'Кв.',
    )
    firstname = models.CharField(
        max_length=100,
        verbose_name = 'Имя',
        default = '-',
    )
    patronymic = models.CharField(
        max_length=100,
        verbose_name = 'Отчество',
        default = '-',
    )
    lastname = models.CharField(
        max_length=100,
        verbose_name = 'Фамилия',
        default = '-',
    )
    phone = models.CharField(
        max_length=11,
        verbose_name = 'Телефон',
    )
    type_abonent = models.PositiveSmallIntegerField(
        choices = TYPE_ABONENT_VAR,
        verbose_name = 'Тип абонента',
        default = 0,
    )
    tarif = models.CharField(
        max_length=100,
        verbose_name = 'Тариф',
    )
    ctn_abonent = models.CharField(
        max_length=100,
        blank = True,
        verbose_name = 'CTN абонента',
    )
    bid_number = models.CharField(
        max_length=100,
        blank = True,
        verbose_name = 'Номер заявки',
    )
    dt_grafic = models.CharField(
        max_length=100,
        blank = True,
        verbose_name = 'В график',
    )
    grafic_error = models.TextField(
        blank = True,
        verbose_name='Ошибки графика',
    )
    grafic_dop_info = models.TextField(
        blank = True,
        verbose_name='График Доп инфо',
    )
    status = models.PositiveSmallIntegerField(
        choices = STATUS_VAR,
        verbose_name = 'Статус',
    )
    change_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано',
    )
    bot_log = models.TextField(
        blank = True,
        verbose_name='Лог бота',
    )


class BidMTS(models.Model):
    STATUS_VAR = (
        (0, 'Заявка поступила'),
        (1, 'Бот забрал заявку'),
        (2, 'Ошибка отправки заявки, передано оператору'),
        (3, 'Заявка принята МТС'),
    )
    login = models.CharField(
        verbose_name = 'Логин',
        max_length = 200,
    )
    password = models.CharField(
        verbose_name = 'Пароль',
        max_length = 200,
    )
    id_lid = models.CharField(
        max_length=50,
        verbose_name = 'ID лида',
    )
    region = models.CharField(
        verbose_name = 'Область',
        max_length = 200,
    )
    city = models.CharField(
        blank = True,
        verbose_name = 'Город',
        max_length = 200,
    )
    street = models.CharField(
        max_length=200,
        verbose_name = 'Адрес',
    )
    house = models.CharField(
        max_length=50,
        verbose_name = 'Дом',
    )
    apartment = models.CharField(
        max_length=50,
        verbose_name = 'Кв.',
    )
    tarif = models.CharField(
        max_length=100,
        verbose_name = 'Тариф',
    )
    firstname = models.CharField(
        max_length=100,
        verbose_name = 'Имя',
    )
    patronymic = models.CharField(
        max_length=100,
        verbose_name = 'Отчество',
        default = '',
        blank = True,
    )
    lastname = models.CharField(
        max_length=100,
        verbose_name = 'Фамилия',
        default = '',
        blank = True,
    )
    phone = models.CharField(
        max_length=11,
        verbose_name = 'Телефон',
    )
    comment = models.TextField(
        blank = True,
        verbose_name='Комментарий',
    )
    bid_number = models.CharField(
        max_length=100,
        blank = True,
        verbose_name = 'Номер заявки',
    )
    status = models.IntegerField(
        choices = STATUS_VAR,
        verbose_name = 'Статус',
    )
    change_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано',
    )
    bot_log = models.TextField(
        blank = True,
        verbose_name='Лог бота',
    )


class BidBeeline2(models.Model):
    STATUS_VAR = (
        (0, 'Заявка поступила'),
        (1, 'Бот забрал заявку'),
        (2, 'Ошибка отправки заявки, передано оператору'),
        (3, 'Заявка принята Билайн'),
    )
    parther_key = models.CharField(
        verbose_name = 'Ключ партнера',
        max_length = 200,
    )
    client_inn = models.CharField(
        verbose_name = 'ИНН партнера',
        max_length = 200,
    )
    client_name = models.CharField(
        verbose_name = 'Название партнера',
        max_length = 200,
    )
    id_lid = models.CharField(
        max_length=50,
        verbose_name = 'ID лида',
    )
    contact_name = models.CharField(
        verbose_name = 'ФИО клиента',
        max_length = 200,
    )
    phone = models.CharField(
        max_length=11,
        verbose_name = 'Телефон',
    )
    email = models.CharField(
        blank = True,
        max_length=50,
        verbose_name = 'email',
    )
    comment = models.TextField(
        blank = True,
        verbose_name='Комментарий',
    )
    products = models.CharField(
        max_length=200,
        verbose_name = 'Услуга',
    )
    bid_number = models.CharField(
        max_length=100,
        blank = True,
        verbose_name = 'Номер заявки',
    )
    status = models.PositiveSmallIntegerField(
        choices = STATUS_VAR,
        verbose_name = 'Статус',
    )
    change_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано',
    )
    bot_log = models.TextField(
        blank = True,
        verbose_name='Лог бота',
    )


class BidRostelecom2(models.Model):
    STATUS_VAR = (
        (0, 'Заявка поступила'),
        (1, 'Бот забрал заявку'),
        (2, 'Ошибка отправки заявки, передано оператору'),
        (3, 'Заявка принята Ростелеком'),
    )
    login = models.CharField(
        verbose_name = 'Логин',
        max_length = 200,
    )
    password = models.CharField(
        verbose_name = 'Пароль',
        max_length = 200,
    )
    id_lid = models.CharField(
        max_length=50,
        verbose_name = 'ID лида',
    )
    firstname = models.CharField(
        max_length=100,
        verbose_name = 'Имя',
        default = '',
        blank = True,
    )
    patronymic = models.CharField(
        max_length=100,
        verbose_name = 'Отчество',
        default = '',
        blank = True,
    )
    lastname = models.CharField(
        max_length=100,
        verbose_name = 'Фамилия',
        default = '',
        blank = True,
    )
    phone = models.CharField(
        max_length=11,
        verbose_name = 'Телефон',
    )
    address = models.CharField(
        max_length=300,
        verbose_name = 'Адрес',
    )
    inn_organisation = models.CharField(
        max_length=100,
        verbose_name = 'ИНН/Организация',
    )
    service = models.CharField(
        max_length=100,
        verbose_name = 'Услуга',
    )
    comment = models.TextField(
        blank = True,
        verbose_name='Комментарий',
    )
    bid_number = models.CharField(
        max_length=100,
        blank = True,
        verbose_name = 'Номер заявки',
    )
    status = models.IntegerField(
        choices = STATUS_VAR,
        verbose_name = 'Статус',
    )
    change_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано',
    )
    bot_log = models.TextField(
        blank = True,
        verbose_name='Лог бота',
    )


class BidRostelecom(models.Model):
    STATUS_VAR = (
        (0, 'Заявка поступила'),
        (1, 'Бот забрал заявку'),
        (2, 'Ошибка отправки заявки, передано оператору'),
        (3, 'Заявка принята Ростелеком'),
    )
    login = models.CharField(
        verbose_name = 'Логин',
        max_length = 200,
    )
    password = models.CharField(
        verbose_name = 'Пароль',
        max_length = 200,
    )
    id_lid = models.CharField(
        max_length=50,
        verbose_name = 'ID лида',
    )
    firstname = models.CharField(
        max_length=100,
        verbose_name = 'Имя',
        default = '',
        blank = True,
    )
    patronymic = models.CharField(
        max_length=100,
        verbose_name = 'Отчество',
        default = '',
        blank = True,
    )
    lastname = models.CharField(
        max_length=100,
        verbose_name = 'Фамилия',
        default = '',
        blank = True,
    )
    phone = models.CharField(
        max_length=11,
        verbose_name = 'Телефон',
    )
    region = models.CharField(
        max_length=100,
        verbose_name = 'Регион',
    )
    city = models.CharField(
        max_length=100,
        verbose_name = 'Город',
    )
    street = models.CharField(
        max_length=100,
        verbose_name = 'Улица',
    )
    house = models.CharField(
        max_length=10,
        verbose_name = 'Дом',
    )
    apartment = models.CharField(
        max_length=10,
        verbose_name = 'Квартира',
    )
    general_package = models.CharField(  # Название общего пакетного предложения
        max_length=100,
        verbose_name = 'Пакетное предл.',
        default = '',
        blank = True,
    )
    service_home_internet = models.CharField(
        max_length=100,
        verbose_name = 'Дом.интернет',
        default = '',
        blank = True,
    )
    service_smart_house = models.CharField(
        max_length=100,
        verbose_name = 'Умный дом',
        default = '',
        blank = True,
    )
    service_smart_intercom = models.CharField(
        max_length=100,
        verbose_name = 'Умный домофон',
        default = '',
        blank = True,
    )
    service_interactive_tv = models.CharField(
        max_length=100,
        verbose_name = 'Интерактивное ТВ',
        default = '',
        blank = True,
    )
    service_wink_tv_online = models.CharField(
        max_length=100,
        verbose_name = 'Wink-ТВ-онлайн',
        default = '',
        blank = True,
    )
    service_home_phone = models.CharField(
        max_length=100,
        verbose_name = 'Дом.телефон',
        default = '',
        blank = True,
    )
    service_mobile_connection = models.CharField(
        max_length=100,
        verbose_name = 'Моб.связь',
        default = '',
        blank = True,
    )
    service_iptv_packets = models.CharField(  # Пакеты телеканалов Интерактивное ТВ
        max_length=100,
        verbose_name = 'Пакет каналов iTV',
        default = '',
        blank = True,
    )
    comment = models.TextField(
        blank = True,
        verbose_name='Комментарий',
    )
    bid_number = models.CharField(
        max_length=100,
        blank = True,
        verbose_name = 'Номер заявки',
    )
    status = models.IntegerField(
        choices = STATUS_VAR,
        verbose_name = 'Статус',
    )
    change_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано',
    )
    bot_log = models.TextField(
        blank = True,
        verbose_name='Лог бота',
    )


class BidDomRu(models.Model):
    STATUS_VAR = (
        (0, 'Заявка поступила'),
        (1, 'Бот забрал заявку'),
        (2, 'Ошибка отправки заявки, передано оператору'),
        (3, 'Заявка принята ДомРу'),
    )
    login = models.CharField(
        verbose_name = 'Логин',
        max_length = 200,
    )
    password = models.CharField(
        verbose_name = 'Пароль',
        max_length = 200,
    )
    id_lid = models.CharField(
        max_length=50,
        verbose_name = 'ID лида',
    )
    firstname = models.CharField(
        max_length=100,
        verbose_name = 'Имя',
        default = '',
        blank = True,
    )
    patronymic = models.CharField(
        max_length=100,
        verbose_name = 'Отчество',
        default = '',
        blank = True,
    )
    lastname = models.CharField(
        max_length=100,
        verbose_name = 'Фамилия',
        default = '',
        blank = True,
    )
    phone = models.CharField(
        max_length=11,
        verbose_name = 'Телефон',
    )
    city = models.CharField(
        max_length=100,
        verbose_name = 'Город',
    )
    street = models.CharField(
        max_length=100,
        verbose_name = 'Улица',
    )
    house = models.CharField(
        max_length=10,
        verbose_name = 'Дом',
    )
    apartment = models.CharField(
        max_length=10,
        verbose_name = 'Квартира',
    )
    tarif = models.CharField(  # Название тарифного плана
        max_length=100,
        verbose_name = 'Тариф',
        default = '',
        blank = True,
    )
    router = models.CharField(
        max_length=100,
        verbose_name = 'Роутер',
        default = '',
        blank = True,
    )
    adapter = models.CharField(
        max_length=100,
        verbose_name = 'Приставка ТВ',
        default = '',
        blank = True,
    )
    comment = models.TextField(
        blank = True,
        verbose_name='Комментарий',
    )
    bid_number = models.CharField(
        max_length=100,
        blank = True,
        verbose_name = 'Номер заявки',
    )
    status = models.IntegerField(
        choices = STATUS_VAR,
        verbose_name = 'Статус',
    )
    change_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано',
    )
    bot_log = models.TextField(
        blank = True,
        verbose_name='Лог бота',
    )


class BidTtk(models.Model):
    STATUS_VAR = (
        (0, 'Заявка поступила'),
        (1, 'Бот забрал заявку'),
        (2, 'Ошибка отправки заявки, передано оператору'),
        (3, 'Заявка принята ТТК'),
    )
    login = models.CharField(
        verbose_name = 'Логин',
        max_length = 200,
    )
    password = models.CharField(
        verbose_name = 'Пароль',
        max_length = 200,
    )
    id_lid = models.CharField(
        max_length=50,
        verbose_name = 'ID лида',
    )
    firstname = models.CharField(
        max_length=100,
        verbose_name = 'Имя',
        default = '',
        blank = True,
    )
    patronymic = models.CharField(
        max_length=100,
        verbose_name = 'Отчество',
        default = '',
        blank = True,
    )
    lastname = models.CharField(
        max_length=100,
        verbose_name = 'Фамилия',
        default = '',
        blank = True,
    )
    phone = models.CharField(
        max_length=11,
        verbose_name = 'Телефон',
    )
    city = models.CharField(
        max_length=100,
        verbose_name = 'Город',
    )
    street = models.CharField(
        max_length=100,
        verbose_name = 'Улица',
    )
    house = models.CharField(
        max_length=10,
        verbose_name = 'Дом',
    )
    apartment = models.CharField(
        max_length=10,
        verbose_name = 'Квартира',
    )
    general_package = models.CharField(  # Название тарифного плана Общий пакет
        max_length=100,
        verbose_name = 'Общий пакет',
        default = '',
        blank = True,
    )
    service_internet = models.CharField(  # Название тарифного плана 
        max_length=100,
        verbose_name = 'Тариф интернет',
        default = '',
        blank = True,
    )
    service_tv = models.CharField(  # Название тарифного плана 
        max_length=100,
        verbose_name = 'Тариф ТВ',
        default = '',
        blank = True,
    )
    equipment = models.CharField(  # Перечень оборудования и способов приобретения
        max_length=1024,
        verbose_name = 'Оборудование',
        default = '',
        blank = True,
    )
    comment = models.TextField(
        blank = True,
        verbose_name='Комментарий',
    )
    bid_number = models.CharField(
        max_length=100,
        blank = True,
        verbose_name = 'Номер заявки',
    )
    status = models.IntegerField(
        choices = STATUS_VAR,
        verbose_name = 'Статус',
    )
    change_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано',
    )
    bot_log = models.TextField(
        blank = True,
        verbose_name='Лог бота',
    )


class BidOnlime(models.Model):
    STATUS_VAR = (
        (0, 'Заявка поступила'),
        (1, 'Бот забрал заявку'),
        (2, 'Ошибка отправки заявки, передано оператору'),
        (3, 'Заявка принята Онлайм'),
    )
    login = models.CharField(
        verbose_name = 'Логин',
        max_length = 200,
    )
    password = models.CharField(
        verbose_name = 'Пароль',
        max_length = 200,
    )
    id_lid = models.CharField(
        max_length=50,
        verbose_name = 'ID лида',
    )
    firstname = models.CharField(
        max_length=100,
        verbose_name = 'Имя',
        default = '',
        blank = True,
    )
    patronymic = models.CharField(
        max_length=100,
        verbose_name = 'Отчество',
        default = '',
        blank = True,
    )
    phone = models.CharField(
        max_length=11,
        verbose_name = 'Телефон',
    )
    city = models.CharField(
        max_length=100,
        verbose_name = 'Город',
    )
    street = models.CharField(
        max_length=100,
        verbose_name = 'Улица',
    )
    house = models.CharField(
        max_length=10,
        verbose_name = 'Дом',
    )
    apartment = models.CharField(
        max_length=10,
        verbose_name = 'Квартира',
    )
    entrances = models.CharField(
        max_length=10,
        verbose_name = 'Подъезд',
    )
    floor = models.CharField(
        max_length=10,
        verbose_name = 'Этаж',
    )
    tarifs_eq = models.CharField(  # Тарифный план, Оборудование
        max_length=250,
        verbose_name = 'Тариф, оборуд.',
        default = '',
        blank = True,
    )
    comment = models.TextField(
        blank = True,
        verbose_name='Комментарий',
    )
    bid_number = models.CharField(
        max_length=100,
        blank = True,
        verbose_name = 'Номер заявки',
    )
    status = models.IntegerField(
        choices = STATUS_VAR,
        verbose_name = 'Статус',
    )
    change_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано',
    )
    bot_log = models.TextField(
        blank = True,
        verbose_name='Лог бота',
    )


class BidMGTS(models.Model):
    STATUS_VAR = (
        (0, 'Заявка поступила'),
        (1, 'Бот забрал заявку'),
        (2, 'Ошибка отправки заявки, передано оператору'),
        (3, 'Заявка принята МГТС'),
    )
    TYPE_GRAFIC_VAR = (
        (0, 'Без назначения'),
        (1, 'На ближайший таймслот'),
        (2, 'На заданное время'),
        (3, 'Запрос таймслотов'),
    )
    login = models.CharField(
        verbose_name = 'Логин',
        max_length = 200,
    )
    password = models.CharField(
        verbose_name = 'Пароль',
        max_length = 200,
    )
    login2 = models.CharField(
        verbose_name = 'Логин2',
        max_length = 200,
    )
    password2 = models.CharField(
        verbose_name = 'Пароль2',
        max_length = 200,
    )
    id_lid = models.CharField(
        max_length=50,
        verbose_name = 'ID лида',
    )
    city = models.CharField(
        verbose_name = 'Город',
        max_length = 200,
    )
    street = models.CharField(
        max_length=200,
        verbose_name = 'Адрес',
    )
    house = models.CharField(
        max_length=50,
        verbose_name = 'Дом',
    )
    apartment = models.CharField(
        max_length=50,
        verbose_name = 'Кв.',
    )
    wifi_router = models.CharField(
        max_length=100,
        verbose_name = 'wifi Роутер',
        default = '',
        blank = True,
    )
    count_tv = models.CharField(
        max_length=50,
        verbose_name = 'Кол-во ТВ',
        default = '0',
    )
    tv_adapter = models.CharField(
        max_length=100,
        verbose_name = 'ТВ приставка',
        default = '',
        blank = True,
    )
    tarif = models.CharField(
        max_length=100,
        verbose_name = 'Тариф',
    )
    tp_grafic = models.PositiveSmallIntegerField(
        choices = TYPE_GRAFIC_VAR,
        verbose_name = 'Тип в график',
        default = 0,
    )
    dt_grafic = models.CharField(
        max_length=100,
        blank = True,
        verbose_name = 'В график',
    )
    firstname = models.CharField(
        max_length=100,
        verbose_name = 'Имя',
        default = '',
        blank = True,
    )
    patronymic = models.CharField(
        max_length=100,
        verbose_name = 'Отчество',
        default = '',
        blank = True,
    )
    lastname = models.CharField(
        max_length=100,
        verbose_name = 'Фамилия',
        default = '',
        blank = True,
    )
    phone = models.CharField(
        max_length=11,
        verbose_name = 'Телефон',
    )
    comment = models.TextField(
        blank = True,
        verbose_name='Комментарий',
    )
    bid_number = models.CharField(
        max_length=100,
        blank = True,
        verbose_name = 'Номер заявки',
    )
    status = models.IntegerField(
        choices = STATUS_VAR,
        verbose_name = 'Статус',
    )
    change_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано',
    )
    bot_log = models.TextField(
        blank = True,
        verbose_name='Лог бота',
    )


class TxV(models.Model):
    STATUS_VAR = (
        (0, 'Запрос поступил'),
        (1, 'Бот забрал запрос'),
        (2, 'Ошибка обработки запроса'),
        (3, 'Запрос отработан'),
    )
    pv_code = models.PositiveSmallIntegerField(
        choices = PV_VARS,
        verbose_name = 'Оператор',
    )
    provider_dc =  models.TextField(
        blank = True,
        verbose_name='Провайдеры ДК',
    )
    login = models.CharField(
        verbose_name = 'Логин',
        max_length = 200,
    )
    password = models.CharField(
        verbose_name = 'Пароль',
        max_length = 200,
    )
    login_2 = models.CharField(
        verbose_name = 'Логин_2',
        max_length = 200,
        blank = True,
    )
    password_2 = models.CharField(
        verbose_name = 'Пароль_2',
        max_length = 200,
        blank = True,
    )
    id_lid = models.CharField(
        max_length=50,
        verbose_name = 'ID лида',
        blank = True,
    )
    region = models.CharField(
        verbose_name = 'Область',
        max_length = 200,
        blank = True,
    )
    city = models.CharField(
        verbose_name = 'Город',
        max_length = 200,
    )
    street = models.CharField(
        max_length=200,
        verbose_name = 'Улица',
    )
    house = models.CharField(
        max_length=50,
        verbose_name = 'Дом',
    )
    apartment = models.CharField(
        max_length=50,
        verbose_name = 'Кв.',
        blank = True,
    )
    available_connect = models.TextField(
        verbose_name = 'ТхВ',
        blank = True,
    )
    tarifs_all = models.TextField(
        blank = True,
        verbose_name='Тарифы',
    )
    pv_address = models.TextField(
        verbose_name = 'ПВ адрес',
        blank = True,
    )
    status = models.PositiveSmallIntegerField(
        choices = STATUS_VAR,
        verbose_name = 'Статус',
    )
    change_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано',
    )
    bot_log = models.TextField(
        blank = True,
        verbose_name='Лог бота',
    )
    class Meta:
        verbose_name = 'ТхВ'
        verbose_name_plural = 'ТхВ'
