import cgi
import os

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.http import QueryDict, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.datastructures import MultiValueDict
from django.utils.translation import ugettext_lazy as _
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import authenticate, login
from django.db.models import Q

from registration.backends import get_backend
from registration.forms import RegistrationForm

from djangopypi.models import Project, Classifier, Release, UPLOAD_TO
from djangopypi.forms import ProjectForm, ReleaseForm
from djangopypi.http import HttpResponseUnauthorized
from djangopypi.http import HttpResponseNotImplemented
from djangopypi.utils import decode_fs


ALREADY_EXISTS_FMT = _("""A file named "%s" already exists for %s. To fix """
                     + "problems with that you should create a new release.")


def parse_distutils_request(request):
    raw_post_data = request.raw_post_data
    sep = raw_post_data.splitlines()[1]
    items = raw_post_data.split(sep)
    post_data = {}
    files = {}
    for part in filter(lambda e: not e.isspace(), items):
        item = part.splitlines()
        if len(item) < 2:
            continue
        header = item[1].replace("Content-Disposition: form-data; ", "")
        kvpairs = header.split(";")
        headers = {}
        for kvpair in kvpairs:
            if not kvpair:
                continue
            key, value = kvpair.split("=")
            headers[key] = value.strip('"')
        if "name" not in headers:
            continue
        content = part[len("\n".join(item[0:2]))+2:len(part)-1]
        if "filename" in headers:
            file = SimpleUploadedFile(headers["filename"], content,
                    content_type="application/gzip")
            files["distribution"] = [file]
        elif headers["name"] in post_data:
            post_data[headers["name"]].append(content)
        else:
            # Distutils sends UNKNOWN for empty fields (e.g platform)
            # [russell.sim@gmail.com]
            if content == 'UNKNOWN':
                post_data[headers["name"]] = [None]
            else:
                post_data[headers["name"]] = [content]
 
    return MultiValueDict(post_data), MultiValueDict(files)



def login_basic_auth(request):
    authentication = request.META.get("HTTP_AUTHORIZATION")
    if not authentication:
        return
    (authmeth, auth) = authentication.split(' ', 1)
    if authmeth.lower() != "basic":
        return
    auth = auth.strip().decode("base64")
    username, password = auth.split(":", 1)
    return authenticate(username=username, password=password)


def submit_project_or_release(user, post_data, files):
    """Registers/updates a project or release"""
    try:
        project = Project.objects.get(name=post_data['name'])
        if project.owner != user:
            return HttpResponseForbidden(
                    "That project is owned by someone else!")
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
            allow_overwrite = getattr(settings,
                "DJANGOPYPI_ALLOW_VERSION_OVERWRITE", False)
            try:
                release = Release.objects.get(version=post_data['version'],
                                              project=project,
                                              distribution=UPLOAD_TO + '/' +
                                              files['distribution']._name)
                if not allow_overwrite:
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
                        "ERRORS: %s" % release_form.errors)
    else:
        return HttpResponseBadRequest("ERRORS: %s" % project_form.errors)

    return HttpResponse()


def register_or_upload(request, post_data, files):
    user = login_basic_auth(request)
    if not user:
        return HttpResponseUnauthorized('pypi')

    login(request, user)
    if not request.user.is_authenticated():
        return HttpResponseForbidden(
                "Not logged in, or invalid username/password.")

    return submit_project_or_release(user, post_data, files)

def create_user(request, post_data, files):
    """Create new user from a distutil client request"""
    form = RegistrationForm({"username": post_data["name"],
                             "email": post_data["email"],
                             "password1": post_data["password"],
                             "password2": post_data["password"]})
    if not form.is_valid():
        # Dist Utils requires error msg in HTTP status: "HTTP/1.1 400 msg"
        # Which is HTTP/WSGI incompatible, so we're just returning a empty 400.
        return HttpResponseBadRequest()

    backend = get_backend("registration.backends.default.DefaultBackend")
    if not backend.registration_allowed(request):
        return HttpResponseBadRequest()
    new_user = backend.register(request, **form.cleaned_data)
    return HttpResponse("OK\n", status=200, mimetype='text/plain')


ACTIONS = {
    # file_upload is the action used with distutils ``sdist`` command.
    "file_upload": register_or_upload,

    # submit is the :action used with distutils ``register`` command.
    "submit": register_or_upload,

    # user is the action used when registering a new user
    "user": create_user,
}


def simple(request, template_name="djangopypi/simple.html"):
    if request.method == "POST":
        post_data, files = parse_distutils_request(request)
        action_name = post_data.get(":action")
        if action_name not in ACTIONS:
            return HttpResponseNotImplemented(
                "The action %s is not implemented" % action_name)
        return ACTIONS[action_name](request, post_data, files)

    dists = Project.objects.all().order_by("name")
    context = RequestContext(request, {
        "dists": dists,
        "title": 'Package Index',
    })

    return render_to_response(template_name, context_instance=context)


def show_links(request, dist_name,
        template_name="djangopypi/show_links.html"):
    try:
        project = Project.objects.get(name=dist_name)
        releases = project.releases.all().order_by('-version')
    except Project.DoesNotExist:
        raise Http404

    context = RequestContext(request, {
        "dist_name": dist_name,
        "releases": releases,
        "project": project,
        "title": project.name,
    })

    return render_to_response(template_name, context_instance=context)


def show_version(request, dist_name, version,
        template_name="djangopypi/show_version.html"):
    try:
        release = Project.objects.get(name=dist_name).releases \
                                        .get(version=version)
    except Project.DoesNotExist:
        raise Http404()

    context = RequestContext(request, {
        "dist_name": dist_name,
        "version": version,
        "release": release,
        "title": dist_name,
    })

    return render_to_response(template_name, context_instance=context)
    
def search(request):
    search_value = ''
    if request.method == 'POST':
        search_value = request.POST.get('search_value')
        if search_value != '':
            dists = Project.objects.filter(Q(name__contains=search_value) | Q(summary__contains=search_value))
            return render_to_response(
                'djangopypi/search_results.html',
                {'dists':dists,'search_value':search_value},
                context_instance = RequestContext(request)
                )
        else:
            dists = Project.objects.all()
            return render_to_response(
                'djangopypi/search_results.html',
                {'search_value':search_value},
                context_instance = RequestContext(request)
                )
    else:
        dists = Project.objects.all()
        return render_to_response(
            'djangopypi/search_results.html',
            {'search_value':search_value},
            context_instance = RequestContext(request)
            )