import github
from django.db import models

# Create your models here.
from django.utils import timezone
from github import NamedUser
from jsonfield import JSONField

from repos.models import Repository


class GithubUserManager(models.Manager):
    def get_or_retrieve(self, login):
        queryset = self.filter(login=login)
        if not queryset.exists():
            user = GithubUser(login=login)
            user.synchronize()
            user.save()
            return user
        return queryset.first()


class GithubUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    avatar_id = models.URLField(blank=True)
    gravatar_id = models.URLField(blank=True)
    type = models.CharField(max_length=24)
    login = models.CharField(max_length=128, db_index=True, unique=True)
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
    stars = models.ManyToManyField(Repository, through='Star', related_name='stargazers')
    forking = models.ManyToManyField(Repository, through='Fork', related_name='forks')
    watching = models.ManyToManyField(Repository, through='Watch', related_name='subscribers')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    synchronized_at = models.DateTimeField()
    data = JSONField(default=dict)

    objects = GithubUserManager()

    def _get_remote_user(self) -> NamedUser:
        g = github.Github()
        return g.get_user(self.login)

    def synchronize(self):
        remote_user = self._get_remote_user()
        self.id = remote_user.id
        self.avatar_id = remote_user.avatar_id
        self.gravatar_id = remote_user.gravatar_id
        self.type = remote_user.type
        self.name = remote_user.name
        self.company = remote_user.company
        self.blog = remote_user.blog
        self.location = remote_user.location
        self.email = remote_user.email
        self.bio = remote_user.bio
        self.created_at = remote_user.created_at
        self.updated_at = remote_user.updated_at
        self.synchronized_at = timezone.now()
        self.data = remote_user.raw_data

    def update_events(self):
        from events.models import Event
        for api_event in self._get_remote_user().get_events():
            actor = GithubUser.objects.get_or_retrieve(api_event.actor.login)
            org = GithubUser.objects.get_or_retrieve(api_event.org.login)
            repo = Repository.objects.get_or_retrieve()
            Event(id=api_event.id, type=api_event.type, payload=api_event.payload,
                  user=self, actor=actor, org=org, repo=repo, public=api_event.public,
                  created_at=api_event.created_at).save()


class Follower(models.Model):
    follower = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    following = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField()


class Star(models.Model):
    user = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)
    created_at = models.DateTimeField()


class Fork(models.Model):
    user = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)
    created_at = models.DateTimeField()


class Watch(models.Model):
    user = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
