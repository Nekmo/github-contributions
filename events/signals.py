from django.db.models.signals import post_save
from django.dispatch import receiver

from events.models import Event


@receiver(post_save, sender=Event)
def parse_event(sender, instance: Event, **kwargs):
    instance.parse_event()


def dummy():
    pass
