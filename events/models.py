import github
from django.conf import settings
from django.db import models

# Create your models here.
from jsonfield import JSONField

from repos.models import Repository
from users.models import GithubUser


class EventQuerySet(models.QuerySet):
    def push_events(self):
        return self.filter(type='PushEvent')

    def star_events(self):
        return self.filter(type='WatchEvent')


class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)

    def push_events(self):
        # TODO: para contar los commits, https://developer.github.com/v3/activity/events/types/#pushevent
        # podría crearse un "fake event" llamado commitEvent. Otra opción es utilizar de alguna manera el
        # "size" del payload. También debería añadirse "action" para otros payloads.
        return self.get_queryset().push_events()

    def star_events(self):
        return self.get_queryset().star_events()


class Event(models.Model):
    id = models.BigIntegerField(primary_key=True)
    type = models.CharField(max_length=32, db_index=True)
    payload = JSONField(default=dict)
    api = models.CharField(max_length=32)
    user = models.ForeignKey(GithubUser, on_delete=models.CASCADE, related_name='own_events')
    actor = models.ForeignKey(GithubUser, on_delete=models.CASCADE, related_name='acted_events')
    org = models.ForeignKey(GithubUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='org_events')
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='events')
    public = models.BooleanField()
    created_at = models.DateTimeField()

    objects = EventManager()
