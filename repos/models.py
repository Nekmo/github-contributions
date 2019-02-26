import github
import pytz
from django.conf import settings
from django.db import models

# Create your models here.
from django.utils import timezone
from github.Repository import Repository as GHRepository
from jsonfield import JSONField


class RepositoryQuerySet(models.QuerySet):
    def own(self):
        return self.filter(owner__login=settings.GITHUB_USER)


class RepositoryManager(models.Manager):
    def get_queryset(self):
        return RepositoryQuerySet(self.model, using=self._db)

    def get_or_retrieve(self, id_):
        queryset = self.filter(id=id_)
        if not queryset.exists():
            user = Repository(id=id_)
            user.synchronize()
            user.save()
            return user
        return queryset.first()

    def own(self):
        return self.get_queryset().own()


class PublicRepositoryManager(RepositoryManager):
    def get_queryset(self):
        return super().get_queryset().filter(private=False)


class Repository(models.Model):
    id = models.BigIntegerField(primary_key=True)
    owner = models.ForeignKey('users.GithubUser', on_delete=models.CASCADE, related_name='repositories')
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255)
    private = models.BooleanField()
    description = models.TextField(blank=True)
    default_branch = models.CharField(max_length=100, default='master')
    fork = models.BooleanField()
    homepage = models.URLField(blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    has_issues = models.BooleanField()
    has_projects = models.BooleanField()
    has_wiki = models.BooleanField()
    has_pages = models.BooleanField()
    has_downloads = models.BooleanField()
    archived = models.BooleanField()
    mirror_url = models.URLField(blank=True)
    data = JSONField(default=dict)

    objects = RepositoryManager()
    publics = PublicRepositoryManager()

    def _get_remote_repo(self) -> GHRepository:
        g = github.Github(settings.GITHUB_USER, settings.GITHUB_TOKEN)
        return g.get_repo(self.id)

    def synchronize(self):
        from users.models import GithubUser
        remote_repo = self._get_remote_repo()
        self.name = remote_repo.name
        self.full_name = remote_repo.full_name
        self.full_name = remote_repo.full_name
        self.private = remote_repo.private
        self.description = remote_repo.description or ''
        self.default_branch = remote_repo.default_branch
        self.fork = remote_repo.fork
        self.homepage = remote_repo.homepage or ''
        self.created_at = remote_repo.created_at.replace(tzinfo=pytz.UTC)
        self.updated_at = remote_repo.updated_at.replace(tzinfo=pytz.UTC)
        self.has_issues = remote_repo.has_issues
        self.has_projects = remote_repo.has_projects
        self.has_wiki = remote_repo.has_wiki
        self.has_pages = False  # TODO: not available
        self.has_downloads = remote_repo.has_downloads
        self.archived = remote_repo.archived
        self.mirror_url = remote_repo.mirror_url or ''
        self.data = remote_repo.raw_data
        self.owner = GithubUser.objects.get_or_retrieve(remote_repo.owner.login)

    def update_stars(self):
        from users.models import Star, GithubUser
        for star in self._get_remote_repo().get_stargazers_with_dates():
            user = GithubUser.objects.get_or_retrieve(star.user.login)
            Star.objects.get_or_create(repo=self, user=user,
                                       defaults=dict(created_at=star.starred_at.replace(tzinfo=pytz.UTC)))

    def update_subscribers(self):
        from users.models import Watch, GithubUser
        for watcher in self._get_remote_repo().get_subscribers():
            user = GithubUser.objects.get_or_retrieve(watcher.login)
            Watch.objects.get_or_create(repo=self, user=user,
                                        defaults=dict(created_at=timezone.now()))

    def update_forks(self):
        from users.models import Fork, GithubUser
        for repo in self._get_remote_repo().get_forks():
            user = GithubUser.objects.get_or_retrieve(repo.owner.login)
            Fork.objects.get_or_create(user=user, repo=self,
                                       defaults=dict(created_at=timezone.now()))
