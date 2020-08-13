from rest_framework import viewsets
from . import models, serializers


class EventViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
