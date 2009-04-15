# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns("djangopypi.views",
    # Simple PyPI
    url(r'^$', "simple",
        name="djangopypi-simple"),

    url(r'^(?P<dist_name>[\w\d_\.\-]+)/(?P<version>[\w\.\d\-_]+)/$',
        "show_version",
        name="djangopypi-show_version"),

    url(r'^(?P<dist_name>[\w\d_\.\-]+)/$', "show_links",
        name="djangopypi-show_links"),
)

