from django import forms
from djangopypi.models import Project, Classifier, Release

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

    def save(self, classifiers, file=None):
        values = dict(self.cleaned_data)
        name = values.pop("name")
        version = values.pop("version")
        platform = values.pop("platform")
        project, c = Project.objects.get_or_create(name=name, defaults=values)
        for classifier in classifiers:
            project.classifiers.add(
                    Classifier.objects.get_or_create(name=classifier)[0])
        release, c = Release.objects.get_or_create(version=version,
                platform=platform, project=project)
        if file:
            release.distribution.save(file.name, file, save=True)
            release.save()


    


