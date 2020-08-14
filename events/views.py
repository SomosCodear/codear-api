from rest_framework import viewsets
from . import models, serializers, filters


class EventViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    filterset_class = filters.EventFilterSet
