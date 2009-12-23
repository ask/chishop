from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from djangopypi.models import Project, Release
from djangopypi.http import HttpResponseNotImplemented
from djangopypi.http import parse_distutils_request
from djangopypi.views.dists import register_or_upload
from djangopypi.views.users import create_user
from djangopypi.views.search import search


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
        project = Project.objects.get(name=dist_name)
        release = project.releases.get(version=version)
    except (Project.DoesNotExist, Release.DoesNotExist):
        raise Http404()

    context = RequestContext(request, {
        "dist_name": dist_name,
        "version": version,
        "release": release,
        "title": dist_name,
    })

    return render_to_response(template_name, context_instance=context)
