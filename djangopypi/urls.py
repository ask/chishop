# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns("",
    # Simple PyPI
    url(r'^/?$', "djangopypi.views.simple",
        name="djangopypi-simple"),

    url(r'^(?P<dist_name>[\w\d_\.\-]+)/(?P<version>[\w\.\d\-_]+)/?',
        "djangopypi.views.show_version",
        name="djangopypi-show_version"),

    url(r'^(?P<dist_name>[\w\d_\.\-]+)/?', "djangopypi.views.show_links",
        name="djangopypi-show_links"),
)

