from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from . import models, serializers, filters


class EventViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    filterset_class = filters.EventFilterSet

    @method_decorator(cache_page(60 * 60 * 24))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def check_filter_present(self, query_param):
        return self.request.query_params.get(query_param, '').strip() != ''

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'list' and not (
            self.check_filter_present('year') and self.check_filter_present('month')
            or self.check_filter_present('upcoming')
        ):
            queryset = queryset.none()

        return queryset
