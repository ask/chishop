from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from djangopypi.http import HttpResponseUnauthorized, login_basic_auth
from djangopypi.forms import ProjectForm, ReleaseForm
from djangopypi.models import Project, Classifier, Release, UPLOAD_TO
from django.utils.translation import ugettext_lazy as _

ALLOW_VERSION_OVERWRITE = getattr(settings,
                                  "DJANGOPYPI_ALLOW_VERSION_OVERWRITE", False)
ALREADY_EXISTS_FMT = _("""A file named "%s" already exists for %s. To fix """
                     + "problems with that you should create a new release.")


def submit_project_or_release(user, post_data, files):
    """Registers/updates a project or release"""
    try:
        project = Project.objects.get(name=post_data['name'])
        if project.owner != user:
            return HttpResponseForbidden(
                    _("That project is owned by someone else!"))
    except Project.DoesNotExist:
        project = None

    project_form = ProjectForm(post_data, instance=project)
    if project_form.is_valid():
        project = project_form.save(commit=False)
        project.owner = user
        project.save()
        for c in post_data.getlist('classifiers'):
            classifier, created = Classifier.objects.get_or_create(name=c)
            project.classifiers.add(classifier)
        if files:
            try:
                release = Release.objects.get(version=post_data['version'],
                                              project=project,
                                              distribution=UPLOAD_TO + '/' +
                                              files['distribution']._name)
                if not ALLOW_VERSION_OVERWRITE:
                    return HttpResponseForbidden(ALREADY_EXISTS_FMT % (
                                release.filename, release))
            except Release.DoesNotExist:
                release = None

            # If the old file already exists, django will append a _ after the
            # filename, however with .tar.gz files django does the "wrong"
            # thing and saves it as project-0.1.2.tar_.gz. So remove it before
            # django sees anything.
            release_form = ReleaseForm(post_data, files, instance=release)
            if release_form.is_valid():
                if release and os.path.exists(release.distribution.path):
                    os.remove(release.distribution.path)
                release = release_form.save(commit=False)
                release.project = project
                release.save()
            else:
                return HttpResponseBadRequest(
                        _("ERRORS: %s" % release_form.errors))
    else:
        return HttpResponseBadRequest(_("ERRORS: %s" % project_form.errors))

    return HttpResponse()


def register_or_upload(request, post_data, files):
    user = login_basic_auth(request)
    if not user:
        return HttpResponseUnauthorized('pypi')

    login(request, user)
    if not request.user.is_authenticated():
        return HttpResponseForbidden(
                _("Not logged in, or invalid username/password."))

    return submit_project_or_release(user, post_data, files)
