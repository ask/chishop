from django.conf import settings

from djangopypi import conf


def role_from_subdomain(request):
    domain = settings.SITE_DOMAIN
    host = request.META["HTTP_HOST"]
    if host == domain:
        request.pypi_role = conf.DEFAULT_ROLE
    is_def = host == domain
    request.pypi_role = (conf.DEFAULT_ROLE if host == domain else
                                domain.replace("." + host, ""))
    return {"pypi_role": request.pypi_role}
