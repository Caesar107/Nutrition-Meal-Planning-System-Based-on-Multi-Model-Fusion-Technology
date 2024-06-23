from mysite import settings
def global_site_name(request):
    return {'site_name': settings.SITE_NAME,}