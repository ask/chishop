from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models.query import Q

from djangopypi.models import Project


def _search_query(q):
    return Q(name__contains=q) | Q(summary__contains=q)


def search(request, template="djangopypi/search_results.html"):
    context = RequestContext(request, {"dists": None, "search_term": ""})

    if request.method == "POST":
        search_term = context["search_term"] = request.POST.get("search_term")
        if search_term:
            query = _search_query(search_term)
            context["dists"] = Project.objects.filter(query)

    if context["dists"] is None:
        context["dists"] = Project.objects.all()

    return render_to_response(template, context_instance=context)
