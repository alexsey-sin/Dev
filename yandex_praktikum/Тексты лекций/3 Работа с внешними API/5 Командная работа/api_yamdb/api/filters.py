from django_filters import rest_framework as filters

from api.models import Title


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class TitleFilter(filters.FilterSet):
    genre = CharFilterInFilter(field_name='genre__slug', lookup_expr='in')
    category = CharFilterInFilter(field_name='category__slug',
                                  lookup_expr='in')
    name = filters.CharFilter(lookup_expr='icontains')
    year = filters.NumberFilter()

    class Meta:
        model = Title
        fields = ['category', 'genre', 'year', 'name']
