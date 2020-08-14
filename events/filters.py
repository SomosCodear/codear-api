from django.utils import timezone
import django_filters
from . import models


class EventFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(
        field_name='date',
        lookup_expr='year',
        label='Year',
    )
    month = django_filters.NumberFilter(
        field_name='date',
        lookup_expr='month',
        label='Month',
    )
    upcoming = django_filters.BooleanFilter(
        field_name='date',
        method='filter_upcoming',
        label='upcoming',
    )

    class Meta:
        model = models.Event
        fields = ('year', 'month', 'upcoming')

    def filter_upcoming(self, queryset, name, value):
        if value:
            lookup = f'{name}__gte'
            queryset = queryset.filter(**{lookup: timezone.now()})

        return queryset
