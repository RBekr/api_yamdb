import django_filters

from reviews.models import Genre, Category, Title


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug")
    genre = django_filters.CharFilter(field_name="genre__slug")
    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')