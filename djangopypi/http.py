from django.http import HttpResponse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.datastructures import MultiValueDict
from django.contrib.auth import authenticate


class HttpResponseNotImplemented(HttpResponse):
    status_code = 501


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401

    def __init__(self, realm):
        HttpResponse.__init__(self)
        self['WWW-Authenticate'] = 'Basic realm="%s"' % realm


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
