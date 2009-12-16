import os
from django import forms
from django.conf import settings
from djangopypi.models import Project, Classifier, Release
from django.utils.translation import ugettext_lazy as _


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['owner', 'classifiers']


class ReleaseForm(forms.ModelForm):
    class Meta:
        model = Release
        exclude = ['project']