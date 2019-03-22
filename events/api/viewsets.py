from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=False)
    def daily_stats(self, request):
        queryset = self.get_queryset()
        queryset = queryset.order_by('created_at').values('created_at').annotate(Sum('created_at__date'))
        return Response(queryset)
