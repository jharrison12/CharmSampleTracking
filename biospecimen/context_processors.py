from django.conf import settings


def staging_or_production(request):
    # return the value you want as a dictionary. you may add multiple values in there.
    return {'STAGING_OR_PRODUCTION': settings.STAGING_OR_PRODUCTION}