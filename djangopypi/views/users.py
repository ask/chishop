from django.http import HttpResponse, HttpResponseBadRequest

from registration.forms import RegistrationForm
from registration.backends import get_backend

DEFAULT_BACKEND = "registration.backends.default.DefaultBackend"


def create_user(request, post_data, files, backend_name=DEFAULT_BACKEND):
    """Create new user from a distutil client request"""
    form = RegistrationForm({"username": post_data["name"],
                             "email": post_data["email"],
                             "password1": post_data["password"],
                             "password2": post_data["password"]})
    if not form.is_valid():
        # Dist Utils requires error msg in HTTP status: "HTTP/1.1 400 msg"
        # Which is HTTP/WSGI incompatible, so we're just returning a empty 400.
        return HttpResponseBadRequest()

    backend = get_backend(backend_name)
    if not backend.registration_allowed(request):
        return HttpResponseBadRequest()
    new_user = backend.register(request, **form.cleaned_data)
    return HttpResponse("OK\n", status=200, mimetype='text/plain')
