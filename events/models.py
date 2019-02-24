import github
from django.conf import settings
from django.db import models

# Create your models here.
from jsonfield import JSONField

from repos.models import Repository
from users.models import GithubUser


class EventManager(models.Manager):
    pass


class Event(models.Model):
    id = models.BigIntegerField(primary_key=True)
    type = models.CharField(max_length=32, db_index=True)
    payload = JSONField(default=dict)
    api = models.CharField(max_length=32)
    user = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    actor = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    org = models.ForeignKey(GithubUser, on_delete=models.SET_NULL, blank=True, null=True)
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)
    public = models.BooleanField()
    created_at = models.DateTimeField()

    objects = EventManager()
