from .models import FilterBOND
from django import forms


class FilterBONDForm(forms.ModelForm):
    class Meta:
        model = FilterBOND
        # fields = ('name', 'sex', 'short_names',)
        fields = [field.name for field in FilterBOND._meta.get_fields()]


    # name = models.CharField(  # Название переменной
        # max_length = 100,
        # unique = True,  # Если True, это поле должно быть уникальным во всей таблице.
        # verbose_name = 'Название',
    # )
    # check_facevalue_from = models.BooleanField(
        # blank = True,
        # null = True,
        # default = 'False',
        # verbose_name = 'активно Номинал от',
    # )
    # facevalue_from = models.IntegerField(
        # blank = True,
        # null = True,
        # verbose_name = 'Номинал от',
    # )
    # check_facevalue_to = models.BooleanField(
        # blank = True,
        # null = True,
        # default = 'False',
        # verbose_name = 'активно Номинал до',
    # )
    # facevalue_to = models.IntegerField(
        # blank = True,
        # null = True,
        # verbose_name = 'Номинал до',
    # )
    # check_matdate_from = models.BooleanField(
        # blank = True,
        # null = True,
        # default = 'False',
        # verbose_name = 'активно Погашение от',
    # )
    # matdate_from = models.DateTimeField(
        # blank = True,
        # null = True,
        # verbose_name = 'Погашение от',
    # )
    # check_matdate_to = models.BooleanField(
        # blank = True,
        # null = True,
        # default = 'False',
        # verbose_name = 'активно Погашение до',
    # )
    # matdate_to = models.DateTimeField(
        # blank = True,
        # null = True,
        # verbose_name = 'Погашение до',
    # )
    # check_profit_from = models.BooleanField(
        # blank = True,
        # null = True,
        # default = 'False',
        # verbose_name = 'активно Доходность от',
    # )
    # profit_from = models.DecimalField(
        # max_digits = 10,
        # decimal_places = 2,
        # blank = True,
        # null = True,
        # verbose_name = 'Доходность от',
    # )
    # check_profit_to = models.BooleanField(
        # blank = True,
        # null = True,
        # default = 'False',
        # verbose_name = 'активно Доходность до',
    # )
    # profit_to = models.DecimalField(
        # max_digits = 10,
        # decimal_places = 2,
        # blank = True,
        # null = True,
        # verbose_name = 'Доходность до',
    # )
    # by_type = models.CharField(
        # max_length = 256,
        # blank = True,
        # null = True,
        # verbose_name = 'Типы',
    # )

