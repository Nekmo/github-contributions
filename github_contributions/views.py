from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'github_contributions/index.html'

    def get_context_data(self, **kwargs):
        return dict(

            **super().get_context_data(**kwargs)
        )
