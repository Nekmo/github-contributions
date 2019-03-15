import os

import requests
from django.conf import settings

from events.models import Event
from events.parsers.base import ParserBase
from users.models import GithubUser


class PushEvent(ParserBase):

    def parse(self):
        for commit in self.payload['commits']:
            r = requests.get(commit['url'], auth=(settings.GITHUB_USER, settings.GITHUB_TOKEN))
            r.raise_for_status()
            data = r.json()
            user = GithubUser.objects.get(login=data['author']['login'])
            Event.objects.create(type='CommitEvent', payload=data, user=user, actor=user, repo=self.event.repo,
                                 public=self.event.public, api='parsed',
                                 created_at=data['commit']['committer']['date'])
