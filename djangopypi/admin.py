from django.contrib import admin
from djangopypi.models import Project, Release

admin.site.register(Project)
admin.site.register(Release)
