from django.db import models

# Create your models here.
from jsonfield import JSONField

from users.models import GithubUser


class Repository(models.Model):
    user = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    private = models.BooleanField()
    description = models.TextField(blank=True)
    fork = models.BooleanField()
    homepage = models.URLField(blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    has_projects = models.BooleanField()
    has_wiki = models.BooleanField()
    has_pages = models.BooleanField()
    archived = models.BooleanField()
    mirror_url = models.URLField(blank=True)
    data = JSONField(default=dict)
