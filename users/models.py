from django.db import models

# Create your models here.
from jsonfield import JSONField


class User(models.Model):
    avatar_id = models.URLField(blank=True)
    gravatar_id = models.URLField(blank=True)
    type = models.CharField(max_length=24)
    name = models.CharField(max_length=128, db_index=True)
    company = models.CharField(max_length=128)
    blog = models.URLField(blank=True)
    location = models.CharField(max_length=192, blank=True)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    data = JSONField(default=dict)
