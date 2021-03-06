from django.conf import settings
from django.core.management.base import BaseCommand

from users.models import GithubUser


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        user = GithubUser.objects.get_or_retrieve(settings.GITHUB_USER)
        user.update_followers()
        user.update_following()
        user.update_repos()
        for repository in user.repositories.all():
            repository.update_stars()
            repository.update_subscribers()
            repository.update_forks()
