from django.db import models

# Create your models here.
from jsonfield import JSONField

from repos.models import Repository


class GithubUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    avatar_id = models.URLField(blank=True)
    gravatar_id = models.URLField(blank=True)
    type = models.CharField(max_length=24)
    login = models.CharField(max_length=128, db_index=True)
    name = models.CharField(max_length=128)
    company = models.CharField(max_length=128)
    blog = models.URLField(blank=True)
    location = models.CharField(max_length=192, blank=True)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField('self', through='Follower', symmetrical=False,
                                       through_fields=('follower', 'following'))
    following = models.ManyToManyField('self', through='Follower', symmetrical=False,
                                       through_fields=('following', 'follower'))
    stars = models.ManyToManyField(Repository, through='Star')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    data = JSONField(default=dict)


class Follower(models.Model):
    follower = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    following = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField()


class Star(models.Model):
    user = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
