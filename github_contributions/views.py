from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'github_contributions/index.html'
