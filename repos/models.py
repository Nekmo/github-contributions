import github
from django.db import models

# Create your models here.
from github.Repository import Repository as GHRepository
from jsonfield import JSONField

from users.models import GithubUser


class RepositoryManager(models.Manager):
    def get_or_retrieve(self, login):
        queryset = self.filter(login=login)
        if not queryset.exists():
            user = Repository(login=login)
            user.synchronize()
            user.save()
            return user
        return queryset.first()


class Repository(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    owner = models.CharField(max_length=100)
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

    def _get_remote_repo(self) -> GHRepository:
        g = github.Github()
        return g.get_repo(self.id)

    def synchronize(self):
        remote_repo = self._get_remote_repo()
        self.name = remote_repo.name
        self.full_name = remote_repo.full_name
        self.full_name = remote_repo.full_name
        self.private = remote_repo.private
        self.description = remote_repo.description
        self.default_branch = remote_repo.default_branch
        self.fork = remote_repo.fork
        self.homepage = remote_repo.homepage
        self.created_at = remote_repo.created_at
        self.updated_at = remote_repo.updated_at
        self.has_issues = remote_repo.has_issues
        self.has_projects = remote_repo.has_projects
        self.has_wiki = remote_repo.has_wiki
        self.has_pages = False  # TODO: not available
        self.has_downloads = remote_repo.has_downloads
        self.archived = remote_repo.archived
        self.mirror_url = remote_repo.mirror_url
        self.data = remote_repo.raw_data
        self.owner = GithubUser.objects.get_or_retrieve(remote_repo.owner.login)
