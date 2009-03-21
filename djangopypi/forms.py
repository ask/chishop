""" forms.py

Copyright (c) 2009, Ask Solem
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

Neither the name of Ask Solem nor the names of its contributors may be used
to endorse or promote products derived from this software without specific
prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

"""

import os
from django import forms
from djangopypi.models import Project, Classifier, Release


class PermissionDeniedError(Exception):
    """The user did not have the priveliges to execute an action."""


class ProjectRegisterForm(forms.Form):
    name = forms.CharField()
    license = forms.CharField(required=False)
    metadata_version = forms.CharField(initial="1.0")
    author = forms.CharField(required=False)
    home_page = forms.CharField(required=False)
    download_url = forms.CharField(required=False)
    summary = forms.CharField(required=False)
    description = forms.CharField(required=False)
    author_email = forms.CharField(required=False)
    version = forms.CharField()
    platform = forms.CharField(required=False)

    PermissionDeniedError = PermissionDeniedError

    def save(self, classifiers, user, file=None):
        values = dict(self.cleaned_data)
        name = values["name"]
        version = values.pop("version")
        platform = values.pop("platform", "UNKNOWN")
        values["owner"] = user

        try:
            project = Project.objects.get(name=name)
        except Project.DoesNotExist:
            project = Project.objects.create(**values)
        else:
            # If the project already exists,
            # be sure that the current user owns this object.
            if project.owner != user:
                raise self.PermissionDeniedError(
                        "%s doesn't own that project." % user.username)
            [setattr(project, field_name, field_value)
                for field_name, field_value in values.items()]
        project.save()


        for classifier in classifiers:
            project.classifiers.add(
                    Classifier.objects.get_or_create(name=classifier)[0])

        # If the old file already exists, django will append a _ after the
        # filename, however with .tar.gz files django does the "wrong" thing
        # and saves it as project-0.1.2.tar_.gz. So remove it before
        # django sees anything.
        
        if file:
            try:
                release = Release.objects.get(version=version,
                        platform=platform, project=project)
                if os.path.exists(release.distribution.path):
                    os.remove(release.distribution.path)
                release.delete()
            except (Release.DoesNotExist, ValueError):
                pass

        release, created = Release.objects.get_or_create(version=version,
                                                         platform=platform,
                                                         project=project)
        if file:
            release.distribution.save(file.name, file, save=True)
            release.save()
