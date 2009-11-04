import os
from django.http import Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _
from djangopypi.http import HttpResponseNotImplemented, parse_weird_post_data
from djangopypi.models import Project
from djangopypi import actions

ACTIONS = {
    # file_upload is the action used with the distutils ``sdist`` command.
    "file_upload": actions.register_or_upload,

    # submit is the :action used with the distutils ``register`` command.
    "submit": actions.register_or_upload,
}


def action(request):
    if request.method != "POST":
        return HttpResponseBadRequest()

    post_data, files = parse_weird_post_data(request.raw_post_data)
    action_name = post_data.get(":action")
    if action_name not in ACTIONS:
        return HttpResponseNotImplemented(
            "Action %s is not implemented" % action_name)
    return ACTIONS[action_name](request, post_data, files)


def simple(request, template_name="djangopypi/simple.html",
        title=_("Package Index")):
    if request.method == "POST":
        return action(request)

    dists = Project.objects.all().order_by("name")
    context = RequestContext(request, {
        "dists": dists,
        "title": title,
    })

    return render_to_response(template_name, context_instance=context)


def show_links(request, dist_name,
        template_name="djangopypi/show_links.html"):
    try:
        project = Project.objects.get(name=dist_name)
        releases = project.releases.all().order_by('-version')
    except Project.DoesNotExist:
        raise Http404(_("No such project: %s" % dist_name))

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
    except Project.DoesNotExist:
        raise Http404(_("No such project: %s" % project))

    context = RequestContext(request, {
        "dist_name": dist_name,
        "version": version,
        "release": release,
        "title": dist_name,
    })

    return render_to_response(template_name, context_instance=context)
