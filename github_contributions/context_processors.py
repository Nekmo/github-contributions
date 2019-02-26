from repos.models import Repository


def count_models(request):
    return {
        'repositories_count': Repository.publics.own().count(),
    }