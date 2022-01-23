# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class LizaGroupPhrase(models.Model):
    text = models.CharField(
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        verbose_name = 'Название группы',  # Удобочитаемое имя поля
        max_length = 200,
        help_text = 'Дайте короткое название группе',  # Дополнительный текст «справки», отображаемый в виджете формы.
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
        # default = ''  # Значение по умолчанию для поля.
    )
    num_group = models.IntegerField(
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
        verbose_name='номер группы',
        help_text='Укажите номер группы',
    )
    priority = models.IntegerField(
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
        verbose_name='Приоритет',
        help_text='Укажите приоритет от 0 до 100',
    )

    def __str__(self):
        return self.text


class LizaPhrase(models.Model):
    text = models.CharField(
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        verbose_name = 'Фраза',  # Удобочитаемое имя поля
        max_length = 200,
        help_text = 'Введите текст фразы',  # Дополнительный текст «справки», отображаемый в виджете формы.
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
    )
    group = models.ForeignKey(
        LizaGroupPhrase,
        on_delete=models.CASCADE,
        verbose_name='Принадлежность фразы к группе',
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата создания/изменения',
        help_text='Текущее время (авто)',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    def __str__(self):
        return self.text


class GermanGroupPhrase(models.Model):
    text = models.CharField(
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        verbose_name = 'Название группы',  # Удобочитаемое имя поля
        max_length = 200,
        help_text = 'Дайте короткое название группе',  # Дополнительный текст «справки», отображаемый в виджете формы.
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
        # default = ''  # Значение по умолчанию для поля.
    )
    num_group = models.IntegerField(
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
        verbose_name='номер группы',
        help_text='Укажите номер группы',
    )
    priority = models.IntegerField(
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
        verbose_name='Приоритет',
        help_text='Укажите приоритет от 0 до 100',
    )

    def __str__(self):
        return self.text


class GermanPhrase(models.Model):
    text = models.CharField(
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        verbose_name = 'Фраза',  # Удобочитаемое имя поля
        max_length = 200,
        help_text = 'Введите текст фразы',  # Дополнительный текст «справки», отображаемый в виджете формы.
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
    )
    group = models.ForeignKey(
        GermanGroupPhrase,
        on_delete=models.CASCADE,
        verbose_name='Принадлежность фразы к группе',
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата создания/изменения',
        help_text='Текущее время (авто)',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    def __str__(self):
        return self.text


class File(models.Model):
    file = models.FileField(
        upload_to="audio/wav",
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        verbose_name = 'Звуковой файл',  # Удобочитаемое имя поля
        help_text = 'Выберите файл',  # Дополнительный текст «справки», отображаемый в виджете формы.
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
    )
    group = models.ForeignKey(
        GermanGroupPhrase,
        on_delete=models.CASCADE,
        verbose_name='Принадлежность фразы к группе',
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата создания/изменения',
        help_text='Текущее время (авто)',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path  # До удаления записи получаем необходимую информацию
        super(File, self).delete(*args, **kwargs)  # Удаляем сначала модель ( объект )
        storage.delete(path)  # Потом удаляем сам файл


class Name(models.Model):
    M = 'М'
    F = 'Ж'
    N = '-'
    SEX_VAR = (
        (M, 'Мужской'),
        (F, 'Женский'),
        (N, 'не определен'),
    )
    text = models.CharField(
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        verbose_name = 'Имя',  # Удобочитаемое имя поля
        max_length = 200,
        help_text = 'Полное имя',  # Дополнительный текст «справки», отображаемый в виджете формы.
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
        # default = ''  # Значение по умолчанию для поля.
    )
    sex = models.CharField(
        max_length=1,
        choices=SEX_VAR,
        default = N,
        verbose_name = 'Пол',
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата создания/изменения',
        help_text='Текущее время (авто)',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    short_names = models.TextField(
        blank = True,
        verbose_name='Короткие имена',
        help_text='Короткие имена через любой знак препинания или с новой строки',
    )

    def __str__(self):
        return self.text


class NdzGroupPhrase(models.Model):  # группы фраз Недозвоны
    text = models.CharField(
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        verbose_name = 'Название группы',  # Удобочитаемое имя поля
        max_length = 200,
        help_text = 'Дайте короткое название группе',  # Дополнительный текст «справки», отображаемый в виджете формы.
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
    )
    num_group = models.IntegerField(
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
        verbose_name='номер группы',
        help_text='Укажите номер группы',
    )
    priority = models.IntegerField(
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
        verbose_name='Приоритет',
        help_text='Укажите приоритет от 0 до 100',
    )

    def __str__(self):
        return self.text


class NdzPhrase(models.Model):  # фразы Недозвоны
    text = models.CharField(
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        verbose_name = 'Фраза',  # Удобочитаемое имя поля
        max_length = 200,
        help_text = 'Введите текст фразы',  # Дополнительный текст «справки», отображаемый в виджете формы.
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
    )
    group = models.ForeignKey(
        NdzGroupPhrase,
        on_delete=models.CASCADE,
        verbose_name='Принадлежность фразы к группе',
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата создания/изменения',
        help_text='Текущее время (авто)',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    def __str__(self):
        return self.text


class PzGroupPhrase(models.Model):  # группы фраз Пропущенные звонки
    text = models.CharField(
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        verbose_name = 'Название группы',  # Удобочитаемое имя поля
        max_length = 200,
        help_text = 'Дайте короткое название группе',  # Дополнительный текст «справки», отображаемый в виджете формы.
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
    )
    num_group = models.IntegerField(
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
        verbose_name='номер группы',
        help_text='Укажите номер группы',
    )
    priority = models.IntegerField(
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
        verbose_name='Приоритет',
        help_text='Укажите приоритет от 0 до 100',
    )

    def __str__(self):
        return self.text


class PzPhrase(models.Model):  # фразы Пропущенные звонки
    text = models.CharField(
        unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        verbose_name = 'Фраза',  # Удобочитаемое имя поля
        max_length = 200,
        help_text = 'Введите текст фразы',  # Дополнительный текст «справки», отображаемый в виджете формы.
        blank = False,  # Если True, поле может быть пустым. По умолчанию False.
    )
    group = models.ForeignKey(
        PzGroupPhrase,
        on_delete=models.CASCADE,
        verbose_name='Принадлежность фразы к группе',
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата создания/изменения',
        help_text='Текущее время (авто)',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    def __str__(self):
        return self.text
