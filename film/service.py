from django_filters import rest_framework as filters

from film.models import Video


class CharFilterInFilter(filters.CharFilter):
    pass


class FilmFilter(filters.FilterSet):
    category = CharFilterInFilter(field_name='category__name')
    class Meta:
        model = Video
        fields = ['category']