from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'GOOGLE_ANALYTICS': settings.GOOGLE_ANALYTICS,
        'SITE_VERSION': settings.SITE_VERSION
    }