from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from events.api.serializers import EventSerializer
from events.models import Event


class EventViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('id', 'event_id')
    # filterset_class = EventFilter
    ordering_fields = search_fields
