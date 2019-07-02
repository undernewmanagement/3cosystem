from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'SITE_VERSION': settings.SITE_VERSION
    }