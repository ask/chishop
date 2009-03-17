# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('')

# Serve static pages.
if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns("django.views",
        url(r"%s(?P<path>.*)$" % settings.MEDIA_URL[1:], "static.serve", {
            "document_root": settings.MEDIA_ROOT}))
urlpatterns += patterns("",
    # Admin interface
    url(r'^admin/doc/', include("django.contrib.admindocs.urls")),
    url(r'^admin/(.*)', admin.site.root),

    # Simple PyPI
    url(r'^/?$', "djangopypi.views.simple",
        name="djangopypi-simple"),

    url(r'^(?P<dist_name>[\w\d_\-]+)/(?P<version>[\w\.\d\-_]+)/?',
        "djangopypi.views.show_version",
        name="djangopypi-show_version"),

    url(r'^(?P<dist_name>[\w\d_\-]+)/?', "djangopypi.views.show_links",
        name="djangopypi-show_links"),
    

)

