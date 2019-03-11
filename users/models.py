import github
import pytz
from django.conf import settings
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


class StarQuerySet(models.QuerySet):
    def own(self):
        return self.filter(repo__owner__login=settings.GITHUB_USER)


class StarManager(models.Manager):
    def get_queryset(self):
        return StarQuerySet(self.model, using=self._db)

    def own(self):
        return self.get_queryset().own()


class FollowerQuerySet(models.QuerySet):
    def own(self):
        return self.filter(following__login=settings.GITHUB_USER)


class FollowerManager(models.Manager):
    def get_queryset(self):
        return FollowerQuerySet(self.model, using=self._db)

    def own(self):
        return self.get_queryset().own()


class WatchQuerySet(models.QuerySet):
    def own(self):
        return self.filter(repo__owner__login=settings.GITHUB_USER)


class WatchManager(models.Manager):
    def get_queryset(self):
        return WatchQuerySet(self.model, using=self._db)

    def own(self):
        return self.get_queryset().own()


class ForkQuerySet(models.QuerySet):
    def own(self):
        return self.filter(repo__owner__login=settings.GITHUB_USER)


class ForkManager(models.Manager):
    def get_queryset(self):
        return ForkQuerySet(self.model, using=self._db)

    def own(self):
        return self.get_queryset().own()


class GithubUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    avatar_url = models.URLField(blank=True)
    gravatar_id = models.URLField(blank=True)
    type = models.CharField(max_length=24)
    login = models.CharField(max_length=128, db_index=True, unique=True)
    name = models.CharField(max_length=128, blank=True)
    company = models.CharField(max_length=128)
    blog = models.URLField(blank=True)
    location = models.CharField(max_length=192, blank=True)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)
    following = models.ManyToManyField('self', through='Follower', symmetrical=False,
                                       related_name='followers',
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
        g = github.Github(settings.GITHUB_USER, settings.GITHUB_TOKEN)
        return g.get_user(self.login)

    def synchronize(self):
        remote_user = self._get_remote_user()
        self.id = remote_user.id
        self.avatar_url = remote_user.avatar_url
        self.gravatar_id = remote_user.gravatar_id
        self.type = remote_user.type
        self.name = remote_user.name or ''
        self.company = remote_user.company or ''
        self.blog = remote_user.blog or ''
        self.location = remote_user.location or ''
        self.email = remote_user.email or ''
        self.bio = remote_user.bio or ''
        self.created_at = remote_user.created_at.replace(tzinfo=pytz.UTC)
        self.updated_at = remote_user.updated_at.replace(tzinfo=pytz.UTC)
        self.synchronized_at = timezone.now()
        self.data = remote_user.raw_data

    def update_events(self):
        from events.models import Event
        for api_event in self._get_remote_user().get_events():
            actor = GithubUser.objects.get_or_retrieve(api_event.actor.login)
            org = None
            if api_event.org:
                org = GithubUser.objects.get_or_retrieve(api_event.org.login)
            repo = Repository.objects.get_or_retrieve(api_event.repo.id)
            Event.objects.get_or_create(id=api_event.id, defaults=dict(
                type=api_event.type, payload=api_event.payload, api='events',
                user=self, actor=actor, org=org, repo=repo, public=api_event.public,
                created_at=api_event.created_at.replace(tzinfo=pytz.UTC)))

    def update_followers(self):
        for follower in self._get_remote_user().get_followers():
            user = GithubUser.objects.get_or_retrieve(follower.login)
            Follower.objects.get_or_create(follower=user, following=self,
                                           defaults=dict(created_at=timezone.now()))

    def update_following(self):
        for follower in self._get_remote_user().get_following():
            user = GithubUser.objects.get_or_retrieve(follower.login)
            Follower.objects.get_or_create(follower=self, following=user,
                                           defaults=dict(created_at=timezone.now()))

    def update_repos(self):
        for repo in self._get_remote_user().get_repos():
            Repository.objects.get_or_retrieve(repo.id)


class Follower(models.Model):
    """TODO: this event is not fired: https://developer.github.com/v3/activity/events/types/
    A manual sync is required.
    """
    follower = models.ForeignKey(GithubUser, on_delete=models.CASCADE, related_name='+')
    following = models.ForeignKey(GithubUser, on_delete=models.CASCADE, related_name='+')
    created_at = models.DateTimeField()

    objects = FollowerManager()


class Star(models.Model):
    user = models.ForeignKey(GithubUser, on_delete=models.CASCADE, related_name='+')
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='+')
    created_at = models.DateTimeField()

    objects = StarManager()


class Fork(models.Model):
    user = models.ForeignKey(GithubUser, on_delete=models.CASCADE, related_name='+')
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='+')
    created_at = models.DateTimeField()

    objects = ForkManager()


class Watch(models.Model):
    user = models.ForeignKey(GithubUser, on_delete=models.CASCADE, related_name='+')
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='+')
    created_at = models.DateTimeField()

    objects = WatchManager()
