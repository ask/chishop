# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns("djangopypi.views",
    # Simple PyPI
    url(r'^simple/$', "simple",
        name="djangopypi-simple"),

    url(r'^simple/(?P<dist_name>[\w\d_\.\-]+)/(?P<version>[\w\.\d\-_]+)/$',
        "show_version",
        name="djangopypi-show_version"),

    url(r'^simple/(?P<dist_name>[\w\d_\.\-]+)/$', "show_links",
        name="djangopypi-show_links"),

    url(r'^$', "simple", {'template_name': 'djangopypi/pypi.html'},
        name="djangopypi-pypi"),

    url(r'^(?P<dist_name>[\w\d_\.\-]+)/$', "show_links",
        {'template_name': 'djangopypi/pypi_show_links.html'},
        name="djangopypi-pypi_show_links"),
    
    url(r'^search','search',name='djangopypi-search')
)