# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, QueryDict
from django.shortcuts import render_to_response
from djangopypi.models import Project
from djangopypi.forms import ProjectRegisterForm
from django.template import RequestContext
from yadayada.utils import template_path_builder
from django.utils.datastructures import MultiValueDict
from django.core.files.uploadedfile import SimpleUploadedFile

T = template_path_builder("djangopypi")


def parse_weird_post_data(data):
    sep = data.splitlines()[1]
    items = data.split(sep)
    post_data = {}
    files = {}
    for part in items:
        if not part.strip():
            continue
        item = part.splitlines()
        if len(item) < 2: continue
        header = item[1].replace("Content-Disposition: form-data; ", "")
        kvpairs = header.split(";")
        headers = {}
        for kvpair in kvpairs:
            if not kvpair: continue
            key, value = kvpair.split("=")
            headers[key] = value.strip('"')
        if not "name" in headers: continue
        content = part[len("\n".join(item[0:2]))+2:len(part)-1]
        if "filename" in headers:
            file = SimpleUploadedFile(headers["filename"], content,
                    content_type="application/gzip")
            files[headers["name"]] = file
        elif headers["name"] in post_data:
            post_data[headers["name"]].append(content)
        else:
            post_data[headers["name"]] = [content]

    return MultiValueDict(post_data), files


def simple(request, template_name=T("simple")):
    if request.method == "POST":
        post_data, files = parse_weird_post_data(request.raw_post_data)
        action = post_data.get(":action")
        classifiers = post_data.getlist("classifiers")
        register_form = ProjectRegisterForm(post_data.copy())
        if register_form.is_valid():
            return HttpResponse(register_form.save(classifiers,
                file=files.get("content")))
            return HttpResponse("Successfully registered.")
        return HttpResponse("ERRORS: %s" % register_form.errors)

    dists = Project.objects.all()
    context = RequestContext(request, {
        "dists": dists,
    })

    return render_to_response(template_name, context_instance=context)

def show_links(request, dist_name, template_name=T("show_links")):
    releases = Project.objects.get(name=dist_name) \
                    .releases.all().order_by('-version')

    context = RequestContext(request, {
        "dist_name": dist_name,
        "releases": releases,
    })

    return render_to_response(template_name, context_instance=context)

def show_version(request, dist_name, version, template_name=T("show_version")):
    release = Project.objects.get(name=dist_name).releases \
                                    .get(version=version)

    context = RequestContext(request, {
        "dist_name": dist_name,
        "version": version,
        "release": release,
    })

    return render_to_response(template_name, context_instance=context)
