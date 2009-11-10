import sys
import traceback

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.datastructures import MultiValueDict


def transmute(f):
    if hasattr(f, "filename") and f.filename:
        v = SimpleUploadedFile(f.filename, f.value, f.type)
    else:
        v = f.value.decode("utf-8")
    return v


def decode_fs(fs):
    POST, FILES = {}, {}
    for k in fs.keys():
        v = transmute(fs[k])
        if isinstance(v, SimpleUploadedFile):
            FILES[k] = [v]
        else:
            # Distutils sends UNKNOWN for empty fields (e.g platform)
            # [russell.sim@gmail.com]
            if v == "UNKNOWN":
                v = None
            POST[k] = [v]
    return MultiValueDict(POST), MultiValueDict(FILES)


def debug(func):
    # @debug is handy when debugging distutils requests
    def _wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            traceback.print_exception(*sys.exc_info())
    return _wrapped