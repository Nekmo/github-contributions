from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'event_id')
