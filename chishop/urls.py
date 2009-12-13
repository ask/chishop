# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include, handler404, handler500
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('')

# Serve static pages.
if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns("django.views",
        url(r"^%s(?P<path>.*)$" % settings.MEDIA_URL[1:], "static.serve", {
            "document_root": settings.MEDIA_ROOT}))

urlpatterns += patterns("",
    # Admin interface
    url(r'^admin/doc/', include("django.contrib.admindocs.urls")),
    url(r'^admin/(.*)', admin.site.root),

    # Registration
    url(r'^accounts/', include('registration.backends.default.urls')),

    # The Chishop
    url(r'', include("djangopypi.urls"))
)
