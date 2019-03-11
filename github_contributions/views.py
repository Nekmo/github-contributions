import datetime

from django.utils import timezone
from django.views.generic import TemplateView

from events.models import Event
from users.models import Star, Follower, Watch


class IndexView(TemplateView):
    template_name = 'github_contributions/index.html'

    def get_context_data(self, **kwargs):
        a_week_ago = timezone.now() - datetime.timedelta(days=7)
        counters_filter = dict(created_at__gte=a_week_ago)
        counters = dict(
            stars_count=Star.objects.filter(**counters_filter).own().count(),
            followers_count=Follower.objects.filter(**counters_filter).own().count(),
            watchers_count=Watch.objects.filter(**counters_filter).own().count(),
        )
        return dict(
            counters,
            **super().get_context_data(**kwargs)
        )
